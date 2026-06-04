"""
notifications.py
================
OneSignal push bildirimleri, 'Seni Özledik' arka plan işçisi
ve güvenlik başlıkları (security headers) burada tanımlanır.

Optimizasyonlar:
  - Player ID TTL cache (5 dk) — aynı kullanıcıya kısa sürede birçok
    bildirim gönderilirken DB sorgusu tekrarlanmaz
"""

import json
import time
import random
import threading
import requests

from extensions import (
    app, supabase, logger,
    ONESIGNAL_APP_ID, ONESIGNAL_API_KEY, ONESIGNAL_API_URL,
)
from cache import app_cache

# ==============================================================================
# GÜVENLİK BAŞLIKLARI (Security Headers)
# ==============================================================================
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options']  = 'nosniff'
    response.headers['X-Frame-Options']         = 'SAMEORIGIN'
    response.headers['X-XSS-Protection']        = '1; mode=block'
    response.headers['Referrer-Policy']         = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy']      = 'geolocation=(self), microphone=(self), camera=(self)'
    if not app.debug:
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

# ==============================================================================
# SENİ ÖZLEDİK BİLDİRİM SİSTEMİ
# Her 30 dakikada kontrol: 10+ saat girmeyen kullanıcılara özel bildirim
# ==============================================================================
_MISS_YOU_MESSAGES = [
    ("😢 Seni özledik {name}!", "FreeriderTR topluluğu seni bekliyor. Bugün bir rota paylaş! 🏔️"),
    ("🏔️ {name}, rotalar seni çağırıyor!", "Uzun süredir ortalarda yoksun. Bugün ne sürüyorsun?"),
    ("🚴 {name} neredesin?", "Topluluk aktif! Yeni rampalar, buluşmalar ve sohbetler seni bekliyor."),
    ("⚡ {name}, günlük çarkını çevirmek istemez misin?", "Bugün ödüllü çark çevirme hakkın var! Kaçırma 🎡"),
    ("🏆 {name}, sıralamada yerinizi koruyun!", "Liderlik tablosunda aktif olmak XP kazandırır. Geri dön!"),
    ("🔥 {name}, yeni içerikler seni bekliyor!", "Reels, haberler ve yeni harita noktaları eklendi."),
    ("💬 {name}, sohbet kaçırıyorsun!", "Topluluk konuşuyor. Sen de katıl, fikrin önemli!"),
    ("🎯 {name}, görevlerin süresi doluyor!", "Tamamlanmamış görevlerin var. XP kazanmak için geri dön."),
    ("📍 {name}, yeni rampalar eklendi!", "Haritada yeni keşfedilmemiş noktalar var. İncele!"),
    ("👑 {name}, senin döndüğünü merak edenler var!", "Topluluğun en değerli üyelerinden birisin. Dön!"),
]

_CHAT_BROADCAST_LOCK = threading.Lock()
_last_chat_broadcast_ts = 0   # son grup chat broadcastinin zamanı
CHAT_BROADCAST_COOLDOWN = 600  # 10 dakika bekleme süresi (kullanıcı talebi)

import os
import tempfile

_CHAT_BROADCAST_FILE = os.path.join(tempfile.gettempdir(), "fr_chat_broadcast.txt")

def _can_broadcast_chat():
    """Grup chat bildirimi için flood kontrolü (10 dk cooldown), çoklu worker uyumlu."""
    global _last_chat_broadcast_ts
    now = time.time()
    
    with _CHAT_BROADCAST_LOCK:
        try:
            last_ts = 0
            if os.path.exists(_CHAT_BROADCAST_FILE):
                with open(_CHAT_BROADCAST_FILE, "r") as f:
                    content = f.read().strip()
                    if content:
                        last_ts = float(content)
            
            if now - last_ts >= CHAT_BROADCAST_COOLDOWN:
                with open(_CHAT_BROADCAST_FILE, "w") as f:
                    f.write(str(now))
                return True
        except Exception as e:
            # Hata olursa eski global değişkeni yedek olarak kullan
            if now - _last_chat_broadcast_ts >= CHAT_BROADCAST_COOLDOWN:
                _last_chat_broadcast_ts = now
                return True
                
    return False

def _miss_you_worker():
    """Her 30 dakikada 10–11 saat önce görülen kullanıcılara bildirim gönderir.
    Supabase JSONB filtresiyle yalnızca ilgili satırlar çekilir — tam tablo taraması yapılmaz."""
    while True:
        time.sleep(1800)  # 30 dakika bekle
        if not supabase:
            continue
        try:
            now_ts       = int(time.time())
            ten_h_ago    = now_ts - 36000   # 10 saat
            eleven_h_ago = now_ts - 39600   # 11 saat


            try:
                res = (
                    supabase.table("users")
                    .select("username, name, stats")
                    .filter("stats->>last_seen_ts", "gte", str(eleven_h_ago))
                    .filter("stats->>last_seen_ts", "lte", str(ten_h_ago))
                    .execute()
                )
                candidates = res.data or []
            except Exception as exc:
                logger.warning(f"Miss-you JSONB filtre hatası, çalıştırma atlandı: {exc}")
                continue

            sent_count = 0
            for u in candidates:
                try:
                    uname         = u.get("username", "")
                    uname_display = (u.get("name") or uname)[:20]
                    st = u.get("stats") or {}
                    if isinstance(st, str):
                        try:
                            st = json.loads(st)
                        except json.JSONDecodeError:
                            st = {}

                    last_miss = st.get("last_miss_notif_ts", 0)
                    if now_ts - last_miss < 86400:  # 24 saat henüz geçmedi
                        continue

                    title_tpl, body_tpl = random.choice(_MISS_YOU_MESSAGES)
                    send_push_to_user(
                        uname,
                        title=title_tpl.format(name=uname_display),
                        body=body_tpl,
                        url="/",
                    )
                    st["last_miss_notif_ts"] = now_ts
                    supabase.table("users").update({"stats": st}).eq("username", uname).execute()
                    sent_count += 1
                    time.sleep(0.1)  # API rate limit
                except Exception as exc:
                    logger.warning(f"Miss-you tekil gönderim hatası ({u.get('username','?')}): {exc}", exc_info=True)

            if sent_count:
                logger.info(f"Seni ozledik: {sent_count} kullaniciya bildirim gonderildi.")
        except Exception as exc:
            logger.error(f"Miss-you worker beklenmedik hata: {exc}", exc_info=True)

threading.Thread(target=_miss_you_worker, daemon=True).start()
print("'Seni Ozledik' bildirim sistemi baslatildi")

# ==============================================================================
# BİLDİRİM HATA LOGLAMA (Admin Panelinde Görünsün Diye)
# ==============================================================================
def _log_notification_error(provider: str, target: str, error_msg: str):
    """Bildirim hatalarını admin_logs tablosuna kaydeder ki VDS terminaline bakmaya gerek kalmasın."""
    if not supabase: return
    try:
        err_id = str(int(time.time() * 1000)) + f"_{provider[:3]}"
        supabase.table('admin_logs').insert({
            "id": err_id,
            "admin": "Sistem",
            "action": f"{provider}_error",
            "target": target,
            "detail": f"{provider} Hatası: {str(error_msg)[:200]}",
            "ts": int(time.time())
        }).execute()
    except Exception as e:
        print(f"Loglama hatası: {e}")

# ==============================================================================
# ONESIGNAL PUSH BİLDİRİM FONKSİYONLARI
# ==============================================================================
def _onesignal_send(payload: dict, target_label: str = "Bilinmeyen"):
    """OneSignal REST API'ye bildirim gönderir ve hataları veritabanına yazar."""
    if not ONESIGNAL_API_KEY or not ONESIGNAL_APP_ID:
        print("[UYARI] OneSignal bildirimi gönderilemedi: .env dosyasında ONESIGNAL_API_KEY veya APP_ID eksik!")
        _log_notification_error("OneSignal", target_label, "ONESIGNAL_API_KEY veya APP_ID eksik (.env kontrol et)")
        return

    def _do_send():
        url = "https://onesignal.com/api/v1/notifications"
        auth_header = f"Key {ONESIGNAL_API_KEY}"
        headers = {
            "Authorization": auth_header,
            "Content-Type": "application/json",
            "accept": "application/json"
        }

        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=10)
            result = resp.json() if resp.text else {}
            if resp.status_code in (200, 202):
                if result.get('errors'):
                    err_str = str(result.get('errors'))
                    if "All included players are not subscribed" in err_str:
                        # Bu normal bir durumdur (Kullanıcı henüz abone olmamış veya izinleri kapatmış)
                        print(f"[BİLGİ] OneSignal: Kullanıcı ({target_label}) henüz abone değil veya bildirimleri kapalı.")
                    else:
                        print(f"[HATA] OneSignal API Hatası ({target_label}): {err_str}")
                        _log_notification_error("OneSignal", target_label, err_str)
                else:
                    print(f"[BAŞARILI] OneSignal gönderildi | Hedef: {target_label} | Alıcı Sayısı: {result.get('recipients', 0)}")
            else:
                err_str = f"HTTP {resp.status_code}: {resp.text[:200]}"
                print(f"[HATA] OneSignal Bağlantı Hatası: {err_str}")
                _log_notification_error("OneSignal", target_label, err_str)
        except Exception as e:
            print(f"[HATA] OneSignal İstek Hatası: {e}")
            _log_notification_error("OneSignal", target_label, f"İstek zaman aşımı veya bağlantı kopukluğu: {str(e)}")
            
    threading.Thread(target=_do_send, daemon=True).start()

def _get_player_id(username: str) -> str | None:
    """Kullanıcının OneSignal player_id'sini cache'li şekilde döner."""
    cache_key = f"pid:{username}"
    cached = app_cache.get(cache_key)
    if cached is not None:
        return cached if cached != "" else None

    player_id = None
    if supabase:
        try:
            u = supabase.table('users').select('stats').eq('username', username).execute()
            if u.data:
                st = u.data[0].get('stats', {}) or {}
                if isinstance(st, str):
                    try: st = json.loads(st)
                    except: st = {}
                player_id = st.get('onesignal_player_id')
        except Exception as exc:
            logger.warning(f'Player ID sorgu hatası [{username}]: {exc}')

    app_cache.set(cache_key, player_id or "", ttl=300)
    return player_id

import os
import base64
from google.oauth2 import service_account
from google.auth.transport.requests import Request

# FCM Token Cache Access Method
def _get_fcm_token(username: str) -> str | None:
    cache_key = f"fcm:{username}"
    cached = app_cache.get(cache_key)
    if cached is not None:
        return cached if cached != "" else None

    fcm_token = None
    if supabase:
        try:
            u = supabase.table('users').select('stats').eq('username', username).execute()
            if u.data:
                st = u.data[0].get('stats', {}) or {}
                if isinstance(st, str):
                    try: st = json.loads(st)
                    except: st = {}
                fcm_token = st.get('fcm_token')
        except Exception as exc:
            logger.warning(f'FCM Token sorgu hatası [{username}]: {exc}')

    app_cache.set(cache_key, fcm_token or "", ttl=300)
    return fcm_token

def _fcm_send(token: str, title: str, body: str, url: str, username: str = "Bilinmeyen"):
    """Firebase Cloud Messaging (FCM) v1 API ile doğrudan bildirim gönderir."""
    def _do_send():
        try:
            cred_str = os.getenv('GOOGLE_CREDENTIALS_JSON')
            if not cred_str:
                print("[UYARI] Firebase bildirimi gönderilemedi: .env dosyasında GOOGLE_CREDENTIALS_JSON eksik!")
                _log_notification_error("Firebase", username, "GOOGLE_CREDENTIALS_JSON eksik (.env kontrol et)")
                return
            
            decoded = base64.b64decode(cred_str).decode('utf-8')
            creds_dict = json.loads(decoded)
            project_id = creds_dict.get("project_id")
            if not project_id:
                return

            creds = service_account.Credentials.from_service_account_info(
                creds_dict, scopes=['https://www.googleapis.com/auth/firebase.messaging']
            )
            creds.refresh(Request())
            access_token = creds.token

            fcm_url = f"https://fcm.googleapis.com/v1/projects/{project_id}/messages:send"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            }
            
            payload = {
                "message": {
                    "token": token,
                    "notification": {
                        "title": title,
                        "body": body,
                        "image": "https://cdn.freeridertr.com.tr/bildirim%20resmi/photo_5825636358775573905_y%20(1).jpg"
                    },
                    "android": {
                        "notification": {
                            "image": "https://cdn.freeridertr.com.tr/bildirim%20resmi/photo_5825636358775573905_y%20(1).jpg"
                        }
                    },
                    "data": {
                        "title": title,
                        "body": body,
                        "url": url,
                        "type": "personal",
                        "deep_link": f"https://freeridertr.com.tr{url}"
                    }
                }
            }

            resp = requests.post(fcm_url, json=payload, headers=headers, timeout=10)
            if resp.status_code == 200:
                print(f"[BAŞARILI] FCM bildirim gönderildi | Hedef: {username}")
            else:
                err_str = f"HTTP {resp.status_code}: {resp.text[:200]}"
                print(f"[HATA] FCM Gönderim Hatası ({username}): {err_str}")
                # "SenderId mismatch" gibi hataları kaydetmek çok önemli
                _log_notification_error("Firebase", username, err_str)
        except Exception as e:
            print(f"[HATA] FCM İstek Hatası: {e}")
            _log_notification_error("Firebase", username, f"Firebase API ulaşılamıyor: {str(e)}")
            
    threading.Thread(target=_do_send, daemon=True).start()

def send_push_to_user(username, title, body, url="/"):
    """Belirli bir kullanıcıya bildirim gönderir. (FCM + OneSignal destekli)"""
    # Anti-Spam (Aynı kişiye arka arkaya bildirim gitmesin - 3 dakika arayla)
    spam_key = f"notif_spam:{username}"
    if app_cache.get(spam_key):
        print(f"[Anti-Spam] {username} için bildirim engellendi (3 dk cooldown).")
        return
    app_cache.set(spam_key, True, ttl=180)

    # 1. Android Native için Firebase Cloud Messaging (FCM)
    # FCM en güveniliri olduğundan öncelikli olarak gönderiyoruz
    fcm_token = _get_fcm_token(username)
    if fcm_token:
        _fcm_send(fcm_token, title, body, url, username=username)

    # 2. PC/Web Tarayıcıları ve eski sürüm Androidler için OneSignal
    # Kullanıcının Player ID'sini (tarayıcı push ID'si) kontrol et
    player_id = _get_player_id(username)

    base_payload = {
        "app_id": ONESIGNAL_APP_ID,


        "headings": {"en": title, "tr": title},
        "contents": {"en": body, "tr": body},
        "web_url": f"https://freeridertr.com.tr{url}",
        "app_url": f"https://freeridertr.com.tr{url}",
        "large_icon": "https://cdn.freeridertr.com.tr/bildirim%20resmi/photo_5825636358775573905_y%20(1).jpg",
        "chrome_web_icon": "https://cdn.freeridertr.com.tr/bildirim%20resmi/photo_5825636358775573905_y%20(1).jpg",
        "data": {"deep_link": f"https://freeridertr.com.tr{url}", "url": url},
    }

    # Hedef kitle oluştur
    if player_id:
        # Eğer Player ID varsa nokta atışı gönder (en garantisi)
        payload_web = dict(base_payload)
        payload_web["include_player_ids"] = [player_id]
        _onesignal_send(payload_web, target_label=f"{username} (PlayerID)")
    
    # External ID ile de gönder (Web Push Player ID alamadıysa veya mobil OneSignal kullanıyorsa)
    payload_legacy = dict(base_payload)
    payload_legacy["include_external_user_ids"] = [username]
    payload_legacy["channel_for_external_user_ids"] = "push"
    _onesignal_send(payload_legacy, target_label=f"{username} (ExternalID)")

def broadcast_push(title, body, exclude_user=None, url="/"):
    """Tüm kullanıcılara (veya belirli biri hariç) OneSignal üzerinden bildirim gönderir."""
    # Kısa süreli Global Anti-Spam koruması (flood engeli - 10 dakikada en fazla 1 genel bildirim)
    spam_file = os.path.join(tempfile.gettempdir(), "fr_global_broadcast.txt")
    now = time.time()
    try:
        if os.path.exists(spam_file):
            with open(spam_file, "r") as f:
                content = f.read().strip()
                last_ts = float(content) if content else 0
            if now - last_ts < 600:
                print(f"[Anti-Spam] Global bildirim engellendi (10 dk cooldown aktif). Denenen: '{title}'")
                return
        with open(spam_file, "w") as f:
            f.write(str(now))
    except Exception as e:
        # Hata olursa bellek içi cache kullan
        spam_key = "notif_spam:global_broadcast"
        if app_cache.get(spam_key):
            print(f"[Anti-Spam] Global bildirim engellendi (10 dk cooldown aktif). Denenen: '{title}'")
            return
        app_cache.set(spam_key, True, ttl=600)

    payload = {
        "app_id": ONESIGNAL_APP_ID,


        "included_segments": ["Subscribed Users", "Total Subscriptions", "Active Users"],
        "target_channel": "push",
        "headings": {"en": title, "tr": title},
        "contents": {"en": body, "tr": body},
        "web_url": f"https://freeridertr.com.tr{url}",
        "app_url": f"https://freeridertr.com.tr{url}",
        "large_icon": "https://cdn.freeridertr.com.tr/bildirim%20resmi/photo_5825636358775573905_y%20(1).jpg",
        "chrome_web_icon": "https://cdn.freeridertr.com.tr/bildirim%20resmi/photo_5825636358775573905_y%20(1).jpg",
        "data": {"deep_link": f"https://freeridertr.com.tr{url}", "url": url},
        "web_push_topic": "freeridertr_broadcast"
    }
    
    # if exclude_user:
    #     payload["excluded_aliases"] = {"external_id": [exclude_user]}
        
    _onesignal_send(payload, target_label="Global (Herkes)")



