"""
routes_pages.py
===============
Statik sayfalar, servis worker, manifest, hesap silme,
heartbeat, push ID kaydetme ve binary dosya yükleme route'ları.
"""

import os
import json
import time
import uuid

from flask import request, jsonify, session, Response
import tempfile

from extensions import app, supabase, r2_client, logger, R2_BUCKET_NAME, R2_PUBLIC_URL
from storage import _VIDEO_EXT_MAP, upload_binary_to_storage
from database import delete_user_assets
from cache import app_cache

# ==============================================================================
# HEARTBEAT — Üyelik bitiş kontrolü
# ==============================================================================
@app.route("/api/heartbeat", methods=["POST"])
def heartbeat():
    if 'username' not in session or not supabase:
        return jsonify({'status': 'error'}), 401
    username = session['username']
    revoked = False
    try:
        now_ts = int(time.time())
        u_res = supabase.table('users').select('stats').eq('username', username).execute()
        if u_res.data:
            stats = u_res.data[0].get('stats', {}) or {}
            if isinstance(stats, str):
                try: stats = json.loads(stats)
                except: stats = {}
            stats['last_seen_ts'] = now_ts

            expiry_ts = stats.get('expiry_ts')
            if expiry_ts and int(stats.get('premium_tier', 0)) > 0:
                if now_ts >= int(expiry_ts):
                    was_trial = stats.get('is_trial', False)
                    stats['premium_tier'] = 0
                    stats['premium_color'] = ''
                    stats.pop('premium_expire_date', None)
                    stats.pop('expiry_ts', None)
                    stats.pop('weekly_reward_active', None)
                    stats.pop('monthly_reward_active', None)
                    if was_trial:
                        stats['trial_expired'] = True
                        stats['is_trial'] = False
                    revoked = True

            supabase.table('users').update({'stats': stats}).eq('username', username).execute()
    except Exception as _exc:
        logger.warning(f'Heartbeat hatası: {_exc}')
    return jsonify({'status': 'ok', 'premium_revoked': revoked})

# ==============================================================================
# PUSH ID KAYDET — OneSignal subscription ID
# ==============================================================================
@app.route("/api/save_push_id", methods=["POST"])
def save_push_id():
    """Kullanicinin OneSignal subscription ID sini Supabase e kaydeder."""
    if 'username' not in session or not supabase:
        return jsonify({'status': 'error'}), 401
    username = session['username']
    try:
        player_id = (request.json or {}).get('player_id', '').strip()
        if not player_id:
            return jsonify({'status': 'error', 'message': 'player_id eksik'}), 400
        u_res = supabase.table('users').select('stats').eq('username', username).execute()
        if u_res.data:
            stats = u_res.data[0].get('stats', {}) or {}
            if isinstance(stats, str):
                try: stats = json.loads(stats)
                except: stats = {}
            if stats.get('onesignal_player_id') != player_id:
                stats['onesignal_player_id'] = player_id
                supabase.table('users').update({'stats': stats}).eq('username', username).execute()
                app_cache.invalidate(f"pid:{username}")
                print(f"OneSignal player_id kaydedildi: {username} -> {player_id[:20]}...")
        return jsonify({'status': 'ok'})
    except Exception as e:
        print(f"save_push_id hatasi: {e}")
        return jsonify({'status': 'error'}), 500
# ==============================================================================
# FCM TOKEN KAYDET — Firebase Cloud Messaging
# ==============================================================================
@app.route("/api/register-fcm-token", methods=["POST"])
def register_fcm_token():
    """Android uygulamasindan gelen FCM token'ini kaydeder."""
    try:
        data = request.json or {}
        token = data.get('token', '').strip()
        user_id = data.get('user_id', '').strip()
        
        if not token or not user_id:
            return jsonify({'status': 'error', 'message': 'Eksik veri'}), 400
            
        u_res = supabase.table('users').select('stats').eq('username', user_id).execute()
        if u_res.data:
            stats = u_res.data[0].get('stats', {}) or {}
            if isinstance(stats, str):
                try: stats = json.loads(stats)
                except: stats = {}
            if stats.get('fcm_token') != token:
                stats['fcm_token'] = token
                supabase.table('users').update({'stats': stats}).eq('username', user_id).execute()
                app_cache.invalidate(f"fcm:{user_id}")
                print(f"FCM token kaydedildi: {user_id} -> {token[:20]}...")
        return jsonify({'status': 'ok'})
    except Exception as e:
        print(f"register_fcm_token hatasi: {e}")
        return jsonify({'status': 'error'}), 500

# ==============================================================================
# GİZLİLİK POLİTİKASI
# ==============================================================================
@app.route("/privacy-policy")
def privacy_policy():
    return """<!DOCTYPE html>
<html lang="tr">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Gizlilik Politikası – FreeriderTR</title>
<style>*{box-sizing:border-box;margin:0;padding:0}body{background:#09090b;color:#d4d4d8;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;padding:24px;max-width:720px;margin:0 auto}h1{color:#fff;font-size:1.8rem;font-weight:900;margin-bottom:4px}.logo{color:#dc2626}h2{color:#fff;font-size:1.1rem;font-weight:700;margin:24px 0 8px;border-left:3px solid #dc2626;padding-left:10px}p,li{font-size:0.9rem;line-height:1.7;color:#a1a1aa;margin-bottom:6px}ul{padding-left:20px;margin-bottom:10px}a{color:#dc2626}.back{margin-top:32px}hr{border-color:#27272a;margin:16px 0}</style>
</head>
<body>
<h1>FREERIDER<span class="logo">TR</span></h1>
<p style="color:#71717a;font-size:0.78rem;margin-bottom:24px">Son güncelleme: Nisan 2026</p>
<h2>1. Topladığımız Veriler</h2>
<ul><li>Kullanıcı adı, şehir ve isteğe bağlı e-posta adresi</li><li>Uygulama içi aktivite (paylaşımlar, mesajlar, harita noktaları)</li><li>Cihaz push bildirim token'ı (yalnızca bildirim göndermek için)</li><li>Galeri erişimi (yalnızca fotoğraf yüklendiğinde, yerel saklama yapılmaz)</li></ul>
<h2>2. Verilerin Kullanımı</h2>
<ul><li>Topluluk hizmetlerini sunmak ve kişiselleştirmek</li><li>Güvenlik ve spam koruması</li><li>Bildirim göndermek (yalnızca izin verilirse)</li><li>Yasal yükümlülüklerin yerine getirilmesi</li></ul>
<h2>3. Veri Paylaşımı</h2>
<p>Verileriniz üçüncü taraflara satılmaz. Yalnızca hizmet altyapısı (Supabase, Cloudflare R2) için teknik aktarım yapılır.</p>
<h2>4. Veri Saklama ve Silme</h2>
<p>Hesabınızı sildiğinizde tüm kişisel verileriniz kalıcı olarak silinir. Silme talebi için: <a href="/delete-account">freeridertr.com.tr/delete-account</a></p>
<h2>5. Güvenlik</h2>
<p>Şifreler bcrypt ile hashlenerek saklanır. Tüm iletişim HTTPS üzerinden gerçekleşir.</p>
<h2>6. İletişim</h2>
<p>Gizlilikle ilgili sorularınız için: <a href="mailto:destek.freerider@gmail.com">destek.freerider@gmail.com</a></p>
<div class="back"><a href="https://freeridertr.com.tr">← Uygulamaya Geri Dön</a></div>
</body></html>""", 200, {'Content-Type': 'text/html; charset=utf-8'}

# ==============================================================================
# KULLANIM ŞARTLARI
# ==============================================================================
@app.route("/terms")
def terms():
    return """<!DOCTYPE html>
<html lang="tr">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Kullanım Şartları – FreeriderTR</title>
<style>*{box-sizing:border-box;margin:0;padding:0}body{background:#09090b;color:#d4d4d8;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;padding:24px;max-width:720px;margin:0 auto}h1{color:#fff;font-size:1.8rem;font-weight:900;margin-bottom:4px}.logo{color:#dc2626}h2{color:#fff;font-size:1.1rem;font-weight:700;margin:24px 0 8px;border-left:3px solid #dc2626;padding-left:10px}p,li{font-size:0.9rem;line-height:1.7;color:#a1a1aa;margin-bottom:6px}ul{padding-left:20px;margin-bottom:10px}a{color:#dc2626}.back{margin-top:32px}</style>
</head>
<body>
<h1>FREERIDER<span class="logo">TR</span></h1>
<p style="color:#71717a;font-size:0.78rem;margin-bottom:24px">Kullanım Şartları – Son güncelleme: Nisan 2026</p>
<h2>1. Kabul</h2>
<p>FreeriderTR'yi kullanarak bu şartları kabul etmiş sayılırsınız. Kabul etmiyorsanız uygulamayı kullanmayınız.</p>
<h2>2. Kullanıcı Sorumlulukları</h2>
<ul><li>Gerçek bilgilerle kayıt olunmalıdır</li><li>Başka kullanıcılara taciz, hakaret veya zarar verici içerik paylaşılamaz</li><li>+18 içerik, uyuşturucu veya yasa dışı içerik kesinlikle yasaktır</li><li>Spam, bot veya sahte hesap oluşturulamaz</li></ul>
<h2>3. İçerik</h2>
<p>Paylaştığınız içeriklerden yasal olarak siz sorumlusunuz. Yönetim kuralları ihlal eden içerikleri kaldırma ve hesabı askıya alma hakkını saklı tutar.</p>
<h2>4. Hesap Feshi</h2>
<p>Kuralları ihlal eden hesaplar uyarısız kapatılabilir. Hesabınızı kendiniz silmek için: <a href="/delete-account">freeridertr.com.tr/delete-account</a></p>
<h2>5. Sorumluluk Sınırı</h2>
<p>FreeriderTR, kullanıcıların paylaştığı içeriklerden sorumlu tutulamaz. Platform "olduğu gibi" sunulmaktadır.</p>
<h2>6. İletişim</h2>
<p><a href="mailto:destek.freerider@gmail.com">destek.freerider@gmail.com</a></p>
<div class="back"><a href="https://freeridertr.com.tr">← Uygulamaya Geri Dön</a></div>
</body></html>""", 200, {'Content-Type': 'text/html; charset=utf-8'}

# ==============================================================================
# ANDROID APP LINKS
# ==============================================================================
@app.route("/.well-known/assetlinks.json")
def assetlinks():
    PACKAGE_NAME = os.environ.get("TWA_PACKAGE_NAME", "com.freeridertr.app")
    SHA256_FINGERPRINT = os.environ.get("TWA_SHA256_FINGERPRINT", "BURAYA_PARMAK_IZI_GELECEK")

    data = [{
        "relation": ["delegate_permission/common.handle_all_urls"],
        "target": {
            "namespace": "android_app",
            "package_name": PACKAGE_NAME,
            "sha256_cert_fingerprints": [SHA256_FINGERPRINT]
        }
    }]
    return Response(
        json.dumps(data, indent=2),
        mimetype="application/json",
        headers={"Access-Control-Allow-Origin": "*"}
    )

# ==============================================================================
# PWA MANİFEST
# ==============================================================================
@app.route("/manifest.json")
def manifest():
    manifest_data = {
        "name": "FreeriderTR - Downhill Toplulugu",
        "short_name": "FreeriderTR",
        "description": "Turkiye'nin en buyuk Downhill ve Freeride dag bisikleti toplulugu.",
        "start_url": "/",
        "scope": "/",
        "display": "standalone",
        "orientation": "portrait",
        "background_color": "#000000",
        "theme_color": "#b91c1c",
        "lang": "tr",
        "categories": ["sports", "social"],
        "icons": [
            {
                "src": "https://cdn.freeridertr.com.tr/profil%20resmi/unnamed.jpg",
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": "https://cdn.freeridertr.com.tr/profil%20resmi/unnamed.jpg",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "any maskable"
            }
        ],
        "screenshots": [],
        "prefer_related_applications": True,
        "related_applications": [
            {
                "platform": "play",
                "url": "https://play.google.com/store/apps/details?id=com.freeridertr.app",
                "id": "com.freeridertr.app"
            }
        ]
    }
    return jsonify(manifest_data)

# ==============================================================================
# SERVİS WORKER (OneSignal + Offline Cache)
# ==============================================================================
@app.route("/OneSignalSDKWorker.js")
@app.route("/sw.js")
def service_worker():
    sw_code = """
importScripts("https://cdn.onesignal.com/sdks/web/v16/OneSignalSDK.sw.js");

// ══════════════════════════════════════════════════════════
// FreeriderTR Offline Service Worker
// ══════════════════════════════════════════════════════════

const APP_CACHE    = 'freeridertr-app-v3';
const TILE_CACHE   = 'freeridertr-tiles-v3';
const APP_VERSION  = 'v29';

// İlk yüklemede önbelleğe alınacak CDN kaynakları
// ── CDN PRECACHE LİSTESİ ─────────────────────────────────────────────────
// NOT: cdn.tailwindcss.com / unpkg.com CORS başlığı dönmez.
// mode:'no-cors' → "opaque" response (status=0, ok=false) alınır — CORS hatası olmaz.
// Opaque response okunamaz ama cache'e konulabilir → offline için yeterli.
const PRECACHE_URLS = [
    'https://cdn.tailwindcss.com',
    'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
    'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
    'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2',
    'https://unpkg.com/leaflet-control-geocoder/dist/Control.Geocoder.css',
    'https://unpkg.com/leaflet-control-geocoder/dist/Control.Geocoder.js',
];

const TILE_HOSTS = ['tile.openstreetmap.org', 'arcgisonline.com', 'basemaps.cartocdn.com'];

// ── INSTALL: CDN kaynaklarını önbelleğe al ──────────────────────────────
self.addEventListener('install', event => {
    self.skipWaiting();
    event.waitUntil(
        caches.open(APP_CACHE).then(cache =>
            Promise.allSettled(
                PRECACHE_URLS.map(url =>
                    fetch(url, { mode: 'no-cors' })      // 'cors' → 'no-cors' : CORS hatası önlenir
                        .then(res => {
                            if (res.ok || res.type === 'opaque') {
                                return cache.put(url, res);
                            }
                            console.warn('[SW install] Önbelleğe alınamadı:', url, 'status:', res.status);
                        })
                        .catch(err =>
                            console.warn('[SW install] Fetch başarısız:', url, err.message)
                        )
                )
            )
        )
    );
});

// ── ACTIVATE: Eski önbellekleri temizle ──────────────────────────────────
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    // Eğer cache adı mevcut APP_CACHE veya TILE_CACHE değilse sil
                    if (cacheName !== APP_CACHE && cacheName !== TILE_CACHE) {
                        console.log('[SW] Eski önbellek siliniyor:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

// ── FETCH: Tüm istekleri yönet ──
self.addEventListener('fetch', event => {
    const req = event.request;
    const url = req.url;

    // 1) Harita tile'ları: stale-while-revalidate
    if (TILE_HOSTS.some(h => url.includes(h))) {
        event.respondWith(
            caches.open(TILE_CACHE).then(cache =>
                cache.match(req).then(cached => {
                    const network = fetch(req).then(res => {
                        // clone() ÖNCE yapılır, orijinal response döndürülür
                        if (res && res.status === 200) {
                            cache.put(req, res.clone());
                        }
                        return res;
                    }).catch(() => null);
                    return cached || network;
                })
            )
        );
        return;
    }

    // 2) CDN kaynakları: cache-first → yoksa no-cors ile çek ve cache'e at
    if (PRECACHE_URLS.some(u => url === u || url.startsWith(u))) {
        event.respondWith(
            caches.match(req).then(cached => {
                if (cached) return cached;
                return fetch(req, { mode: 'no-cors' }).then(res => {
                    if (res && (res.ok || res.type === 'opaque')) {
                        // res.clone() ile cache'e yaz, orijinali tarayıcıya ver
                        const toCache = res.clone();
                        caches.open(APP_CACHE).then(c => c.put(req, toCache));
                    }
                    return res;
                }).catch(() => null);
            })
        );
        return;
    }

    // 3) Ana sayfa (/): network-first, offline'da cache'den dön
    if (req.mode === 'navigate' || url.endsWith('/') || url.match(/\/$/)) {
        event.respondWith(
            fetch(req)
                .then(res => {
                    if (res && res.status === 200) {
                        // clone() → cache, orijinal → tarayıcı
                        const toCache = res.clone();
                        caches.open(APP_CACHE).then(cache => cache.put(req, toCache));
                    }
                    return res;
                })
                .catch(() =>
                    caches.match(req).then(cached =>
                        cached || caches.match('/')
                    )
                )
        );
        return;
    }

    // 4) API çağrıları: sadece online, offline'da boş JSON dön
    if (url.includes('/api/')) {
        event.respondWith(
            fetch(req).catch(() =>
                new Response(
                    JSON.stringify({ status: 'offline', message: 'İnternet bağlantısı yok. Uygulama çevrimdışı modda çalışıyor.' }),
                    { headers: { 'Content-Type': 'application/json' } }
                )
            )
        );
        return;
    }
});
"""
    return sw_code, 200, {
        'Content-Type': 'application/javascript',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Service-Worker-Allowed': '/'
    }

# ==============================================================================
# BINARY DOSYA YÜKLEME (Multipart)
# ==============================================================================
@app.route("/api/upload", methods=["POST"])
def api_upload():
    """Multipart binary dosya yükleme — base64 JSON'dan çok daha hızlı."""
    if 'username' not in session:
        return jsonify({'status': 'error', 'message': 'Giriş yapmalısınız!'}), 401

    if not r2_client:
        return jsonify({'status': 'error', 'message': 'Depolama servisi yapılandırılmamış, yükleme şu an kullanılamıyor.'})

    file  = request.files.get('file')
    folder = request.form.get('folder', 'uploads')

    if not file or not file.filename:
        return jsonify({'status': 'error', 'message': 'Dosya bulunamadı!'})

    mime_type = file.content_type or 'application/octet-stream'
    allowed_image = mime_type.startswith('image/')
    allowed_video = mime_type.startswith('video/')
    allowed_audio = mime_type.startswith('audio/')

    if not (allowed_image or allowed_video or allowed_audio):
        return jsonify({'status': 'error', 'message': f'Desteklenmeyen dosya türü: {mime_type}'})

    raw_sub = mime_type.split('/')[1].split(';')[0]
    if allowed_video:
        ext = _VIDEO_EXT_MAP.get(raw_sub, 'mp4')
    elif allowed_audio:
        ext = raw_sub if raw_sub in ('mp3','ogg','wav','webm','aac','m4a') else 'mp3'
    else:
        ext = 'jpg' if raw_sub == 'jpeg' else raw_sub

    try:
        file_data = file.read()
        file_size = len(file_data)
        max_size = 50 * 1024 * 1024 if allowed_video else 10 * 1024 * 1024
        if file_size > max_size:
            mb = max_size // (1024*1024)
            return jsonify({'status': 'error', 'message': f'Dosya çok büyük! Maksimum {mb}MB olabilir.'})

        public_url = upload_binary_to_storage(file_data, mime_type, folder, ext)
        if public_url:
            return jsonify({'status': 'ok', 'url': public_url})
        else:
            return jsonify({'status': 'error', 'message': 'Yükleme başarısız oldu (R2).'})
    except Exception as e:
        print(f"❌ /api/upload hatası: {e}")
        return jsonify({'status': 'error', 'message': 'Yükleme başarısız oldu, lütfen tekrar deneyin.'})

# ==============================================================================
# CHUNKED DOSYA YÜKLEME (Nginx limitlerini aşmak için)
# ==============================================================================
@app.route("/api/upload_chunk", methods=["POST"])
def api_upload_chunk():
    if 'username' not in session:
        return jsonify({'status': 'error', 'message': 'Giriş yapmalısınız!'}), 401
    
    upload_id = request.form.get('uploadId')
    chunk_index = request.form.get('chunkIndex')
    file = request.files.get('chunk')
    
    if not upload_id or chunk_index is None or not file:
        return jsonify({'status': 'error', 'message': 'Eksik parametreler.'}), 400
        
    chunk_path = os.path.join(tempfile.gettempdir(), f"freerider_chunk_{upload_id}_{chunk_index}")
    try:
        file.save(chunk_path)
        return jsonify({'status': 'ok'})
    except Exception as e:
        print(f"Chunk kaydetme hatası: {e}")
        return jsonify({'status': 'error', 'message': 'Parça kaydedilemedi.'}), 500

@app.route("/api/upload_finish", methods=["POST"])
def api_upload_finish():
    if 'username' not in session:
        return jsonify({'status': 'error', 'message': 'Giriş yapmalısınız!'}), 401
        
    data = request.json or {}
    upload_id = data.get('uploadId')
    total_chunks = int(data.get('totalChunks', 0))
    folder = data.get('folder', 'uploads')
    
    if not upload_id or total_chunks == 0:
        return jsonify({'status': 'error', 'message': 'Eksik veriler.'}), 400
        
    mime_type = data.get('mimeType', 'application/octet-stream')
    allowed_video = mime_type.startswith('video/')
    raw_sub = mime_type.split('/')[1].split(';')[0] if '/' in mime_type else ''
    
    if allowed_video:
        ext = _VIDEO_EXT_MAP.get(raw_sub, 'mp4')
    else:
        ext = 'jpg' if raw_sub == 'jpeg' else raw_sub

    try:
        file_data = bytearray()
        for i in range(total_chunks):
            chunk_path = os.path.join(tempfile.gettempdir(), f"freerider_chunk_{upload_id}_{i}")
            if not os.path.exists(chunk_path):
                return jsonify({'status': 'error', 'message': f'Eksik parça: {i}. Lütfen tekrar deneyin.'})
            with open(chunk_path, 'rb') as f:
                file_data.extend(f.read())
            os.remove(chunk_path)
            
        file_size = len(file_data)
        max_size = 50 * 1024 * 1024 if allowed_video else 10 * 1024 * 1024
        if file_size > max_size:
            return jsonify({'status': 'error', 'message': f'Dosya çok büyük! Maksimum {max_size//(1024*1024)}MB olabilir.'})
            
        public_url = upload_binary_to_storage(bytes(file_data), mime_type, folder, ext)
        if public_url:
            print(f"✅ Chunked Upload Başarılı: {public_url} ({file_size//1024} KB)")
            return jsonify({'status': 'ok', 'url': public_url})
        return jsonify({'status': 'error', 'message': 'R2 sunucusuna aktarılamadı.'})
        
    except Exception as e:
        print(f"❌ Chunked Upload Birleştirme Hatası: {e}")
        # Temizleme
        for i in range(total_chunks):
            chunk_path = os.path.join(tempfile.gettempdir(), f"freerider_chunk_{upload_id}_{i}")
            if os.path.exists(chunk_path): os.remove(chunk_path)
        return jsonify({'status': 'error', 'message': 'Yükleme birleştirilemedi.'}), 500

# ==============================================================================
# HESAP SİLME WEB SAYFASI (Google Play zorunluluğu)
# ==============================================================================
@app.route("/delete-account", methods=["GET", "POST"])
def delete_account_page():
    """Google Play politikası gereği: Uygulama dışından erişilebilen hesap silme sayfası."""
    from werkzeug.security import check_password_hash

    message = ""
    message_type = ""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        if not username or not password:
            message = "Kullanıcı adı ve şifre zorunludur."
            message_type = "error"
        elif username.lower() == 'admin':
            message = "Yönetici hesabı silinemez."
            message_type = "error"
        else:
            try:
                u_res = supabase.table('users').select('password').eq('username', username).execute()
                if not u_res.data:
                    message = "Kullanıcı bulunamadı."
                    message_type = "error"
                elif not check_password_hash(u_res.data[0].get('password', ''), password):
                    message = "Şifre yanlış."
                    message_type = "error"
                else:
                    asset_result = delete_user_assets(username)
                    logger.info(f"Web hesap silme R2 temizliği: {username} → {asset_result}")
                    supabase.table('markers').delete().eq('addedBy', username).execute()
                    supabase.table('events').delete().eq('creator', username).execute()
                    supabase.table('market').delete().eq('owner', username).execute()
                    supabase.table('stories').delete().eq('user', username).execute()
                    supabase.table('comments').delete().eq('user', username).execute()
                    supabase.table('reels').delete().eq('user', username).execute()
                    supabase.table('dms').delete().or_(f'sender.eq.{username},receiver.eq.{username}').execute()
                    supabase.table('messages').delete().eq('user', username).execute()
                    supabase.table('users').delete().eq('username', username).execute()
                    app_cache.invalidate('leaderboard_data')
                    message = "Hesabınız ve tüm verileriniz kalıcı olarak silindi. Bu işlem geri alınamaz."
                    message_type = "success"
                    logger.info(f"Web hesap silindi: {username}")
            except Exception as exc:
                logger.error(f"Web hesap silme hatası ({username}): {exc}", exc_info=True)
                message = f"Bir hata oluştu: {str(exc)}"
                message_type = "error"

    import html as _html
    _safe_msg = _html.escape(message) if message else ""
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hesabı Sil – FreeriderTR</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ background: #09090b; color: #fff; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 20px; }}
        .card {{ background: #18181b; border: 1px solid #3f3f46; border-radius: 20px; padding: 36px 28px; max-width: 420px; width: 100%; }}
        .logo {{ text-align: center; font-size: 2.5rem; font-weight: 900; letter-spacing: 0.08em; margin-bottom: 6px; }}
        .logo span {{ color: #dc2626; }}
        .subtitle {{ text-align: center; color: #a1a1aa; font-size: 0.78rem; margin-bottom: 28px; text-transform: uppercase; letter-spacing: 0.1em; }}
        h1 {{ font-size: 1.3rem; font-weight: 800; margin-bottom: 8px; color: #ef4444; }}
        .warning {{ background: #1c0a0a; border: 1px solid #7f1d1d; border-radius: 12px; padding: 14px 16px; margin-bottom: 22px; font-size: 0.82rem; color: #fca5a5; line-height: 1.6; }}
        .warning ul {{ padding-left: 18px; margin-top: 8px; }}
        label {{ display: block; font-size: 0.78rem; color: #a1a1aa; margin-bottom: 6px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }}
        input {{ width: 100%; background: #09090b; border: 1px solid #3f3f46; border-radius: 10px; padding: 13px 16px; color: #fff; font-size: 0.95rem; outline: none; margin-bottom: 14px; transition: border 0.2s; }}
        input:focus {{ border-color: #dc2626; }}
        button {{ width: 100%; background: #dc2626; color: #fff; border: none; border-radius: 10px; padding: 14px; font-size: 0.95rem; font-weight: 800; cursor: pointer; text-transform: uppercase; letter-spacing: 0.08em; transition: background 0.2s; }}
        button:hover {{ background: #b91c1c; }}
        .msg-error {{ background: #1c0a0a; border: 1px solid #dc2626; border-radius: 10px; padding: 12px 16px; color: #fca5a5; font-size: 0.85rem; margin-bottom: 16px; }}
        .msg-success {{ background: #052e16; border: 1px solid #166534; border-radius: 10px; padding: 12px 16px; color: #86efac; font-size: 0.85rem; margin-bottom: 16px; }}
        .back {{ text-align: center; margin-top: 18px; }}
        .back a {{ color: #71717a; font-size: 0.8rem; text-decoration: none; }}
        .back a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
<div class="card">
    <div class="logo">FREERIDER<span>TR</span></div>
    <div class="subtitle">Hesap Silme Talebi</div>
    <h1>🗑️ Hesabımı Sil</h1>
    <div class="warning">
        <strong>⚠️ Bu işlem geri alınamaz!</strong>
        <ul>
            <li>Profiliniz kalıcı olarak silinir</li>
            <li>Tüm gönderileriniz, ilanlarınız ve etkinlikleriniz silinir</li>
            <li>XP, rozet ve abonelik bilgileriniz silinir</li>
            <li>Mesajlaşma geçmişiniz silinir</li>
        </ul>
    </div>
    {"<div class='msg-error'>" + _safe_msg + "</div>" if message_type == "error" else ""}
    {"<div class='msg-success'>" + _safe_msg + "</div>" if message_type == "success" else ""}
       {'' if message_type == "success" else '''
    <form method="POST" action="/delete-account">
        <label for="username">Kullanıcı Adı</label>
        <input type="text" id="username" name="username" placeholder="Kullanıcı adınız" required autocomplete="username">
        <label for="password">Şifre</label>
        <input type="password" id="password" name="password" placeholder="Şifrenizi onaylayın" required autocomplete="current-password">
        <button type="submit">HESABIMI KALICI OLARAK SİL</button>
    </form>
    '''}
    <div class="back"><a href="https://freeridertr.com.tr">← Uygulamaya Geri Dön</a></div>
</div>
</body>
</html>"""

# ==============================================================================
# SEO: ROBOTS.TXT & SITEMAP.XML
# ==============================================================================
@app.route("/robots.txt")
def robots_txt():
    domain = request.host_url.rstrip('/')
    content = f"""User-agent: *
Allow: /

Sitemap: {domain}/sitemap.xml
"""
    return Response(content, mimetype="text/plain")

@app.route("/sitemap.xml")
def sitemap_xml():
    domain = request.host_url.rstrip('/')
    content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
   <url>
      <loc>{domain}/</loc>
      <changefreq>daily</changefreq>
      <priority>1.0</priority>
   </url>
   <url>
      <loc>{domain}/terms</loc>
      <changefreq>monthly</changefreq>
      <priority>0.5</priority>
   </url>
   <url>
      <loc>{domain}/privacy-policy</loc>
      <changefreq>monthly</changefreq>
      <priority>0.5</priority>
   </url>
   <url>
      <loc>{domain}/delete-account</loc>
      <changefreq>yearly</changefreq>
      <priority>0.3</priority>
   </url>
</urlset>"""
    return Response(content, mimetype="application/xml")

# ==============================================================================
# GOOGLE SITE VERIFICATION
# ==============================================================================
@app.route("/google2611b5b089af46b6.html")
def google_verification():
    return Response("google-site-verification: google2611b5b089af46b6.html", mimetype="text/html")
