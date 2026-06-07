# ==============================================================================
# FREERIDER AI MODERASYONSİSTEMİ — moderation.py
# Mevcut Flask projesine eklemek için:
#   1. Bu dosyayı ana .py dosyanın yanına koy
#   2. Ana dosyanda: from moderation import register_moderation_routes
#   3. Supabase istemcisi tanımlandıktan HEMEN SONRA:
#      register_moderation_routes(app, supabase, logger, rate_check, push_fn=send_push_to_user)
# ==============================================================================
# GEREKLİ SUPABASE TABLOLARI (SQL):
#
# CREATE TABLE moderation_reports (
#   id          uuid DEFAULT gen_random_uuid() PRIMARY KEY,
#   message_id  text,
#   content     text NOT NULL,
#   sender      text NOT NULL,
#   reporter_ip text,
#   is_inappropriate bool DEFAULT false,
#   severity    text DEFAULT 'low',   -- 'low' | 'medium' | 'high'
#   status      text DEFAULT 'pending', -- 'pending' | 'reviewed' | 'dismissed'
#   admin_note  text,
#   created_at  timestamptz DEFAULT now()
# );
#
# CREATE TABLE banned_users (
#   username    text PRIMARY KEY,
#   banned_at   timestamptz DEFAULT now(),
#   banned_by   text DEFAULT 'admin',
#   reason      text
# );
# ==============================================================================

import re
import html
import unicodedata
import datetime
import logging
import time as _time
import json as _json
from functools import wraps
from flask import request, jsonify, session


# ==============================================================================
# KARAKTER NORMALİZASYON HARİTASI
# ==============================================================================
# Önce Türkçe ve leetspeak karakterleri ASCII karşılıklarına çevir,
# sonra ayırıcıları temizle. Sıra önemli: _CHAR_MAP önce uygulanmalı!
_CHAR_MAP = str.maketrans({
    # Türkçe karakterler (MUTLAKA ASCII'ye çevrilmeden ÖNCE uygulanmalı)
    'ş': 's', 'Ş': 's',
    'ç': 'c', 'Ç': 'c',
    'ğ': 'g', 'Ğ': 'g',
    'ü': 'u', 'Ü': 'u',
    'ö': 'o', 'Ö': 'o',
    'ı': 'i', 'İ': 'i',
    # Leetspeak / obfuscation
    '@': 'a', '4': 'a', 'á': 'a', 'à': 'a', 'ä': 'a', 'â': 'a',
    '!': 'i', '1': 'i', '2': 'i', 'ï': 'i', 'í': 'i',
    '0': 'o', 'ó': 'o', 'ô': 'o',
    '$': 's', '5': 's',
    '3': 'e', 'é': 'e', 'è': 'e',
    '7': 't',
    '6': 'g',
    'ú': 'u', 'û': 'u',
    # Ayırıcılar — kaldır (boşluklar korunacak)
    '.': ' ', '-': ' ', '_': ' ', '*': ' ',
    '(': ' ', ')': ' ', '[': ' ', ']': ' ', '{': ' ', '}': ' ',
    '+': ' ', '=': ' ', '#': ' ', '~': ' ',
})

# ==============================================================================
# TÜRKÇE ARGO VE OFANSİF KELİME PATTERNLERİ
# ==============================================================================
# Not: Pattern'lar normalize edilmiş metin üzerinde çalışır.
# Normalize sonrası: tüm Türkçe karakterler ASCII'ye çevrilmiş,
# boşluk/nokta/tire kaldırılmış, küçük harfe dönüştürülmüş olur.
# Bu yüzden pattern'lar sade ASCII kullanabilir.
_SEP = r'[^a-z]*'  # Harfler arası olası ayırıcı (normalize sonrası çoğu gider ama yine de)

_PATTERNS: list[tuple[str, str]] = [
    # ── YÜKSEK ŞİDDET ──
    # amk / amq — sadece tam kelime (tam kıvamında vs. eşleşmemesi için \b eklendi)
    (rf'\ba+m+[kq]+\b', 'high'),
    (rf'\ba+m+c+[iu]+[kq]+\b', 'high'),
    (rf'\ba+m+[iu]+n+a+\b', 'high'),
    (rf'\ba+n+a+n+[iu]+\b', 'high'),
    
    # sik - sadece kelime sınırı ile (bisiklet gibi kelimelerde false positive önleme)
    (rf'\bs+[iu]+[kq]+\b', 'high'),
    (rf'\bs+[iu]+[kq]+t+[iu]+r+\b', 'high'),
    (rf'\bh+a+s+[iu]+[kq]+t+[iu]+r+\b', 'high'),
    
    # orospu
    (rf'\bo+r+o+s+p+u+\b', 'high'),
    (rf'\bo+r+s+p+u+\b', 'high'),
    (rf'\bo+c+\b', 'high'),
    
    # göt (sadece tam kelime)
    (rf'\bg+o+t+\b', 'high'),
    (rf'\bg+o+t+v+e+r+\b', 'high'),
    
    # piç
    (rf'\bp+[iu]+c+\b', 'high'),
    (rf'\bp+u+s+t+\b', 'high'),
    
    # yarak
    (rf'\by+a+r+a+[kq]+\b', 'high'),
    (rf'\by+a+r+a+m+\b', 'high'),
    
    # ibne vb
    (rf'\b[iu]+b+n+e+\b', 'high'),
    (rf'\bk+a+h+p+e+\b', 'high'),
    (rf'\bg+a+v+a+t+\b', 'high'),
    (rf'\bp+e+z+e+v+e+n+[kq]+\b', 'high'),

    # ── ORTA ŞİDDET ──
    (rf'\ba+[qk]+\b', 'medium'),
    (rf'\bm+[kq]+\b', 'medium'),

    # ── DÜŞÜK ŞİDDET (SADECE UYARI VERİR, FLAGLEMEZ) ──
    (r'\bbok\b', 'low'),
    (r'\bmal\b', 'low'),
    (rf'\bs+a+l+a+[kq]+\b', 'low'),
    (rf'\ba+p+t+a+l+\b', 'low'),
    (rf'\bg+e+r+[iu]+z+e+k+a+l+[iu]+\b', 'low'),
    (rf'\be+z+[iu]+[kq]+\b', 'low')
]

_COMPILED: list[tuple[re.Pattern, str]] = [
    (re.compile(pat, re.IGNORECASE | re.UNICODE), sev)
    for pat, sev in _PATTERNS
]


def _normalize(text: str) -> str:
    """Metni küfür tespiti için normalize eder.

    Sıralama kritik:
    1. Küçük harfe çevir
    2. _CHAR_MAP ile Türkçe + leetspeak → ASCII karşılığı
    3. Kalan non-ASCII'yi sil ama BOŞLUKLARI KORU
    """
    result = text.lower()
    result = result.translate(_CHAR_MAP)
    # Kalan non-ASCII ve noktalama işaretlerini boşluğa çevir
    result = re.sub(r'[^a-z\s]', ' ', result)
    # Fazla boşlukları tek boşluk yap
    result = re.sub(r'\s+', ' ', result).strip()
    # Tekrar eden karakterleri sıkıştır: "aaammk" -> "amk", "sikkk" -> "sik"
    result = re.sub(r'(.)\1{2,}', r'\1', result)
    return result


# ==============================================================================
# ANA İÇERİK ANALİZİ FONKSİYONU
# ==============================================================================
def analyze_content(text: str) -> dict:
    if not text or not text.strip():
        return {
            'is_inappropriate': False,
            'severity': 'none',
            'matched_patterns': [],
            'confidence': 0.0,
        }

    raw_text    = html.unescape(text)
    norm_text   = _normalize(raw_text)

    matched     : list[tuple[str, str]] = []
    severity_order = {'high': 3, 'medium': 2, 'low': 1, 'none': 0}
    max_severity   = 'none'

    for pattern, severity in _COMPILED:
        if pattern.search(norm_text):
            matched.append((pattern.pattern, severity))
            if severity_order[severity] > severity_order[max_severity]:
                max_severity = severity

    hit_count  = len(matched)
    base_score = severity_order[max_severity] / 3.0
    confidence = min(1.0, base_score + (hit_count - 1) * 0.15)

    return {
        'is_inappropriate': max_severity in ('medium', 'high'),
        'severity': max_severity,
        'matched_patterns': [p for p, _ in matched],
        'confidence': round(confidence, 2),
    }


# ==============================================================================
# RAPOR KAYIT YARDIMCISI
# ==============================================================================
def _save_report(supabase_client, log, message_id, content, sender, reporter_ip, analysis) -> bool:
    record = {
        'message_id':     message_id,
        'content':        content[:2000],
        'sender':         sender,
        'reporter_ip':    reporter_ip,
        'is_inappropriate': analysis['is_inappropriate'],
        'severity':       analysis['severity'],
        'status':         'pending',
    }

    log.warning(
        f"[MODERASYONBİLDİRİMİ] Kullanıcı [{sender}], "
        f'"{content[:120]}" ifadesiyle raporlandı. '
        f"Şiddet={analysis['severity']} | Güven={analysis['confidence']}"
    )

    if not supabase_client:
        log.error("Supabase bağlantısı yok — rapor yalnızca log'a yazıldı.")
        return False

    try:
        supabase_client.table('moderation_reports').insert(record).execute()
        log.info(f"Rapor Supabase'e kaydedildi. sender={sender}")
        return True
    except Exception as exc:
        log.error(f"Rapor Supabase kaydedilemedi: {exc}")
        return False


# ==============================================================================
# KULLANICI BAN KONTROL YARDIMCISI
# ==============================================================================
def is_user_banned(supabase_client, username: str) -> bool:
    if not supabase_client or not username:
        return False
    try:
        res = (
            supabase_client.table('banned_users')
            .select('username')
            .eq('username', username)
            .limit(1)
            .execute()
        )
        return bool(res.data)
    except Exception:
        return False


# ==============================================================================
# ANA KAYIT FONKSİYONU
# ==============================================================================
def register_moderation_routes(app, supabase_client, log=None, rate_check_fn=None, push_fn=None):
    """Flask app'e moderasyon rotalarını ekler.

    Parametreler
    ------------
    app              : Flask uygulama nesnesi
    supabase_client  : Başlatılmış Supabase Client (veya None)
    log              : logger nesnesi (opsiyonel)
    rate_check_fn    : rate_check(ip, action, max_calls, window_sec) → bool
    push_fn          : send_push_to_user(username, title, body, url) fonksiyonu
                       Admin'e push bildirim göndermek için kullanılır.
    """
    if log is None:
        log = logging.getLogger('freeridertr.moderation')

    def login_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not session.get('username'):
                return jsonify({'status': 'error', 'message': 'Giriş yapılmamış.'}), 401
            return f(*args, **kwargs)
        return decorated

    def admin_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            role = session.get('role', '')
            username = session.get('username', '')
            is_admin = (
                role in ('Admin', 'SubAdmin')
                or username == 'Admin'
                or username.lower() == 'admin'
                or session.get('is_admin')
            )
            if not is_admin:
                return jsonify({'status': 'error', 'message': 'Yetkisiz erişim.'}), 403
            return f(*args, **kwargs)
        return decorated

    # ══════════════════════════════════════════════════════════════════
    # NOT: /report_message endpoint'i routes_api_data.py'ye taşındı.
    # Frontend sendAction('report_message') → /api/data üzerinden çağrılır.
    # analyze_content() ve _save_report() bu modülden import edilir.
    # ══════════════════════════════════════════════════════════════════

    # ══════════════════════════════════════════════════════════════════
    # ENDPOINT 2: GET /admin/reports
    # ══════════════════════════════════════════════════════════════════
    @app.route('/admin/reports', methods=['GET'])
    @admin_required
    def admin_reports():
        if not supabase_client:
            return jsonify({'status': 'error', 'message': 'Veritabanı bağlantısı yok.'}), 503

        status_filter   = request.args.get('status', 'pending')
        severity_filter = request.args.get('severity', 'all')
        try:
            page     = max(1, int(request.args.get('page', 1)))
            per_page = min(100, max(1, int(request.args.get('per_page', 20))))
        except ValueError:
            page, per_page = 1, 20

        offset = (page - 1) * per_page

        try:
            query = (
                supabase_client.table('moderation_reports')
                .select('*')
                .order('created_at', desc=True)
                .range(offset, offset + per_page - 1)
            )

            if status_filter != 'all':
                query = query.eq('status', status_filter)
            if severity_filter != 'all':
                query = query.eq('severity', severity_filter)

            res = query.execute()
            reports = res.data or []

            return jsonify({
                'status':  'ok',
                'reports': reports,
                'page':    page,
                'per_page': per_page,
                'count':   len(reports),
            })

        except Exception as exc:
            log.error(f"Admin rapor listesi alınamadı: {exc}")
            return jsonify({'status': 'error', 'message': str(exc)}), 500

    # ══════════════════════════════════════════════════════════════════
    # ENDPOINT 3: POST /admin/ban_user
    # ══════════════════════════════════════════════════════════════════
    @app.route('/admin/ban_user', methods=['POST'])
    @admin_required
    def admin_ban_user():
        if not supabase_client:
            return jsonify({'status': 'error', 'message': 'Veritabanı bağlantısı yok.'}), 503

        data     = request.get_json(silent=True) or {}
        username = str(data.get('username', '')).strip()[:80]
        reason   = str(data.get('reason', 'Moderasyon ihlali')).strip()[:500]
        report_id = str(data.get('report_id', '')).strip()[:100]

        if not username:
            return jsonify({'status': 'error', 'message': 'Kullanıcı adı gerekli.'}), 400

        admin_user = session.get('username', 'admin')

        try:
            supabase_client.table('banned_users').upsert({
                'username':  username,
                'banned_by': admin_user,
                'reason':    html.escape(reason),
            }).execute()

            supabase_client.table('users').update(
                {'is_banned': True}
            ).eq('username', username).execute()

            if report_id:
                supabase_client.table('moderation_reports').update({
                    'status':     'reviewed',
                    'admin_note': f'{admin_user} tarafından banlama kararı verildi.',
                }).eq('id', report_id).execute()

            log.warning(
                f"[BAN] {admin_user} → kullanıcı [{username}] banlandı. Gerekçe: {reason}"
            )

            return jsonify({
                'status':  'ok',
                'message': f'{html.escape(username)} başarıyla banlandı.',
            })

        except Exception as exc:
            log.error(f"Kullanıcı banlanırken hata: {exc}")
            return jsonify({'status': 'error', 'message': str(exc)}), 500

    # ══════════════════════════════════════════════════════════════════
    # ENDPOINT 4: POST /admin/dismiss_report
    # ══════════════════════════════════════════════════════════════════
    @app.route('/admin/dismiss_report', methods=['POST'])
    @admin_required
    def admin_dismiss_report():
        if not supabase_client:
            return jsonify({'status': 'error', 'message': 'Veritabanı bağlantısı yok.'}), 503

        data      = request.get_json(silent=True) or {}
        report_id = str(data.get('report_id', '')).strip()

        if not report_id:
            return jsonify({'status': 'error', 'message': 'report_id gerekli.'}), 400

        try:
            supabase_client.table('moderation_reports').update({
                'status':     'dismissed',
                'admin_note': f'Reddedildi — {session.get("username", "admin")}',
            }).eq('id', report_id).execute()

            return jsonify({'status': 'ok', 'message': 'Rapor reddedildi.'})

        except Exception as exc:
            log.error(f"Rapor dismiss hatası: {exc}")
            return jsonify({'status': 'error', 'message': str(exc)}), 500

    # ══════════════════════════════════════════════════════════════════
    # ENDPOINT 5: GET /admin/panel
    # ══════════════════════════════════════════════════════════════════
    @app.route('/admin/panel', methods=['GET'])
    @admin_required
    def admin_panel():
        from flask import redirect
        return redirect("/")

    log.info("✅ Moderasyon rotaları kayıt edildi: /admin/reports, /admin/ban_user, /admin/dismiss_report ( /admin/panel redirects to / )")
    return app
