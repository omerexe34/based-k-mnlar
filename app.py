"""
app.py
======
Ana giriş noktası.
Tüm modülleri doğru sırayla import eder; Flask uygulamasını başlatır.

Modül yükleme sırası (bağımlılık grafiğine göre):
  1. extensions      — Flask app, Supabase, R2, env vars
  2. rate_limiter    — Rate limit store (extensions'a bağımlı)
  3. notifications   — OneSignal, Miss-You worker (extensions + requests)
  4. storage         — R2 upload, base64 (extensions)
  5. ai              — Groq AI (extensions)
  6. database        — init_db, delete_user_assets (extensions + storage)
  7. iap             — Google Play IAP route (extensions)
  8. routes_pages    — Statik sayfalar, heartbeat, upload (extensions + storage + database)
  9a. routes_iap_web — Web/iOS satın alma talebi route'u
  9b. moderation     — AI moderasyon rotaları (/report_message, /admin/*)
  10. routes_api_data — /api/data route (extensions + tüm yardımcı modüller)
  11. html_template  — HTML_CODE string'i
"""

import os

# 1 — Temel bileşenler (Flask app, Supabase, R2)
from extensions import app, supabase, logger, ONESIGNAL_APP_ID, SUPABASE_URL, SUPABASE_KEY, SUPABASE_ANON_KEY

# 2 — Rate limiter (extensions'a bağımlı)
import rate_limiter  # noqa: F401 — yan etki: thread'i başlatır
from rate_limiter import rate_check

# 3 — Bildirimler + güvenlik başlıkları (extensions + rate_limiter)
import notifications  # noqa: F401 — yan etki: @after_request kaydı + worker thread

# 4 — Depolama yardımcıları
import storage  # noqa: F401

# 5 — AI yardımcıları
import ai  # noqa: F401

# 6 — Veritabanı yardımcıları + başlatma
from database import init_db
# init_db()  # Gunicorn boot timeout'a (30 sn) sebep olmaması için devre dışı bırakıldı

# 7 — Google Play IAP route
import iap  # noqa: F401 — yan etki: @app.route kaydı

# 8 — Statik sayfalar + yardımcı API route'ları
import routes_pages  # noqa: F401 — yan etki: @app.route kayıtları

# 8b — Mesaj raporlama: routes_api_data.py içindeki report_message action'ı kullanılıyor
# import routes_report  # KALDIRILDI — duplicate endpoint temizliği

# 9a — Web / iOS satın alma talebi route'u  ← ÖNCEKİ HATA: BU SATIR EKSİKTİ
import routes_iap_web  # noqa: F401 — yan etki: @app.route kaydı
import routes_cekilis  # noqa: F401 — yan etki: @app.route kaydı (çekiliş sistemi)

# 9b — AI Moderasyon sistemi
from moderation import register_moderation_routes
from notifications import send_push_to_user as _mod_push_fn
register_moderation_routes(app, supabase, logger, rate_check, push_fn=_mod_push_fn)

# 10 — Ana veri API'si
import routes_api_data  # noqa: F401 — yan etki: @app.route kaydı

# 11 — HTML şablonu (önbellekli)
from html_template import HTML_CODE

# ==============================================================================
# ANA SAYFA — Template Caching
# Jinja2 render_template_string her çağrıda template'i parse eder.
# Template bir kez render edilip cache'lenerek CPU tasarrufu sağlanır.
# ==============================================================================
from flask import render_template_string, make_response, jsonify
from markupsafe import Markup
import html_template

# HTML şablonu uygulama başlangıcında bir kez render edilip belleğe alınır.
# Her istekte 800KB dosyayı yeniden import etmek yerine hazır HTML döndürülür.
_CACHED_HTML: str | None = None

def _build_html_cache():
    global _CACHED_HTML
    _CACHED_HTML = render_template_string(
        html_template.HTML_CODE,
        onesignal_app_id=ONESIGNAL_APP_ID or "",
        supabase_url="https://freeridertr.com.tr/supabase-api",  # Frontend icin HTTPS proxy URL
        supabase_key=SUPABASE_ANON_KEY or "",
    )
    logger.info("HTML şablonu belleğe alındı (%d bayt).", len(_CACHED_HTML))

# Uygulama başlarken render et
with app.app_context():
    _build_html_cache()

@app.route("/")
def index():
    resp = make_response(_CACHED_HTML)
    resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    resp.headers['Pragma'] = 'no-cache'
    resp.headers['Expires'] = '0'
    return resp

@app.route("/reload-template", methods=["POST"])
def reload_template():
    """Sadece yetkili Admin tarafından çağrılabilir — HTML cache'i yeniler."""
    from flask import request as _req, session as _ses
    if _ses.get('role') != 'Admin' and _ses.get('username') != 'Admin':
        return jsonify({'status': 'error', 'message': 'Yetkisiz'}), 403
    _build_html_cache()
    return jsonify({'status': 'ok', 'message': 'HTML cache yenilendi.'})

# ==============================================================================
# TELEGRAM BOT BAŞLATICI
# ==============================================================================
try:
    import telegram_bot
    telegram_bot.start_bot_thread()
except Exception as e:
    from extensions import logger
    logger.error(f"Telegram bot başlatılamadı: {e}")

# ==============================================================================
# UYGULAMA BAŞLATICI
# ==============================================================================
if __name__ == "__main__":
    print("===================================================")
    print("💎 V7.0 FREERIDER PLUS (HAFTALIK YARIŞ & SOSYAL MEDYA EDITION)")
    print("🚀 SİSTEM CANLIYA HAZIR, BANDWIDTH OPTİMİZE EDİLDİ!")
    print("===================================================")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

