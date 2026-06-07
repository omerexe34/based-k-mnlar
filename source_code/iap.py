"""
iap.py
======
Google Play In-App Purchase (IAP) doğrulama.
/api/verify_google_purchase endpoint'i burada tanımlanır.
"""

import os
import json
import datetime

from flask import request, jsonify, session

from extensions import (
    app, supabase, logger,
    GOOGLE_PLAY_PACKAGE_NAME,
    GOOGLE_API_AVAILABLE,
)

# Load fallback base64 credential
try:
    import google_play_key
except ImportError:
    pass

# Koşullu import — extensions.py'de zaten denendi, burada tekrar import etmiyoruz
try:
    import google.oauth2.service_account as gsa
    from googleapiclient.discovery import build as gapi_build
except ImportError:
    gsa = None
    gapi_build = None

# ==============================================================================
# GOOGLE PLAY IN-APP PURCHASE (IAP) YAPILANDIRMASI
# Servis hesabı anahtarı ASLA koda gömülmez; GOOGLE_APPLICATION_CREDENTIALS
# environment variable üzerinden okunur (dosya yolu olarak tanımlanır).
# ==============================================================================
def _get_google_play_service():
    """Google Play Developer API servis nesnesini döndürür.
    Önce GOOGLE_CREDENTIALS_JSON (JSON string/Base64) sonra GOOGLE_APPLICATION_CREDENTIALS (dosya yolu) dener.
    Başarısızlık durumunda None döner ve hata loglanır."""
    if not GOOGLE_API_AVAILABLE:
        logger.error("Google API kütüphaneleri yüklü değil.")
        return None
    try:
        creds_json = os.environ.get("GOOGLE_CREDENTIALS_JSON")
        if creds_json:
            creds_json = creds_json.strip().strip("'\"")
            
            # base64 decode if needed (avoids Render newline escaping issues)
            if not creds_json.startswith("{"):
                try:
                    import base64
                    decoded = base64.b64decode(creds_json).decode("utf-8")
                    if decoded.strip().startswith("{"):
                        creds_json = decoded.strip()
                except Exception as b64_err:
                    logger.warning(f"GOOGLE_CREDENTIALS_JSON base64 decode denemesi basarisiz: {b64_err}")
            
            info = json.loads(creds_json)
            
            # Clean private_key format
            if "private_key" in info:
                pk = info["private_key"]
                # Replace literal \n (backslash + n) with actual newline characters
                pk = pk.replace("\\n", "\n")
                
                # Check for space-replaced newlines
                header = "-----BEGIN PRIVATE KEY-----"
                footer = "-----END PRIVATE KEY-----"
                if header in pk and footer in pk:
                    parts = pk.split(header)[1].split(footer)
                    body = parts[0].strip()
                    if "\n" not in body and " " in body:
                        body = body.replace(" ", "\n")
                    pk = f"{header}\n{body}\n{footer}\n"
                
                info["private_key"] = pk

            credentials = gsa.Credentials.from_service_account_info(
                info,
                scopes=["https://www.googleapis.com/auth/androidpublisher"],
            )
        else:
            creds_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
            if not creds_path:
                logger.error("Ne GOOGLE_CREDENTIALS_JSON ne de GOOGLE_APPLICATION_CREDENTIALS tanımlı.")
                return None
            credentials = gsa.Credentials.from_service_account_file(
                creds_path,
                scopes=["https://www.googleapis.com/auth/androidpublisher"],
            )
        service = gapi_build("androidpublisher", "v3", credentials=credentials)
        return service
    except Exception as exc:
        logger.error(f"Google Play servis nesnesi oluşturulamadı: {exc}", exc_info=True)
        return None

# Ürün kimliği → premium tier eşleştirmesi
_IAP_PRODUCT_TIER_MAP = {
    # ── AKTİF: Abonelik (Subscription) ürünleri — Play Console ID'leri ile BİREBİR AYNI ──
    "freeridertr_ultra_pack_monthly":    3,  # 👑 Ultra+  (Tier 3) — aylık abonelik
    "freeridertr_deluxe_pack_monthly":   2,  # 🌟 Deluxe  (Tier 2) — aylık abonelik
    "freeridertr_standard_pack_monthly": 1,  # ⭐ Standart(Tier 1) — aylık abonelik

    # ── ESKİ / YEDEK: Geçiş dönemi ürünleri — aktif kullanıcı varsa tutulmalı ──
    "premium_standard_monthly": 1,
    "premium_deluxe_monthly":   2,
    "premium_ultra_monthly":    3,

    # ── GERİYE DÖNÜK UYUMLULUK: Eski tek seferlik (inapp) ürünler ────────
    "ultra_pack_1":    3,
    "deluxe_pack_1":   2,
    "standard_pack_1": 1,
}

@app.route("/api/verify_google_purchase", methods=["POST"])
def verify_google_purchase():
    """Google Play IAP satın alım token'ını backend'de doğrular ve
    kullanıcının premium seviyesini günceller.

    Beklenen JSON gövdesi:
        {
            "purchaseToken": "<Google'dan gelen token>",
            "productId":     "<Google Play ürün ID'si>",
            "purchaseType":  "subscription" | "inapp"   (opsiyonel)
        }
    """
    if "username" not in session or not supabase:
        return jsonify({"status": "error", "message": "Oturum açılmamış."}), 401

    current_username = session["username"]

    data = request.get_json(silent=True) or {}
    purchase_token = (data.get("purchaseToken") or "").strip()
    product_id     = (data.get("productId")     or "").strip()
    purchase_type  = (data.get("purchaseType")  or "subscription").strip().lower()
    is_restore     = data.get("isRestore", False)
    
    if purchase_type != "subscription":
        logger.warning(
            f"verify_google_purchase: purchaseType='{purchase_type}' alındı; "
            f"tüm paketler aboneliğe dönüştürüldüğünden 'subscription' olarak işleniyor."
        )
        purchase_type = "subscription"

    if not purchase_token or not product_id:
        logger.warning(f"verify_google_purchase: Eksik parametre ({current_username})")
        return jsonify({"status": "error", "message": "purchaseToken ve productId zorunludur."}), 400

    tier = _IAP_PRODUCT_TIER_MAP.get(product_id)
    if tier is None:
        logger.warning(f"verify_google_purchase: Bilinmeyen ürün ID → {product_id}")
        return jsonify({"status": "error", "message": "Geçersiz ürün ID."}), 400

    if not GOOGLE_PLAY_PACKAGE_NAME:
        logger.error("verify_google_purchase: GOOGLE_PLAY_PACKAGE_NAME tanımlı değil.")
        return jsonify({"status": "error", "message": "Sunucu yapılandırma hatası."}), 500

    expiry_ts = None
    try:
        u_res = supabase.table("users").select("*").eq("username", current_username).execute()
        if not u_res.data:
            return jsonify({"status": "error", "message": "Kullanıcı bulunamadı."}), 404
            
        stats = u_res.data[0].get("stats", {}) or {}
        if isinstance(stats, str):
            try: stats = json.loads(stats)
            except json.JSONDecodeError: stats = {}
            
        # Admin tarafından engellendiyse ve bu otomatik restore ise, Google Play'in aboneliği restore etmesini reddet
        if stats.get('gp_admin_revoked') and is_restore:
            logger.warning(f"verify_google_purchase: {current_username} için abonelik admin tarafından engellenmiş. Restore reddedildi.")
            return jsonify({"status": "error", "message": "Abonelik yönetici tarafından engellenmiş."}), 403
            
    except Exception as e:
        return jsonify({"status": "error", "message": "Kullanıcı verisi alınamadı."}), 500

    service = _get_google_play_service()
    if service is None:
        logger.error(
            f"verify_google_purchase: Google Play API kullanılamıyor ({current_username})"
        )
        return jsonify({
            "status": "error",
            "message": "Google API Servis Hesabı ayarlanmamış veya kimlik doğrulanamadı."
        }), 503
    else:
        try:
            result = (
                service.purchases()
                .subscriptions()
                .get(
                    packageName=GOOGLE_PLAY_PACKAGE_NAME,
                    subscriptionId=product_id,
                    token=purchase_token,
                )
                .execute()
            )
            payment_state = result.get("paymentState", 0)
            if payment_state not in (1, 2):
                logger.warning(
                    f"verify_google_purchase: Ödeme durumu geçersiz "
                    f"(paymentState={payment_state}, kullanıcı={current_username})"
                )
                return jsonify({"status": "error", "message": "Ödeme henüz tamamlanmamış."}), 402
            expiry_ms = int(result.get("expiryTimeMillis", 0))
            expiry_ts = expiry_ms // 1000 if expiry_ms else None
            logger.info(f"verify_google_purchase: API doğrulaması başarılı ({current_username})")
        except Exception as exc:
            logger.error(
                f"verify_google_purchase: Google Play API doğrulama hatası ({current_username}): {exc}",
                exc_info=True,
            )
            return jsonify({
                "status": "error",
                "message": f"Google Play Hatası: {str(exc)}"
            }), 503

    # ── Kullanıcı premium statüsünü Supabase'de güncelle ───────────────────
    try:
        # u_res ve stats zaten yukarıda alındı

        stats["premium_tier"]   = tier
        stats.pop("pending_premium", None)
        stats.pop("gp_admin_revoked", None)  # Yeni ödeme alındığı/onaylandığı için engeli kaldır

        if not stats.get("premium_color"):
            color_map = {1: "std-blue", 2: "dlx-blue", 3: "ult-gold"}
            stats["premium_color"] = color_map.get(tier, "std-blue")

        if expiry_ts:
            stats["expiry_ts"]           = expiry_ts
            exp_dt                       = datetime.datetime.fromtimestamp(expiry_ts)
            stats["premium_expire_date"] = exp_dt.strftime("%Y-%m-%d")
        else:
            stats.pop("expiry_ts", None)
            stats.pop("premium_expire_date", None)

        stats["gp_purchase_token"] = purchase_token
        stats["gp_product_id"]     = product_id

        supabase.table("users").update({"stats": stats}).eq("username", current_username).execute()
        logger.info(
            f"✅ Google Play IAP doğrulandı: {current_username} → tier {tier} "
            f"(bitiş: {stats.get('premium_expire_date', 'belirsiz')})"
        )
    except Exception as exc:
        logger.error(
            f"verify_google_purchase: Supabase güncelleme hatası ({current_username}): {exc}",
            exc_info=True,
        )
        return jsonify({"status": "error", "message": "Kullanıcı güncellenemedi."}), 500

    updated_user = u_res.data[0]
    updated_user["stats"] = stats

    return jsonify({
        "status":  "ok",
        "tier":    tier,
        "expiry":  stats.get("premium_expire_date"),
        "message": "Satın alım başarıyla doğrulandı.",
        "user":    updated_user
    })
