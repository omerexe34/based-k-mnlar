import html
import json
import random
import datetime

from flask import request, jsonify, session
from extensions import app, supabase, logger
from cache import app_cache
from storage import upload_base64_to_storage

def _get_current_user():
    return session.get("username")

def _is_admin(username: str) -> bool:
    if not username:
        return False
    cached = app_cache.get(f"role:{username}")
    if cached is not None:
        return cached in ("Admin", "SubAdmin")
    try:
        res = supabase.table("users").select("role").eq("username", username).execute()
        if res.data:
            role = res.data[0].get("role", "")
            app_cache.set(f"role:{username}", role, ttl=120)
            return role in ("Admin", "SubAdmin")
    except Exception as exc:
        logger.warning("_is_admin sorgu hatası: %s", exc)
    return False

def _auto_finalize(gw: dict):
    gw_id = gw.get("id")
    participants = gw.get("participants") or []
    winner_count = gw.get("winner_count") or 1
    admin_pick_mode = gw.get("admin_pick_mode") or False
    admin_picked_usernames = gw.get("admin_picked_usernames") or []

    if not participants:
        supabase.table("giveaways").update({
            "status": "cancelled",
            "finalized_at": datetime.datetime.utcnow().isoformat()
        }).eq("id", gw_id).execute()
        return

    winners = []

    # Admin önceden kazananları seçmişse onları kullan
    if admin_pick_mode and admin_picked_usernames:
        for uname in admin_picked_usernames:
            for p in participants:
                if isinstance(p, dict) and p.get("username") == uname:
                    winners.append({"username": p.get("username"), "instagram": p.get("instagram", "")})
                    break
                elif p == uname:
                    winners.append({"username": p, "instagram": ""})
                    break
    
    # Admin seçimi yoksa veya boşsa rastgele seç
    if not winners:
        count_to_pick = min(winner_count, len(participants))
        selected_participants = random.sample(participants, count_to_pick)
        for winner_entry in selected_participants:
            if isinstance(winner_entry, dict):
                winners.append({
                    "username": winner_entry.get("username", ""),
                    "instagram": winner_entry.get("instagram", "")
                })
            else:
                winners.append({"username": str(winner_entry), "instagram": ""})

    try:
        supabase.table("giveaways").update({
            "status": "completed",
            "winners": winners,
            "finalized_at": datetime.datetime.utcnow().isoformat()
        }).eq("id", gw_id).execute()
        logger.info(f"Çekiliş otomatik sonuçlandırıldı: {gw_id} → {len(winners)} kazanan")
    except Exception as e:
        logger.warning(f"Otomatik sonuçlandırma hatası: {e}")
        if winners:
            w1 = winners[0]
            supabase.table("giveaways").update({
                "status": "completed",
                "winner_username": w1["username"],
                "winner_instagram": w1["instagram"],
                "finalized_at": datetime.datetime.utcnow().isoformat()
            }).eq("id", gw_id).execute()

@app.route("/api/giveaways", methods=["GET"])
def api_giveaways_list():
    try:
        res = (
            supabase.table("giveaways")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )
        giveaways = res.data or []

        today = datetime.date.today().isoformat()
        needs_refresh = False
        for gw in giveaways:
            if gw.get("status") == "active" and gw.get("end_date") and gw["end_date"] < today:
                _auto_finalize(gw)
                needs_refresh = True

        if needs_refresh:
            res = (
                supabase.table("giveaways")
                .select("*")
                .order("created_at", desc=True)
                .execute()
            )
        return jsonify({"status": "ok", "data": res.data or []})
    except Exception as exc:
        logger.error("Çekiliş listeleme hatası: %s", exc)
        return jsonify({"status": "error", "message": "Çekilişler yüklenemedi."}), 500

@app.route("/api/giveaways/create", methods=["POST"])
def api_giveaways_create():
    current_user = _get_current_user()
    if not current_user:
        return jsonify({"status": "error", "message": "Giriş yapmalısınız."}), 401
    if not _is_admin(current_user):
        return jsonify({"status": "error", "message": "Yetkisiz işlem."}), 403

    data = request.get_json(force=True, silent=True) or {}
    title                  = html.escape(data.get("title", "").strip())
    prize                  = html.escape(data.get("prize", "").strip())
    description            = html.escape(data.get("description", "").strip())
    end_date               = data.get("end_date", "").strip()
    image_b64              = data.get("image_base64", "")
    winner_count           = max(1, int(data.get("winner_count", 1)))
    admin_pick_mode        = bool(data.get("admin_pick_mode", False))
    admin_picked_usernames = [u.strip() for u in data.get("admin_picked_usernames", []) if u.strip()]

    if not title or not prize or not end_date:
        return jsonify({"status": "error", "message": "Başlık, ödül ve tarih zorunludur."}), 400

    try:
        datetime.date.fromisoformat(end_date)
    except ValueError:
        return jsonify({"status": "error", "message": "Geçersiz tarih formatı."}), 400

    image_url = ""
    if image_b64.startswith("data:image"):
        try:
            uploaded = upload_base64_to_storage(image_b64, folder="giveaways")
            if uploaded and uploaded.startswith("http"):
                image_url = uploaded
            else:
                image_url = image_b64
        except Exception as e:
            logger.error("Giveaway resim yükleme hatası: %s", e)
            image_url = image_b64

    record = {
        "title": title,
        "prize": prize,
        "description": description,
        "image_url": image_url,
        "end_date": end_date,
        "status": "active",
        "participants": [],
        "winner_count": winner_count,
        "winners": [],
        "admin_pick_mode": admin_pick_mode,
        "admin_picked_usernames": admin_picked_usernames if admin_picked_usernames else None,
        "created_by": current_user,
        "created_at": datetime.datetime.utcnow().isoformat(),
    }

    try:
        supabase.table("giveaways").insert(record).execute()
        return jsonify({"status": "ok", "message": "Çekiliş oluşturuldu."})
    except Exception as exc:
        logger.error("Çekiliş oluşturma hatası: %s", exc)
        return jsonify({"status": "error", "message": "Çekiliş kaydedilemedi."}), 500

@app.route("/api/giveaways/<int:gw_id>/join", methods=["POST"])
def api_giveaways_join(gw_id):
    current_user = _get_current_user()
    if not current_user:
        return jsonify({"status": "error", "message": "Giriş yapmalısınız."}), 401

    data = request.get_json(force=True, silent=True) or {}
    instagram = html.escape(data.get("instagram", "").strip().lstrip("@"))

    if not instagram:
        return jsonify({"status": "error", "message": "Instagram zorunludur!"}), 400

    try:
        res = supabase.table("giveaways").select("status, end_date, participants").eq("id", gw_id).execute()
        if not res.data:
            return jsonify({"status": "error", "message": "Çekiliş bulunamadı."}), 404

        gw = res.data[0]
        if gw.get("status") != "active":
            return jsonify({"status": "error", "message": "Bu çekiliş aktif değil."}), 400

        today = datetime.date.today().isoformat()
        if gw.get("end_date") and gw["end_date"] < today:
            return jsonify({"status": "error", "message": "Bu çekilişin süresi dolmuş."}), 400

        participants = gw.get("participants") or []
        already_joined = any(
            (p.get("username") == current_user if isinstance(p, dict) else p == current_user)
            for p in participants
        )
        if already_joined:
            return jsonify({"status": "error", "message": "Zaten katıldınız."}), 400

        participants.append({"username": current_user, "instagram": instagram})
        supabase.table("giveaways").update({"participants": participants}).eq("id", gw_id).execute()
        return jsonify({"status": "ok", "message": "Çekilişe başarıyla katıldınız!"})
    except Exception as exc:
        logger.error("Katılım hatası: %s", exc)
        return jsonify({"status": "error", "message": "Bir hata oluştu."}), 500

@app.route("/api/giveaways/<int:gw_id>/finalize", methods=["POST"])
def api_giveaways_finalize(gw_id):
    current_user = _get_current_user()
    if not current_user or not _is_admin(current_user):
        return jsonify({"status": "error", "message": "Yetkisiz işlem."}), 403

    data = request.get_json(force=True, silent=True) or {}
    manual_winners = [u.strip() for u in data.get("manual_winners", []) if u.strip()]

    try:
        res = supabase.table("giveaways").select(
            "status, participants, winner_count, admin_pick_mode, admin_picked_usernames"
        ).eq("id", gw_id).execute()
        if not res.data:
            return jsonify({"status": "error", "message": "Çekiliş bulunamadı."}), 404

        gw = res.data[0]
        if gw.get("status") != "active":
            return jsonify({"status": "error", "message": "Çekiliş zaten sonuçlanmış."}), 400

        participants = gw.get("participants") or []
        winner_count = gw.get("winner_count") or 1
        admin_pick_mode = gw.get("admin_pick_mode") or False
        admin_picked_usernames = gw.get("admin_picked_usernames") or []

        if not participants:
            return jsonify({"status": "error", "message": "Katılımcı yok!"}), 400

        winners = []

        # Öncelik sırası:
        # 1. API'den gelen manual_winners (anlık override)
        # 2. admin_pick_mode=True ise kayıtlı admin_picked_usernames
        # 3. Rastgele
        sources = manual_winners or (admin_picked_usernames if admin_pick_mode else [])

        if sources:
            for uname in sources:
                for p in participants:
                    if isinstance(p, dict) and p.get("username") == uname:
                        winners.append({"username": p.get("username"), "instagram": p.get("instagram", "")})
                        break
                    elif p == uname:
                        winners.append({"username": p, "instagram": ""})
                        break

        if not winners:
            count_to_pick = min(winner_count, len(participants))
            selected_participants = random.sample(participants, count_to_pick)
            for p in selected_participants:
                if isinstance(p, dict):
                    winners.append({"username": p.get("username", ""), "instagram": p.get("instagram", "")})
                else:
                    winners.append({"username": str(p), "instagram": ""})

        if not winners:
            return jsonify({"status": "error", "message": "Geçerli kazanan bulunamadı."}), 400

        supabase.table("giveaways").update({
            "status": "completed",
            "winners": winners,
            "finalized_at": datetime.datetime.utcnow().isoformat()
        }).eq("id", gw_id).execute()

        winner_names = ", ".join([w["username"] for w in winners])
        return jsonify({
            "status": "ok",
            "winners": winners,
            "message": f"🏆 Kazananlar: {winner_names}!"
        })
    except Exception as exc:
        logger.error("Sonuçlandırma hatası: %s", exc)
        return jsonify({"status": "error", "message": "Hata oluştu."}), 500

@app.route("/api/giveaways/<int:gw_id>/delete", methods=["POST"])
def api_giveaways_delete(gw_id):
    current_user = _get_current_user()
    if not current_user or not _is_admin(current_user):
        return jsonify({"status": "error", "message": "Yetkisiz işlem."}), 403

    try:
        supabase.table("giveaways").delete().eq("id", gw_id).execute()
        return jsonify({"status": "ok", "message": "Çekiliş silindi."})
    except Exception as exc:
        logger.error("Çekiliş silme hatası: %s", exc)
        return jsonify({"status": "error", "message": "Silinemedi."}), 500
