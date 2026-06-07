"""
routes_iap_web.py
=================
Web / iOS / tarayıcı üzerinden gelen satın alma talepleri.

Endpoint:
    POST /api/web_purchase_request

İşlev:
    1. Oturumu doğrular.
    2. Aynı talep aynı gün daha önce gönderilmişse duplikasyon önleme ile
       hata dönmeden sessizce "ok" döner (kullanıcı deneyimi bozulmaz).
    3. Admin kullanıcısını (role='admin' veya username='Admin') bulur.
    4. Supabase dms tablosuna otomatik DM ekler:
         "[Kullanıcı Adı] adlı kullanıcı [Üyelik Tipi] satın almak istiyor.
          Lütfen iletişime geçin."
    5. Admin'e OneSignal push bildirimi gönderir.
    6. Kullanıcının stats alanına talebin zamanını kaydeder
       (duplikasyon önleme için).
"""

import json
import time
import datetime
import html

from flask import request, jsonify, session

from extensions import app, supabase, logger
from notifications import send_push_to_user

# ==============================================================================
# ÜRÜN ID → OKUNABILIR AD EŞLEŞTİRMESİ
# iap.py'deki _IAP_PRODUCT_TIER_MAP ile senkronize tutun.
# ==============================================================================
_PRODUCT_DISPLAY_NAMES = {
    # Aktif abonelikler
    "freeridertr_ultra_pack_monthly":    "👑 Ultra+ Üyelik",
    "freeridertr_deluxe_pack_monthly":   "🌟 Deluxe Üyelik",
    "freeridertr_standard_pack_monthly": "⭐ Standart Üyelik",
    # Geçiş dönemi ürünleri
    "premium_standard_monthly": "⭐ Standart Üyelik",
    "premium_deluxe_monthly":   "🌟 Deluxe Üyelik",
    "premium_ultra_monthly":    "👑 Ultra+ Üyelik",
    # Geriye dönük uyumluluk
    "ultra_pack_1":    "👑 Ultra+ Üyelik",
    "deluxe_pack_1":   "🌟 Deluxe Üyelik",
    "standard_pack_1": "⭐ Standart Üyelik",
}

_COOLDOWN_HOURS = 24   # Aynı ürün için kaç saatte bir talep gönderilebilir


def _find_admin_username() -> str | None:
    """Supabase'de role='Admin' veya 'admin' olan ilk kullanıcıyı,
    bulamazsa username='Admin' kullanıcısını, o da yoksa None döner.
    NOT: login sistemi role değerini 'Admin' (büyük A) olarak kaydeder."""

    # Önce büyük harfle dene (sistemin kullandığı format)
    for role_val in ("Admin", "admin", "SubAdmin"):
        try:
            res = (
                supabase.table("users")
                .select("username")
                .eq("role", role_val)
                .limit(1)
                .execute()
            )
            if res.data:
                found = res.data[0]["username"]
                logger.info(f"_find_admin_username: '{found}' bulundu (role={role_val})")
                return found
        except Exception as exc:
            logger.warning(f"_find_admin_username: role='{role_val}' sorgusu başarısız: {exc}")

    # Son çare: sabit 'Admin' kullanıcı adı
    try:
        res2 = (
            supabase.table("users")
            .select("username")
            .eq("username", "Admin")
            .limit(1)
            .execute()
        )
        if res2.data:
            logger.info("_find_admin_username: 'Admin' kullanıcısı username eşleşmesiyle bulundu.")
            return res2.data[0]["username"]
    except Exception as exc:
        logger.warning(f"_find_admin_username: 'Admin' sorgusu başarısız: {exc}")

    return None


# ==============================================================================
# ENDPOINT
# ==============================================================================
@app.route("/api/web_purchase_request", methods=["POST"])
def web_purchase_request():
    """
    Beklenen JSON gövdesi:
        { "productId": "freeridertr_ultra_pack_monthly" }

    Dönüş:
        { "status": "ok",   "message": "Talebiniz iletildi." }
        { "status": "wait", "message": "Daha önce talep gönderdiniz. Lütfen bekleyin." }
        { "status": "error","message": "<açıklama>" }
    """
    if "username" not in session or not supabase:
        return jsonify({"status": "error", "message": "Oturum açılmamış."}), 401

    current_username = session["username"]

    body       = request.get_json(silent=True) or {}
    product_id = (body.get("productId") or "").strip()

    if not product_id:
        return jsonify({"status": "error", "message": "Ürün ID eksik."}), 400

    product_label = _PRODUCT_DISPLAY_NAMES.get(product_id, product_id)

    # ── 1. Duplikasyon kontrolü ────────────────────────────────────────────────
    try:
        u_res = (
            supabase.table("users")
            .select("stats")
            .eq("username", current_username)
            .execute()
        )
        if not u_res.data:
            return jsonify({"status": "error", "message": "Kullanıcı bulunamadı."}), 404

        stats = u_res.data[0].get("stats", {}) or {}
        if isinstance(stats, str):
            try:
                stats = json.loads(stats)
            except json.JSONDecodeError:
                stats = {}

        now_ts       = int(time.time())
        purchase_reqs = stats.get("web_purchase_requests", {})

        if isinstance(purchase_reqs, dict):
            last_ts = int(purchase_reqs.get(product_id, 0))
            elapsed_h = (now_ts - last_ts) / 3600
            if elapsed_h < _COOLDOWN_HOURS:
                remaining_h = int(_COOLDOWN_HOURS - elapsed_h) + 1
                return jsonify({
                    "status":  "wait",
                    "message": (
                        f"Bu ürün için zaten bir talep ilettiniz. "
                        f"Yönetici sizinle iletişime geçecek. "
                        f"(Tekrar talep için yaklaşık {remaining_h} saat bekleyin.)"
                    ),
                })

    except Exception as exc:
        logger.error(
            f"web_purchase_request: stats okuma hatası ({current_username}): {exc}",
            exc_info=True,
        )
        return jsonify({"status": "error", "message": "Sunucu hatası, lütfen tekrar deneyin."}), 500

    # ── 2. Admin'i bul ─────────────────────────────────────────────────────────
    admin_username = _find_admin_username()
    if not admin_username:
        logger.error("web_purchase_request: Admin kullanıcısı bulunamadı!")
        return jsonify({"status": "error", "message": "Yönetici bulunamadı, lütfen destek ile iletişime geçin."}), 500

    # ── 3. Admin'e DM gönder ───────────────────────────────────────────────────
    dm_text = (
        f"💳 [SATIN ALMA TALEBİ]\n"
        f"Kullanıcı: {current_username}\n"
        f"Ürün: {product_label}\n"
        f"Zaman: {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
        f"Lütfen kullanıcıyla iletişime geçin."
    )
    try:
        dm_id = str(int(time.time() * 1000))
        supabase.table("dms").insert({
            "id":           dm_id,
            "sender":       current_username,
            "receiver":     admin_username,
            "participants": [current_username, admin_username],
            "text":         dm_text,
            "type":         "text",
            "ts":           int(time.time() * 1000),  # milisaniye timestamp
        }).execute()
        logger.info(
            f"web_purchase_request: DM gönderildi "
            f"({current_username} → {admin_username}, ürün: {product_id})"
        )
    except Exception as exc:
        logger.error(
            f"web_purchase_request: DM insert hatası ({current_username}): {exc}",
            exc_info=True,
        )
        return jsonify({"status": "error", "message": "Talep gönderilemedi, tekrar deneyin."}), 500

    # ── 4. Admin'e push bildirimi gönder ───────────────────────────────────────
    try:
        send_push_to_user(
            admin_username,
            title=f"💳 Satın Alma Talebi: {current_username}",
            body=f"{current_username} → {product_label} satın almak istiyor.",
            url="/",
        )
    except Exception as exc:
        logger.warning(f"web_purchase_request: push bildirimi gönderilemedi: {exc}")

    # ── 5. Stats'a talep zamanını kaydet (duplikasyon önleme) ─────────────────
    try:
        if not isinstance(purchase_reqs, dict):
            purchase_reqs = {}
        purchase_reqs[product_id] = now_ts
        stats["web_purchase_requests"] = purchase_reqs
        supabase.table("users").update({"stats": stats}).eq("username", current_username).execute()
    except Exception as exc:
        # Kritik değil — kayıt başarısız olsa da kullanıcıya ok dön
        logger.warning(f"web_purchase_request: stats güncelleme hatası: {exc}")

    return jsonify({
        "status":  "ok",
        "message": (
            "Talebiniz yöneticiye iletildi! 🎉\n"
            "En kısa sürede sizinle iletişime geçilecek."
        ),
    })
