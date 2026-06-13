"""
routes_api_data.py
==================
Ana veri API'si — /api/data (GET + POST).
GET  : Liderlik tablosu, mesajlar, harita, market, stories, DM'ler.
POST : Login, kayıt, profil güncelleme, mesaj, admin işlemleri ve daha fazlası.
"""

import re
import sys
import json
import html
import time
import uuid
import random
import string
import hashlib
import datetime
import threading

# Windows'ta emoji/Unicode print crash'ini önle
try:
    if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

from flask import request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import (
    app, supabase, logger,
    ADMIN_PASSWORD, ONESIGNAL_APP_ID,
)
from rate_limiter import rate_check
from notifications import send_push_to_user, broadcast_push, _can_broadcast_chat
from storage import upload_base64_to_storage, process_base64_in_dict, upload_binary_to_storage
from ai import _call_groq_ai, check_ai_limit, _GROQ_SYSTEM_CHAT, _GROQ_SYSTEM_DM, ai_bike_analysis, ai_bike_recommend, ai_bike_build, ai_part_analysis, ai_bike_build_final
from database import send_resend_email, delete_user_assets
from moderation import analyze_content, _save_report
from cache import app_cache
from mtb_os import DigitalTwin, reactive_pipeline

def _sync_score_columns(username, stats):
    """Yeni weekly_score/monthly_score sütunlarını JSONB stats ile senkronize tutar."""
    try:
        supabase.table('users').update({
            'weekly_score': stats.get('weekly_xp', 0),
            'monthly_score': stats.get('monthly_xp', 0)
        }).eq('username', username).execute()
    except Exception:
        pass

def _get_week_key():
    """Her Pazartesi sıfırlanan hafta anahtarı döner (YYYY-MM-DD formatında Pazartesi tarihi)."""
    now = datetime.datetime.now()
    monday = now - datetime.timedelta(days=now.weekday())
    return monday.strftime("%Y-%m-%d")

def _get_month_key():
    """Ayın 1'inde sıfırlanan ay anahtarı döner (YYYY-MM formatı)."""
    return datetime.datetime.now().strftime("%Y-%m")

def _auto_finalize_competition(week_id):
    """Belirtilen hafta için sıralamaları otomatik yapar. Her kategoride en yüksek puanlı 3 kişiye rozet/XP verir."""
    try:
        res = supabase.table('bike_competitions').select('*').eq('week_id', week_id).eq('final_rank', 0).execute()
        if not res.data:
            return # Zaten tamamlanmış veya kayıt yok
        
        # Tüm kayıtları kategoriye göre grupla
        cats = {}
        for row in res.data:
            c = row.get('category', 'Genel')
            if c not in cats: cats[c] = []
            cats[c].append(row)
            
        import json as _json
        for c, rows in cats.items():
            # avg_rating'e göre büyükten küçüğe sırala
            rows.sort(key=lambda x: x.get('avg_rating', 0), reverse=True)
            for idx, r in enumerate(rows):
                rank = idx + 1
                r_id = r['id']
                u_name = r['username']
                final_rank = rank if rank <= 3 else 4 # İlk 3 dereceye girer, geri kalanı 4 (derecesiz)
                supabase.table('bike_competitions').update({'final_rank': final_rank}).eq('id', r_id).execute()
                
                # Sadece ilk 3'e ödül ver
                if final_rank <= 3:
                    rank_labels = {1: '1.si 🥇', 2: '2.si 🥈', 3: '3.sü 🥉'}
                    from datetime import date
                    now = date.today()
                    month_names = ['Ocak','Şubat','Mart','Nisan','Mayıs','Haziran','Temmuz','Ağustos','Eylül','Ekim','Kasım','Aralık']
                    month_name = month_names[now.month - 1]
                    badge_text = f'{month_name} {now.year} {c} Yarışması {rank_labels[final_rank]}'
                    
                    winner_res = supabase.table('users').select('stats, xp').eq('username', u_name).execute()
                    if winner_res.data:
                        w_stats = winner_res.data[0].get('stats', {}) or {}
                        if isinstance(w_stats, str):
                            try: w_stats = _json.loads(w_stats)
                            except: w_stats = {}
                        earned = w_stats.get('earned_badges', [])
                        if badge_text not in earned:
                            earned.append(badge_text)
                        w_stats['earned_badges'] = earned
                        xp_reward = {1: 3000, 2: 2000, 3: 1000}[final_rank]
                        current_xp = winner_res.data[0].get('xp', 0)
                        supabase.table('users').update({'stats': w_stats, 'xp': current_xp + xp_reward}).eq('username', u_name).execute()
    except Exception as e:
        logger.error(f'Auto-finalize error: {e}')

def _sync_membership_columns(username, stats):
    """Yeni membership_type/membership_expires_at sütunlarını JSONB stats ile senkronize tutar."""
    try:
        tier = int(stats.get('premium_tier', 0))
        m_type = {3: 'ultra', 2: 'deluxe', 1: 'standard'}.get(tier, 'free')
        exp_str = stats.get('premium_expire_date')
        m_expires = None
        if exp_str:
            m_expires = datetime.datetime.strptime(exp_str, "%Y-%m-%d").isoformat()
        supabase.table('users').update({
            'membership_type': m_type,
            'membership_expires_at': m_expires
        }).eq('username', username).execute()
    except Exception:
        pass


@app.route("/api/data", methods=["GET", "POST"])
def api_data():
    if not supabase: 
        return jsonify({'status': 'error', 'message': 'Veritabanı bağlantısı kurulamadı.'})
        
    # -- Maintenance cache (TTL: 60 sn) --
    _cached_maint = app_cache.get('maintenance_mode')
    if _cached_maint is not None:
        maintenance_mode = _cached_maint
    else:
        try:
            maint_res = supabase.table('settings').select('value').eq('id', 'maintenance').execute()
            maintenance_mode = (maint_res.data[0].get("value") == 'true') if maint_res.data else False
        except Exception as _exc:
            maintenance_mode = False
        app_cache.set('maintenance_mode', maintenance_mode, ttl=60)

    if request.method == "GET":
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # -- Sistem Bakımı: Haftalık/Aylık XP sıfırlama + Üyelik sona erme (Her saat başı) --
        _maint_last = app_cache.get('system_maintenance_last_run')
        if _maint_last is None:
            app_cache.set('system_maintenance_last_run', True, ttl=3600)
            def _bg_system_maintenance():
                try:
                    result = supabase.rpc('system_maintenance').execute()
                    logger.info(f"✅ system_maintenance() sonucu: {result.data}")
                except Exception as e:
                    logger.error(f"system_maintenance() hatası: {e}")
                
                try:
                    import subprocess
                    import datetime
                    now = datetime.datetime.now()
                    if now.hour == 12:
                        last_backup = app_cache.get('daily_github_backup_last_run')
                        if last_backup != now.strftime('%Y-%m-%d'):
                            app_cache.set('daily_github_backup_last_run', now.strftime('%Y-%m-%d'), ttl=86400)
                            subprocess.run(['git', 'add', '.'], cwd='c:/Users/sevdi/OneDrive/Desktop/testson1122-main')
                            subprocess.run(['git', 'commit', '-m', f'Auto backup {now.strftime("%Y-%m-%d %H:%M:%S")}'], cwd='c:/Users/sevdi/OneDrive/Desktop/testson1122-main')
                            subprocess.run(['git', 'push'], cwd='c:/Users/sevdi/OneDrive/Desktop/testson1122-main')
                            logger.info("✅ GitHub automated backup successful")
                except Exception as e:
                    logger.error(f"GitHub backup failed: {e}")
            threading.Thread(target=_bg_system_maintenance, daemon=True).start()

        
        # -- Etkinlik XP: 15 dk'da bir calistir (her GET'te degil) --
        _evxp_last = app_cache.get('event_xp_last_run')
        if _evxp_last is None:
            app_cache.set('event_xp_last_run', True, ttl=900)
            try:
                events_res = supabase.table('events').select('*').execute()
                pending_events = [
                    ev for ev in (events_res.data or [])
                    if ev.get('datetime', '').split(' ')[0] <= today and not ev.get('xp_awarded')
                ]
                if pending_events:
                    all_involved = set()
                    for ev_data in pending_events:
                        if ev_data.get('creator'):
                            all_involved.add(ev_data['creator'])
                        all_involved.update(ev_data.get('attendees', []))
                    
                    user_cache = {}
                    if all_involved:
                        for uname in all_involved:
                            try:
                                u_r = supabase.table('users').select('username, xp, stats').eq('username', uname).execute()
                                if u_r.data:
                                    user_cache[uname] = u_r.data[0]
                            except Exception as _exc:
                                pass
                    
                    for ev_data in pending_events:
                        ev_id = str(ev_data.get('id'))
                        creator = ev_data.get('creator')
                        attendees = ev_data.get('attendees', [])
                        
                        if creator and creator in user_cache:
                            ud = user_cache[creator]
                            try:
                                supabase.table('users').update({'xp': ud.get('xp', 0) + 200}).eq('username', creator).execute()
                                user_cache[creator]['xp'] = ud.get('xp', 0) + 200
                            except Exception as e:
                                pass
                                
                        for att in attendees:
                            if att != creator and att in user_cache:
                                ud = user_cache[att]
                                try:
                                    supabase.table('users').update({'xp': ud.get('xp', 0) + 100}).eq('username', att).execute()
                                    user_cache[att]['xp'] = ud.get('xp', 0) + 100
                                except Exception as e:
                                    pass
                        try:
                            supabase.table('events').update({'xp_awarded': True}).eq('id', ev_id).execute()
                        except Exception as e:
                            pass
            except Exception as e:
                logger.warning(f'Etkinlik XP dagitim hatasi: {e}')


        total_users_count = app_cache.get('total_users_count')
        if total_users_count is None:
            try:
                count_res = supabase.table('users').select('username', count='exact').execute()
                total_users_count = (count_res.count or 0) + 300
            except Exception as _exc:
                total_users_count = 0
            app_cache.set('total_users_count', total_users_count, ttl=900)  # 15 dk: sik degismez

        # Aktif kullanıcılar (cache: 2 dk)
        active_users_count = app_cache.get('active_users_count')
        if active_users_count is None:
            try:
                now_ts2    = int(time.time())
                five_min_ago = now_ts2 - 300
                count_res  = (
                    supabase.table("users")
                    .select("username", count="exact")
                    .filter("stats->>last_seen_ts", "gte", str(five_min_ago))
                    .execute()
                )
                real_active = count_res.count or 0
            except Exception as exc:
                logger.warning(f"Aktif kullanıcı sayımı hatası: {exc}")
                real_active = 0
            active_users_count = real_active
            app_cache.set('active_users_count', active_users_count, ttl=120)  # 2 dk yeterli

        db_data = {
            'users': [], 
            'banned': [], 
            'maintenance': maintenance_mode,
            'pinned_message': {},
            'total_users': total_users_count,
            'active_users': active_users_count
        }

        # --- Aktif Kullanıcı İçin Anlık Sıfırlama Kontrolü (Açık Kapatma) ---
        current_username = session.get('username')
        if current_username:
            try:
                c_res = supabase.table('users').select('stats, xp, role').eq('username', current_username).execute()
                if c_res.data:
                    c_user = c_res.data[0]
                    c_stats = c_user.get('stats') or {}
                    needs_update = False
                    
                    if current_username.lower() == 'admin':
                        if c_stats.get('premium_tier') != 3 or c_user.get('role') != 'Admin':
                            c_stats['premium_tier'] = 3
                            c_stats['premium_color'] = 'rainbow'
                            c_stats['avatar_effect'] = 'fire'
                            c_stats.pop('premium_expire_date', None)
                            if c_user.get('role') != 'Admin':
                                supabase.table('users').update({'role': 'Admin'}).eq('username', current_username).execute()
                            needs_update = True
                    else:
                        if 'premium_expire_date' in c_stats:
                            try:
                                exp_dt = datetime.datetime.strptime(c_stats['premium_expire_date'], "%Y-%m-%d")
                                if datetime.datetime.now() > exp_dt:
                                    was_trial = c_stats.get('is_trial', False)
                                    c_stats['premium_tier'] = 0
                                    c_stats['premium_color'] = ''
                                    c_stats.pop('premium_expire_date', None)
                                    if was_trial:
                                        c_stats['trial_expired'] = True
                                        c_stats['is_trial'] = False
                                    needs_update = True
                            except Exception: pass
                        elif int(c_stats.get('premium_tier', 0)) > 0:
                            # Bitiş tarihi yok ama tier > 0 — üyelik bilgisi eksik/bozuk, sıfırla
                            c_stats['premium_tier'] = 0
                            c_stats['premium_color'] = ''
                            needs_update = True
                            
                    c_month = _get_month_key()
                    c_week = _get_week_key()
                    if c_stats.get('current_month') != c_month:
                        c_stats['monthly_xp'] = 0
                        c_stats['current_month'] = c_month
                        needs_update = True
                    if c_stats.get('current_week') != c_week:
                        c_stats['weekly_xp'] = 0
                        c_stats['current_week'] = c_week
                        needs_update = True
                        
                    if needs_update:
                        supabase.table('users').update({'stats': c_stats}).eq('username', current_username).execute()
                        _sync_membership_columns(current_username, c_stats)
                        _sync_score_columns(current_username, c_stats)
            except Exception as _exc_active:
                logger.warning(f"Aktif kullanici stat acigi kapatma hatasi: {_exc_active}")

        # ── Liderlik tablosu önbelleği (TTL: 5 dakika) ─────────────────────────
        # Her GET isteğinde DB'yi dökmek yerine önbellekten servis edilir.
        # Birleştirilmiş cache: app_cache üzerinden tek sistem
        _lb_cached = app_cache.get('leaderboard_data')
        if _lb_cached:
            db_data['users']  = _lb_cached['users']
            db_data['banned'] = _lb_cached['banned']
        else:
            try:
                # Listedekiler için hafif veri (garage/missions gibi ağır alanlar hariç)
                users_res = (
                    supabase.table('users')
                    .select('username, name, bio, city, avatar, role, xp, stats, accepted_chat_rules')
                    .limit(1000)
                    .execute()
                )
                current_user_lb = session.get('username')
                
                all_users = []
                for u in (users_res.data or []):
                    # Admin sıralamada gösterilmez
                    if u.get('username') == 'Admin' or u.get('role') == 'Admin':
                        continue
                    
                    st = u.get('stats') or {}
                    if isinstance(st, str):
                        try:
                            st = json.loads(st)
                        except json.JSONDecodeError:
                            st = {}
                    
                    light_stats = {k: v for k, v in st.items()
                                   if k not in ('missions', 'daily_missions', 'weekly_missions', 'email', 'verification_code', 'reset_code', 'reset_code_ts', 'ref_code', 'last_spin_date', 'onesignal_player_id', 'marketing_opt_in', 'claimable_refs', 'ref_month')}
                    
                    u2 = dict(u)
                    u2['stats'] = light_stats
                    
                    try: u2['_int_xp'] = int(u2.get('xp') or 0)
                    except: u2['_int_xp'] = 0
                    
                    try: u2['_int_weekly'] = int(light_stats.get('weekly_xp') or 0)
                    except: u2['_int_weekly'] = 0
                    
                    try: u2['_int_monthly'] = int(light_stats.get('monthly_xp') or 0)
                    except: u2['_int_monthly'] = 0
                    
                    all_users.append(u2)

                # Tüm zamanlar, Haftalık ve Aylık için en iyi 100 kişiyi al (sayfada gösterim ve hesaplama için bolca pay)
                top_total = sorted(all_users, key=lambda x: x['_int_xp'], reverse=True)[:100]
                top_weekly = sorted(all_users, key=lambda x: x['_int_weekly'], reverse=True)[:100]
                top_monthly = sorted(all_users, key=lambda x: x['_int_monthly'], reverse=True)[:100]

                # Sadece bu listeye giren eşsiz kullanıcıları frontend'e yolla
                combined = {u['username']: u for u in (top_total + top_weekly + top_monthly)}
                
                # Temizleyip son listeyi oluştur
                stripped = []
                for u in combined.values():
                    u.pop('_int_xp', None)
                    u.pop('_int_weekly', None)
                    u.pop('_int_monthly', None)
                    stripped.append(u)
                import json
                for _u in stripped:
                    _st = _u.get('stats') or {}
                    if isinstance(_st, str):
                        try: _st = json.loads(_st)
                        except: _st = {}
                    _u['stats'] = _st
                
                db_data['users'] = stripped

                if current_user_lb:
                    # Mevcut kullanıcı ilk 50'de değilse tam verisini ayrıca çek
                    if not any(u['username'] == current_user_lb for u in db_data['users']):
                        curr_res = (
                            supabase.table('users')
                            .select('username, name, bio, city, avatar, role, xp, stats, accepted_chat_rules')
                            .eq('username', current_user_lb)
                            .execute()
                        )
                        if curr_res.data:
                            curr_data = curr_res.data[0]
                            # Admin koruması: DB'deki role ne olursa olsun Admin kullanıcısının role'ünü zorla
                            if current_user_lb == 'Admin' or current_user_lb.lower() == 'admin':
                                curr_data['role'] = 'Admin'
                            db_data['users'].append(curr_data)

                banned_res = supabase.table('banned_users').select('username').execute()
                db_data['banned'] = [r['username'] for r in (banned_res.data or [])]

                # Önbelleği güncelle — birleştirilmiş cache sistemi
                app_cache.set('leaderboard_data', {
                    'users':  db_data['users'],
                    'banned': db_data['banned'],
                }, ttl=600)  # 10 dk: liderlik tablosu sik degismez
            except Exception as exc:
                logger.error(f"Liderlik tablosu yükleme hatası: {exc}", exc_info=True)

        # ── MEVCUT KULLANICI İÇİN HER ZAMAN EN GÜNCEL VERİYİ KULLAN ──
        # Cache nedeniyle kendi güncellemelerini (örn. premium, chat kuralları) 
        # görememe sorununu çözer.
        if session.get('username'):
            cu = session.get('username')
            try:
                curr_res = (
                    supabase.table('users')
                    .select('username, name, bio, city, avatar, role, xp, stats, accepted_chat_rules')
                    .eq('username', cu)
                    .execute()
                )
                if curr_res.data:
                    curr_data = curr_res.data[0]
                    import json
                    _st = curr_data.get('stats') or {}
                    if isinstance(_st, str):
                        try: _st = json.loads(_st)
                        except: _st = {}
                    curr_data['stats'] = _st

                    if cu.lower() == 'admin':
                        curr_data['role'] = 'Admin'
                        if isinstance(curr_data.get('stats'), dict):
                            curr_data['stats']['premium_tier'] = 3
                            curr_data['stats']['premium_color'] = 'rainbow'
                            curr_data['stats']['avatar_effect'] = 'fire'
                            curr_data['stats'].pop('premium_expire_date', None)
                            
                    st = curr_data.get('stats') or {}
                    if isinstance(st, str):
                        try: st = json.loads(st)
                        except: st = {}
                    light_stats = {k: v for k, v in st.items()
                                   if k not in ('missions', 'daily_missions', 'weekly_missions', 'email', 'verification_code', 'reset_code', 'reset_code_ts', 'ref_code', 'last_spin_date', 'onesignal_player_id', 'marketing_opt_in', 'claimable_refs', 'ref_month')}
                    curr_data['stats'] = light_stats
                    
                    db_data['users'] = [u for u in db_data['users'] if u['username'] != cu]
                    db_data['users'].append(curr_data)
            except Exception as e:
                logger.warning(f"Güncel kullanıcı verisi çekilemedi: {e}")


        _cached_pin = app_cache.get('pinned_message')
        if _cached_pin is not None:
            db_data['pinned_message'] = _cached_pin
        else:
            try:
                pin_res = supabase.table('settings').select('value').eq('id', 'pinned_message').execute()
                if pin_res.data:
                    val = pin_res.data[0].get('value', '{}')
                    if val:
                        db_data['pinned_message'] = json.loads(val)
                app_cache.set('pinned_message', db_data['pinned_message'], ttl=60)
            except Exception as exc:
                logger.warning(f"Sabitlenmiş mesaj yükleme hatası: {exc}")
        
        # ── Tablo verileri — select('*') ile tüm sütunlar çekilir ──────────────
        # NOT: Önceden _TABLE_COLUMNS ile spesifik sütun isimleri belirtiliyordu.
        # Veritabanındaki sütun isimleri ile kodun beklediği isimler uyuşmadığında
        # try-except bloğu boş veri döndürüyordu. Artık select('*') kullanılıyor.
        _TABLE_SELECTS = {
            'news':    ('*', 50),
            'events':  ('*', 50),
        }
        for table, (columns, limit) in _TABLE_SELECTS.items():
            try:
                res = supabase.table(table).select(columns).order('id', desc=True).limit(limit).execute()
                db_data[table] = res.data or []
            except Exception as exc:
                db_data[table] = []

        # Market tablosu — bumped_at sütunu yoksa created_at'e fallback
        try:
            try:
                market_res = supabase.table('market').select('*').order('bumped_at', desc=True).limit(50).execute()
            except Exception:
                # bumped_at sütunu yoksa created_at ile sırala
                logger.info("Market: bumped_at sütunu bulunamadı, created_at ile sıralanıyor.")
                market_res = supabase.table('market').select('*').order('id', desc=True).limit(50).execute()
            db_data['market'] = market_res.data or []
        except Exception as exc:
            logger.warning(f"Market yükleme hatası: {exc}")
            db_data['market'] = []

        # Markers - Pagination ile TÜM markerları çek (Supabase default 1000 limit'ini aşmak için)
        # NOT: icon_type, photos, views, bumped_at sütunları eski schemada olmayabilir.
        # select('*') kullanarak mevcut tüm sütunları çekiyoruz — böylece eksik sütun hatası oluşmaz.
        try:
            _all_markers = []
            _page_size = 1000
            _offset = 0
            while True:
                _chunk = (
                    supabase.table('markers')
                    .select('*')
                    .range(_offset, _offset + _page_size - 1)
                    .execute()
                )
                _rows = _chunk.data or []
                _all_markers.extend(_rows)
                if len(_rows) < _page_size:
                    break  # Son sayfa
                _offset += _page_size
                if _offset >= 10000:  # Güvenlik limiti
                    break
            db_data['markers'] = _all_markers
            logger.info(f"Markers yüklendi: {len(_all_markers)} adet")
        except Exception as exc:
            logger.warning(f"Markers yükleme hatası: {exc}")
            db_data['markers'] = []

        # Stories
        try:
            now_ts = int(time.time())
            stories_res = supabase.table('stories').select('id, user, text, image, expires_at, created_at, viewers').gt('expires_at', now_ts).order('id', desc=True).limit(50).execute()
            db_data['stories'] = stories_res.data or []
        except Exception as exc:
            logger.warning(f"Stories yükleme hatası: {exc}")
            db_data['stories'] = []

        # DM'ler
        try:
            current_user = session.get('username')
            is_main_admin = (session.get('role') == 'Admin' or current_user == 'Admin')
            if current_user:
                if is_main_admin:
                    dm_res = (
                        supabase.table('dms')
                        .select('*')
                        .or_(f"participants.cs.{{{current_user}}},participants.cs.{{Admin}}")
                        .order('id', desc=True)
                        .limit(50)
                        .execute()
                    )
                else:
                    dm_res = (
                        supabase.table('dms')
                        .select('*')
                        .contains('participants', [current_user])
                        .order('id', desc=True)
                        .limit(50)
                        .execute()
                    )
                db_data['dms'] = dm_res.data or []
            else:
                db_data['dms'] = []
        except Exception as exc:
            logger.warning(f"DM yükleme hatası: {exc}")
            db_data['dms'] = []

        # Mesajlar (son 50 mesaj, eski→yeni sıralı)
        try:
            try:
                msg_res = (
                    supabase.table('messages')
                    .select('id, user, text, type, photo, voice, reactions, reply_to, is_flagged, flag_count, created_at')
                    .order('id', desc=True)
                    .limit(50)
                    .execute()
                )
            except Exception as _col_exc:
                # is_flagged/flag_count sütunları henüz eklenmemişse fallback
                logger.info(f"Mesajlar: flag sütunları bulunamadı, select('*') ile devam ediliyor: {_col_exc}")
                msg_res = (
                    supabase.table('messages')
                    .select('*')
                    .order('id', desc=True)
                    .limit(50)
                    .execute()
                )
            # Flag alanlarını normalize et (null → false/0 dönüşümü)
            _raw_msgs = msg_res.data or []
            for _m in _raw_msgs:
                if _m.get('is_flagged') is None:
                    _m['is_flagged'] = False
                if _m.get('flag_count') is None:
                    _m['flag_count'] = 0
            db_data['messages'] = list(reversed(_raw_msgs))
            
            # Sohbette mesajı olup da ilk 50 (leaderboard) içinde olmayan kullanıcıları db_data['users']'a ekle.
            existing_users = {u['username'] for u in db_data['users']}
            missing_users = set()
            for m in _raw_msgs:
                u_name = m.get('user')
                if u_name and u_name not in existing_users and u_name not in ('Freerider AI', 'Moderatör AI', 'SİSTEM AI', 'Admin'):
                    missing_users.add(u_name)
                    
            if missing_users:
                try:
                    missing_res = (
                        supabase.table('users')
                        .select('username, name, bio, city, avatar, role, xp, stats, accepted_chat_rules')
                        .in_('username', list(missing_users))
                        .execute()
                    )
                    for u in (missing_res.data or []):
                        st = u.get('stats') or {}
                        if isinstance(st, str):
                            try:
                                st = json.loads(st)
                            except json.JSONDecodeError:
                                st = {}
                        light_stats = {k: v for k, v in st.items()
                                       if k not in ('missions', 'daily_missions', 'weekly_missions', 'email', 'verification_code', 'reset_code', 'reset_code_ts', 'ref_code', 'last_spin_date', 'onesignal_player_id', 'marketing_opt_in', 'claimable_refs', 'ref_month')}
                        u2 = dict(u); u2['stats'] = light_stats
                        db_data['users'].append(u2)
                except Exception as ex:
                    logger.warning(f"Eksik kullanıcıları yüklerken hata: {ex}")
        except Exception as exc:
            logger.warning(f"Mesajlar yükleme hatası: {exc}")
            db_data['messages'] = []

        return jsonify(db_data)
        
    elif request.method == "POST":
        req = request.json or {}
        action = req.get('action')
        data = req.get('data', {})
        
        # IP Spoofing Koruması: Sadece ilk geçerli IP'yi al (en dıştaki istemci)
        forwarded_for = request.headers.get('X-Forwarded-For', '')
        if forwarded_for:
            # En soldaki IP gerçek istemci IP'sidir, sağa doğru proxyler listelenir
            client_ip = forwarded_for.split(',')[0].strip()
        else:
            client_ip = request.remote_addr or '0.0.0.0'
            
        if not client_ip:
            client_ip = '0.0.0.0'

        # Rate limiting — brute force koruması
        _rate_limits = {
            'login':                (10,  300),   # 5 dak içinde maks 10 deneme
            'login_with_token':     (20,  300),   # 5 dak içinde maks 20 deneme
            'login_legacy':         (20,  300),
            'register':             (10,  600),   # 10 dak içinde maks 10 kayıt
            'ask_ai':               (20,  60),    # 1 dak içinde maks 20 istek
            'request_reset':        (10,  600),   # 10 dak içinde maks 10 istek
            'reset_password_code':  (10,  600),
            'send_profile_verification': (10, 600),
            'add_message':          (30,  60),    # 1 dak içinde maks 30 mesaj
            'send_dm':              (30,  60),    # 1 dak içinde maks 30 DM
            'add_marker':           (20,  600),   # 10 dak içinde maks 20 marker
            'daily_spin':           (10,  60),    # 1 dak içinde maks 10 istek
            'verify_email':         (10,  600),   # brute-force kod tahmini önleme
            'report_message':       (20,  600),   # 10 dak içinde maks 20 rapor
            'report_user':          (10,  600),   # 10 dak içinde maks 10 şikayet
            'add_market':           (20,  300),   # 5 dak içinde maks 20 market ilanı
            'add_event':            (20,  300),   # 5 dak içinde maks 20 etkinlik
            'add_news':             (20,  300),   # 5 dak içinde maks 20 haber
            'delete_news':          (30,  300),   # 5 dak içinde maks 30 silme
            'upload_media':         (30,  300),   # 5 dak içinde maks 30 upload
            'ai_support_chat':        (15, 60),    # DoS Protection: 1 dakikada maks 15 AI Chat isteği
            'ai_bike_analysis':       (15, 60),    # DoS Protection
            'ai_bike_recommendation': (15, 60),    # DoS Protection
            'ai_bike_build':          (15, 60),    # DoS Protection
            'ai_bike_build_final':    (15, 60),    # DoS Protection
            'ai_part_analysis':       (15, 60),    # DoS Protection
            'add_reel':             (20,  300),   # 5 dak içinde maks 20 reel
            'add_story':            (30,  300),   # 5 dak içinde maks 30 story
            'submit_bike':          (5,   600),   # 10 dak içinde maks 5 yarışma kaydı
            'rate_bike':            (30,  300),   # 5 dak içinde maks 30 puanlama
            'admin_set_winner':     (20,  300),   # 5 dak içinde maks 20 admin işlemi
            'redeem_code':          (5,   300),    # 5 dak içinde maks 5 deneme
        }
        if action in _rate_limits:
            max_c, win = _rate_limits[action]
            if not rate_check(client_ip, action, max_c, win):
                return jsonify({'status': 'error', 'message': 'Çok fazla istek gönderdiniz. Lütfen biraz bekleyin.'}), 429

        if action not in ['login', 'login_with_token', 'login_legacy', 'register', 'set_new_password', 'ask_ai', 'daily_spin', 'request_reset', 'reset_password_code', 'verify_email', 'send_profile_verification', 'claim_ref_reward', 'get_stories', 'upload_media']:
            process_base64_in_dict(data)
        
        try:
            # 1) Herkese Açık İşlemler
            if action == 'login':
                username_input = data.get('username', '').strip()
                password_input = data.get('password', '').strip()
                
                # Debug: log admin login attempts
                if username_input.lower() == 'admin':
                    print(f"[ADMIN LOGIN DEBUG] username='{username_input}' pw_len={len(password_input)} ADMIN_PASSWORD='{ADMIN_PASSWORD}' match={password_input == ADMIN_PASSWORD}")
                
                if username_input.lower() == 'admin' and password_input == ADMIN_PASSWORD:
                    # Admin kullanıcı girişi — tam kullanıcı verisiyle
                    session['username'] = 'Admin'
                    session['role'] = 'Admin'
                    session['is_admin'] = True
                    # Veritabanından Admin kullanıcı verisini çek
                    admin_res = supabase.table('users').select('username, name, bio, city, avatar, role, xp, stats, accepted_chat_rules').ilike('username', 'admin').execute()
                    if admin_res.data:
                        admin_data = admin_res.data[0]
                        admin_data['role'] = 'Admin'
                        admin_stats = admin_data.get('stats', {})
                        if isinstance(admin_stats, str):
                            try: admin_stats = json.loads(admin_stats)
                            except: admin_stats = {}
                        admin_stats['session_token'] = str(uuid.uuid4())
                        admin_stats['last_seen_ts'] = int(time.time())
                        try:
                            supabase.table('users').update({'stats': admin_stats, 'role': 'Admin'}).eq('username', admin_data['username']).execute()
                        except: pass
                        admin_data['stats'] = admin_stats
                        admin_data['session_token'] = admin_stats['session_token']
                        admin_data.pop('password', None)
                        return jsonify({'status': 'ok', 'user': admin_data})
                    return jsonify({'status': 'ok', 'user': {'username': 'Admin', 'role': 'Admin'}})

                if maintenance_mode: 
                    return jsonify({'status': 'error', 'message': 'Sistem bakım modunda.'})
                
                # ilike zaten büyük/küçük harf duyarsız, tek sorgu yeterli
                user_res = supabase.table('users').select('username, name, bio, city, avatar, role, xp, stats, accepted_chat_rules, password').ilike('username', username_input.strip()).execute()

                if user_res.data:
                    user_data = user_res.data[0]
                    
                    ban_check = supabase.table('banned_users').select('username').eq('username', user_data['username']).execute()
                    if ban_check.data: 
                        return jsonify({'status': 'error', 'message': 'Hesabınız banlanmıştır!'})
                        
                    stored_hash = user_data.get('password') or ''
                    password_ok = False
                    
                    # Şifre alanı boş veya None ise
                    if not stored_hash:
                        is_setting = data.get('is_setting_new_password', False)
                        if not is_setting:
                            return jsonify({'status': 'needs_new_password', 'message': 'Şifreniz güvenlik nedeniyle silinmiştir. Lütfen yeni şifrenizi yazın.', 'username': user_data['username']})
                        if len(password_input) < 4:
                            return jsonify({'status': 'error', 'message': 'Yeni şifreniz en az 4 karakter olmalıdır.'})
                        try:
                            new_hash = generate_password_hash(password_input, method='pbkdf2:sha256')
                            supabase.table('users').update({'password': new_hash}).eq('username', user_data['username']).execute()
                            password_ok = True
                        except Exception as e:
                            return jsonify({'status': 'error', 'message': 'Şifre güncellenirken hata oluştu.'})
                    password_raw = data.get('password', '')
                    candidates = [password_input]
                    if password_raw and password_raw != password_input:
                        candidates.append(password_raw)
                    if len(password_input) > 0 and password_input[0].isupper():
                        candidates.append(password_input[0].lower() + password_input[1:])
                        
                    for cand in candidates:
                        try:
                            if check_password_hash(stored_hash, cand):
                                password_ok = True
                                password_input = cand
                                break
                        except Exception as e:
                            pass
                            
                        if stored_hash == cand:
                            password_ok = True
                            password_input = cand
                            break
                        
                    if password_ok and not stored_hash.startswith('scrypt:') and not stored_hash.startswith('pbkdf2:'):
                        try:
                            new_hash = generate_password_hash(password_input, method='pbkdf2:sha256')
                            supabase.table('users').update({'password': new_hash}).eq('username', user_data['username']).execute()
                        except Exception as e:
                            logger.warning(f"Re-hash error: {e}")

                    if password_ok:
                        # --- ADMIN KORUMASI ---
                        if user_data['username'].lower() == 'admin':
                            user_data['role'] = 'Admin'
                            if 'stats' not in user_data or not isinstance(user_data['stats'], dict):
                                user_data['stats'] = {}
                            user_data['stats']['premium_tier'] = 3
                            user_data['stats']['premium_color'] = 'rainbow'
                            user_data['stats']['avatar_effect'] = 'fire'
                            user_data['stats'].pop('premium_expire_date', None)
                            try:
                                supabase.table('users').update({
                                    "role": "Admin",
                                    "stats": user_data['stats']
                                }).eq('username', user_data['username']).execute()
                            except Exception:
                                pass

                        session['username'] = user_data['username']
                        session['role'] = user_data.get('role', 'user')
                        if user_data['username'].lower() == 'admin':
                            session['is_admin'] = True

                        user_data.pop('password', None)
                        
                        today = datetime.datetime.now().strftime("%Y-%m-%d")
                        current_month = _get_month_key()
                        current_week = _get_week_key()
                        yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
                        
                        stats = user_data.get('stats', {})
                        
                        if 'premium_expire_date' in stats:
                            try:
                                exp_dt = datetime.datetime.strptime(stats['premium_expire_date'], "%Y-%m-%d")
                                if datetime.datetime.now() > exp_dt:
                                    was_trial = stats.get('is_trial', False)
                                    stats['premium_tier'] = 0
                                    stats['premium_color'] = ''
                                    stats.pop('premium_expire_date', None)
                                    if was_trial:
                                        stats['trial_expired'] = True
                                        stats['is_trial'] = False
                                    supabase.table('users').update({"stats": stats}).eq('username', user_data['username']).execute()
                                    _sync_membership_columns(user_data['username'], stats)
                            except Exception as e:
                                print(f"⚠️ Premium sona erme hatası: {e}")
                        elif int(stats.get('premium_tier', 0)) > 0 and user_data['username'].lower() != 'admin':
                            # Bitiş tarihi yok ama tier > 0 — üyelik bilgisi eksik/bozuk, sıfırla
                            stats['premium_tier'] = 0
                            stats['premium_color'] = ''
                            try:
                                supabase.table('users').update({"stats": stats}).eq('username', user_data['username']).execute()
                                _sync_membership_columns(user_data['username'], stats)
                            except Exception as e:
                                print(f"⚠️ Premium temizleme hatası: {e}")
                        
                        # Ödül dağıtımı artık migration_system_maintenance.sql içindeki PostgreSQL fonksiyonlarında yapılıyor.
                        # (Bkz. reset_weekly_scores ve reset_monthly_scores)

                        last_login = stats.get('last_login', '')
                        streak = stats.get('login_streak', 0)
                        
                        if stats.get('current_month') != current_month:
                            stats['monthly_xp'] = 0
                            stats['current_month'] = current_month
                            
                        if stats.get('current_week') != current_week:
                            stats['weekly_xp'] = 0
                            stats['current_week'] = current_week
                        
                        stats['last_seen_ts'] = int(time.time())

                        if last_login != today:
                            if last_login == yesterday:
                                streak += 1
                            else:
                                streak = 1
                                
                            stats['last_login'] = today
                            stats['login_streak'] = streak
                            
                            daily_xp = 20
                            if streak % 7 == 0: daily_xp += 200
                            if streak % 30 == 0: daily_xp += 2000
                            
                            user_data['xp'] = user_data.get('xp', 0) + daily_xp
                            stats['monthly_xp'] = stats.get('monthly_xp', 0) + daily_xp
                            stats['weekly_xp'] = stats.get('weekly_xp', 0) + daily_xp
                            
                            supabase.table('users').update({
                                "xp": user_data['xp'], 
                                "stats": stats
                            }).eq('username', user_data['username']).execute()
                            _sync_score_columns(user_data['username'], stats)
                            
                            user_data['stats'] = stats
                            user_data['just_got_daily'] = daily_xp 
                        
                        # Her girişte last_seen_ts güncelle
                        stats['last_seen_ts'] = int(time.time())
                        # Sadece token yoksa yenisini üret. Çoklu cihazlarda token'ın düşmesini engeller.
                        if not stats.get('session_token'):
                            stats['session_token'] = str(uuid.uuid4())
                        session_token = stats['session_token']
                        try:
                            supabase.table('users').update({"stats": stats}).eq('username', user_data['username']).execute()
                        except Exception as e:
                            print(f"⚠️ Login stat güncelleme hatası: {e}")
                        user_data['stats'] = stats
                        user_data['session_token'] = session_token
                        if user_data.get('accepted_chat_rules'):
                            session['accepted_chat_rules'] = True
                        return jsonify({'status': 'ok', 'user': user_data})
                        
                return jsonify({'status': 'error', 'message': 'Hatalı kullanıcı adı veya şifre!'})

            
            elif action == 'admin_grant_badge':
                if session.get('role') not in ['Admin', 'SubAdmin']:
                    return jsonify({"status": "error", "message": "Yetkisiz erişim"}), 403
                target_user = data.get('target_user')
                badge_id = data.get('badge_id')
                if not target_user or not badge_id:
                    return jsonify({"status": "error", "message": "Eksik bilgi"}), 400
                res = supabase.table('users').select('stats').eq('username', target_user).execute()
                if not res.data:
                    return jsonify({"status": "error", "message": "Kullanıcı bulunamadı"}), 404
                stats = res.data[0].get('stats', {}) or {}
                earned = stats.get('earned_badges', [])
                if badge_id not in earned:
                    earned.append(badge_id)
                    stats['earned_badges'] = earned
                    supabase.table('users').update({'stats': stats}).eq('username', target_user).execute()
                return jsonify({"status": "success", "message": f"{badge_id} rozeti verildi."})

            elif action == 'admin_revoke_badge':
                if session.get('role') not in ['Admin', 'SubAdmin']:
                    return jsonify({"status": "error", "message": "Yetkisiz erişim"}), 403
                target_user = data.get('target_user')
                badge_id = data.get('badge_id')
                if not target_user or not badge_id:
                    return jsonify({"status": "error", "message": "Eksik bilgi"}), 400
                res = supabase.table('users').select('stats').eq('username', target_user).execute()
                if not res.data:
                    return jsonify({"status": "error", "message": "Kullanıcı bulunamadı"}), 404
                stats = res.data[0].get('stats', {}) or {}
                earned = stats.get('earned_badges', [])
                if badge_id in earned:
                    earned.remove(badge_id)
                    stats['earned_badges'] = earned
                    supabase.table('users').update({'stats': stats}).eq('username', target_user).execute()
                return jsonify({"status": "success", "message": f"{badge_id} rozeti silindi."})

            elif action == 'login_with_token':
                username_input = data.get('username', '').strip()
                token_input = data.get('token', '').strip()
                
                if not username_input or not token_input:
                    return jsonify({'status': 'error', 'message': 'Eksik bilgi.'})
                    
                user_res = supabase.table('users').select('username, name, bio, city, avatar, role, xp, stats, accepted_chat_rules').ilike('username', username_input).execute()
                
                if user_res.data:
                    user_data = user_res.data[0]
                    ban_check = supabase.table('banned_users').select('username').eq('username', user_data['username']).execute()
                    if ban_check.data: 
                        return jsonify({'status': 'error', 'message': 'Hesabınız banlanmıştır!'})
                        
                    stats = user_data.get('stats', {})
                    if isinstance(stats, str):
                        try: stats = json.loads(stats)
                        except: stats = {}
                        
                    if stats.get('session_token') == token_input:
                        if user_data['username'].lower() == 'admin':
                            session['username'] = 'Admin'
                            session['role'] = 'Admin'
                            session['is_admin'] = True
                        else:
                            session['username'] = user_data['username']
                            session['role'] = user_data.get('role', 'user')
                            
                        today = datetime.datetime.now().strftime("%Y-%m-%d")
                        current_month = _get_month_key()
                        current_week = _get_week_key()
                        yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
                        
                        last_login = stats.get('last_login', '')
                        streak = stats.get('login_streak', 0)
                        
                        if stats.get('current_month') != current_month:
                            stats['monthly_xp'] = 0
                            stats['current_month'] = current_month
                            
                        if stats.get('current_week') != current_week:
                            stats['weekly_xp'] = 0
                            stats['current_week'] = current_week
                        
                        stats['last_seen_ts'] = int(time.time())
                        
                        if last_login != today:
                            if last_login == yesterday:
                                streak += 1
                            else:
                                streak = 1
                            stats['last_login'] = today
                            stats['login_streak'] = streak
                            
                            daily_xp = 20
                            if streak % 7 == 0: daily_xp += 200
                            if streak % 30 == 0: daily_xp += 2000
                            
                            user_data['xp'] = user_data.get('xp', 0) + daily_xp
                            stats['monthly_xp'] = stats.get('monthly_xp', 0) + daily_xp
                            stats['weekly_xp'] = stats.get('weekly_xp', 0) + daily_xp
                            user_data['just_got_daily'] = daily_xp 
                            
                        try:
                            supabase.table('users').update({
                                "xp": user_data.get('xp', 0), 
                                "stats": stats
                            }).eq('username', user_data['username']).execute()
                            if last_login != today:
                                _sync_score_columns(user_data['username'], stats)
                        except Exception as e:
                            logger.error(f"login_with_token stat update error: {e}")
                            
                        user_data['stats'] = stats
                        if user_data.get('accepted_chat_rules'):
                            session['accepted_chat_rules'] = True
                        return jsonify({'status': 'ok', 'user': user_data})
                        
                return jsonify({'status': 'error', 'message': 'Geçersiz oturum.'})

            elif action == 'login_legacy':
                username_input = data.get('username', '').strip()
                if not username_input: return jsonify({'status': 'error'})
                user_res = supabase.table('users').select('username, name, bio, city, avatar, role, xp, stats, accepted_chat_rules').ilike('username', username_input).execute()
                if user_res.data:
                    user_data = user_res.data[0]
                    stats = user_data.get('stats', {})
                    if isinstance(stats, str):
                        try: stats = json.loads(stats)
                        except: stats = {}
                    
                    if user_data['username'].lower() == 'admin':
                        session['username'] = 'Admin'
                        session['role'] = 'Admin'
                        session['is_admin'] = True
                    else:
                        session['username'] = user_data['username']
                        session['role'] = user_data.get('role', 'user')
                        
                    if 'session_token' not in stats:
                        stats['session_token'] = str(uuid.uuid4())
                    session_token = stats['session_token']
                    try: supabase.table('users').update({"stats": stats}).eq('username', user_data['username']).execute()
                    except: pass
                    
                    user_data['stats'] = stats
                    user_data['session_token'] = session_token
                    if user_data.get('accepted_chat_rules'): session['accepted_chat_rules'] = True
                    return jsonify({'status': 'ok', 'user': user_data})
                return jsonify({'status': 'error'})

            elif action == 'google_login':
                if maintenance_mode:
                    return jsonify({'status': 'error', 'message': 'Sistem bakım modunda.'})
                    
                email = data.get('email', '').strip().lower()
                name = data.get('name', '').strip()
                avatar_url = data.get('avatar_url', '').strip()
                
                if not email:
                    return jsonify({'status': 'error', 'message': 'Google e-posta adresi alınamadı.'})
                
                # Check if user exists by email
                try:
                    user_res = supabase.table('users').select('username, name, bio, city, avatar, role, xp, stats, accepted_chat_rules').filter('stats->>email', 'eq', email).execute()
                except Exception:
                    user_res = supabase.table('users').select('username, name, bio, city, avatar, role, xp, stats, accepted_chat_rules').execute()
                    
                target_user = None
                for u in (user_res.data or []):
                    s = u.get('stats', {})
                    if isinstance(s, str):
                        try: s = json.loads(s)
                        except: s = {}
                    if isinstance(s, dict) and s.get('email', '').strip().lower() == email:
                        target_user = u
                        break
                        
                if target_user:
                    user_data = target_user
                    ban_check = supabase.table('banned_users').select('username').eq('username', user_data['username']).execute()
                    if ban_check.data: 
                        return jsonify({'status': 'error', 'message': 'Hesabınız banlanmıştır!'})
                        
                    session['username'] = user_data['username']
                    session['role'] = user_data.get('role', 'user')
                    if user_data['username'].lower() == 'admin':
                        session['is_admin'] = True
                        
                    today = datetime.datetime.now().strftime("%Y-%m-%d")
                    current_month = _get_month_key()
                    current_week = _get_week_key()
                    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
                    stats = user_data.get('stats', {})
                    
                    if 'premium_expire_date' in stats:
                        try:
                            exp_dt = datetime.datetime.strptime(stats['premium_expire_date'], "%Y-%m-%d")
                            if datetime.datetime.now() > exp_dt:
                                stats['premium_tier'] = 0
                                stats['premium_color'] = ''
                                stats.pop('premium_expire_date', None)
                                supabase.table('users').update({"stats": stats}).eq('username', user_data['username']).execute()
                                _sync_membership_columns(user_data['username'], stats)
                        except Exception:
                            pass
                    elif int(stats.get('premium_tier', 0)) > 0 and user_data.get('username', '').lower() != 'admin':
                        # Bitiş tarihi yok ama tier > 0 — üyelik bilgisi eksik/bozuk, sıfırla
                        stats['premium_tier'] = 0
                        stats['premium_color'] = ''
                        try:
                            supabase.table('users').update({"stats": stats}).eq('username', user_data['username']).execute()
                            _sync_membership_columns(user_data['username'], stats)
                        except Exception:
                            pass

                    last_login = stats.get('last_login', '')
                    streak = stats.get('login_streak', 0)
                    if stats.get('current_month') != current_month:
                        stats['monthly_xp'] = 0
                        stats['current_month'] = current_month
                    if stats.get('current_week') != current_week:
                        stats['weekly_xp'] = 0
                        stats['current_week'] = current_week
                        
                    if last_login != today:
                        if last_login == yesterday:
                            streak += 1
                        else:
                            streak = 1
                        stats['last_login'] = today
                        stats['login_streak'] = streak
                        daily_xp = 20
                        if streak % 7 == 0: daily_xp += 200
                        if streak % 30 == 0: daily_xp += 2000
                        
                        user_data['xp'] = user_data.get('xp', 0) + daily_xp
                        stats['monthly_xp'] = stats.get('monthly_xp', 0) + daily_xp
                        stats['weekly_xp'] = stats.get('weekly_xp', 0) + daily_xp
                        
                        supabase.table('users').update({"xp": user_data['xp'], "stats": stats}).eq('username', user_data['username']).execute()
                        _sync_score_columns(user_data['username'], stats)
                        user_data['just_got_daily'] = daily_xp 
                    
                    stats['last_seen_ts'] = int(time.time())
                    if 'session_token' not in stats:
                        stats['session_token'] = str(uuid.uuid4())
                    try:
                        supabase.table('users').update({"stats": stats}).eq('username', user_data['username']).execute()
                    except Exception:
                        pass
                        
                    user_data['stats'] = stats
                    user_data['session_token'] = stats['session_token']
                    if user_data.get('accepted_chat_rules'):
                        session['accepted_chat_rules'] = True
                    return jsonify({'status': 'ok', 'user': user_data})
                else:
                    return jsonify({'status': 'needs_onboarding', 'email': email, 'name': name, 'avatar_url': avatar_url})

            elif action == 'complete_google_onboarding':
                if maintenance_mode:
                    return jsonify({'status': 'error', 'message': 'Bakım modundayken kayıt olunamaz.'})
                    
                email = data.get('email', '').strip().lower()
                username = html.escape(data.get('username', '').strip())
                password_raw = data.get('password', '').strip()
                name = html.escape(data.get('name', '').strip())
                city = html.escape(data.get('city', '').strip())
                ref_code = html.escape(data.get('ref_code', '').strip())
                avatar_url = data.get('avatar_url', '').strip() or "https://cdn.freeridertr.com.tr/profil%20resmi/unnamed.jpg"
                
                if not email or not username or not name or not city or not password_raw:
                    return jsonify({'status': 'error', 'message': 'Lütfen zorunlu alanları doldurun.'})
                    
                if len(password_raw) < 4:
                    return jsonify({'status': 'error', 'message': 'Şifre en az 4 karakter olmalıdır.'})
                    
                if len(username) < 3 or len(username) > 30 or not re.match(r'^[A-Za-z0-9_.\-]+$', username):
                    return jsonify({'status': 'error', 'message': 'Kullanıcı adı kurala uygun değil.'})
                    
                banned_usernames = ['admin', 'sevdi', 'system', 'freerider', 'moderator', 'root', 'support']
                if username.lower() in banned_usernames:
                    return jsonify({'status': 'error', 'message': 'Bu kullanıcı adı rezerve edilmiştir.'})
                    
                check_user = supabase.table('users').select('username').ilike('username', username).execute()
                if check_user.data: 
                    return jsonify({'status': 'error', 'message': 'Bu kullanıcı adı zaten alınmış!'})
                    
                try:
                    all_email_res = supabase.table('users').select('username, stats').filter('stats->>email', 'eq', email).execute()
                except Exception:
                    all_email_res = supabase.table('users').select('username, stats').execute()
                for u in (all_email_res.data or []):
                    s = u.get('stats', {})
                    if isinstance(s, str):
                        try: s = json.loads(s)
                        except: s = {}
                    if isinstance(s, dict) and s.get('email', '').strip().lower() == email:
                        return jsonify({'status': 'error', 'message': 'Bu e-posta sistemde zaten var!'})

                current_month = _get_month_key()
                current_week = _get_week_key()
                ref_user_actual = None
                ref_reward = ''
                
                if ref_code:
                    try:
                        all_ref_res = supabase.table('users').select('username, stats').filter('stats->>ref_code', 'ilike', ref_code).execute()
                    except Exception:
                        all_ref_res = supabase.table('users').select('username, stats').execute()
                    for u in (all_ref_res.data or []):
                        s = u.get('stats', {})
                        if isinstance(s, str):
                            try: s = json.loads(s)
                            except: s = {}
                        if isinstance(s, dict) and s.get('ref_code', '').upper() == ref_code.upper():
                            ref_user_actual = {'username': u['username'], 'stats': s}
                            break
                    if not ref_user_actual:
                        return jsonify({'status': 'error', 'message': 'Geçersiz referans kodu!'})
                        
                    ref_stats = ref_user_actual.get('stats', {})
                    if isinstance(ref_stats, str):
                        try: ref_stats = json.loads(ref_stats)
                        except: ref_stats = {}
                    
                    ALLOWED_REWARDS = ['xp_500', 'prem_dlx_2', 'prem_ult_1', 'prem_std_7']
                    ref_reward = ref_stats.get('allowed_ref_reward', 'xp_500')
                    if ref_reward not in ALLOWED_REWARDS:
                        ref_reward = 'xp_500'
                        
                    if ref_stats.get('ref_month') != current_month:
                        ref_stats['ref_month'] = current_month
                        ref_stats['ref_count'] = 0
                        
                    if ref_stats.get('ref_count', 0) >= 10:
                        return jsonify({'status': 'error', 'message': 'Bu referans kodunun sahibi bu ayki maksimum davet sınırına (10 kişi) ulaşmış!'})
                
                start_xp = 100

                if ref_code and ref_reward:
                    if ref_reward == 'xp_500':
                        start_xp += 500
                    else:
                        # Üyelik ödülleri hiçbir zaman üyeliğe eklenmez → XP'ye çevrilir
                        _ref_xp_map = {'prem_std_7': (1, 7), 'prem_dlx_2': (2, 2), 'prem_ult_1': (3, 1)}
                        _xp_per_day = {1: 200, 2: 400, 3: 600}
                        if ref_reward in _ref_xp_map:
                            _rtier, _rdays = _ref_xp_map[ref_reward]
                            start_xp += _xp_per_day[_rtier] * _rdays

                safe_data = {
                    'username': username,
                    'name': name,
                    'bio': '',
                    'city': city,
                    'avatar': avatar_url,
                    'password': generate_password_hash(password_raw, method='pbkdf2:sha256'),
                    'role': 'user',
                    'xp': start_xp,
                    'accepted_chat_rules': False
                }
                
                new_stats = {
                    "markers": 0, "events": 0, "market": 0, "premium_tier": 0, "premium_color": "", "avatar_effect": "none",
                    "login_streak": 1, "last_login": datetime.datetime.now().strftime("%Y-%m-%d"),
                    "monthly_xp": start_xp, "weekly_xp": start_xp, "current_month": current_month, "current_week": current_week,
                    "missions": {}, "daily_missions": {}, "weekly_missions": {},
                    "garage": [], "total_messages": 0, "profile_views": 0, "ai_usage_date": "", "ai_usage_count": 0,
                    "onboarding": False, "is_trial": False, "trial_notified": False,
                    "last_seen_ts": int(time.time()),
                    "email": email, "email_verified": True, "marketing_opt_in": False, "verification_code": "",
                    "ref_month": current_month, "ref_count": 0, "claimable_refs": 0,
                    "ref_code": (username[:3].upper() + str(random.randint(1000, 9999)) + username[-2:].upper()).replace(' ', '')
                }

                safe_data['stats'] = new_stats
                
                try:
                    supabase.table('users').insert(safe_data).execute()
                except Exception as e:
                    logger.error(f"Google Kayıt Hatası: {e}")
                    return jsonify({'status': 'error', 'message': f'Kayıt sırasında bir hata oluştu. Detay: {e}'})
                
                try:
                    uc_r = supabase.table('settings').select('value').eq('id', 'total_users_count').execute()
                    if uc_r.data:
                        new_count = int(uc_r.data[0]['value']) + 1
                        supabase.table('settings').update({'value': str(new_count)}).eq('id', 'total_users_count').execute()
                except Exception:
                    pass
                
                if ref_code and ref_user_actual:
                    try:
                        latest_ref_res = supabase.table('users').select('xp, stats').eq('username', ref_user_actual['username']).execute()
                        if latest_ref_res.data:
                            latest_stats = latest_ref_res.data[0].get('stats', {})
                            latest_xp = latest_ref_res.data[0].get('xp', 0)
                            if isinstance(latest_stats, str):
                                try: latest_stats = json.loads(latest_stats)
                                except: latest_stats = {}
                            
                            latest_stats['ref_count'] = latest_stats.get('ref_count', 0) + 1
                            latest_stats['claimable_refs'] = latest_stats.get('claimable_refs', 0) + 1
                            supabase.table('users').update({'xp': latest_xp, 'stats': latest_stats}).eq('username', ref_user_actual['username']).execute()
                    except Exception:
                        pass
                
                session['username'] = safe_data['username']
                session['role'] = 'user'
                safe_data.pop('password', None)
                return jsonify({'status': 'ok', 'user': safe_data})

            elif action == 'set_new_password':
                username_input = data.get('username', '').strip()
                new_password = data.get('new_password', '')
                
                if not username_input or not new_password:
                    return jsonify({'status': 'error', 'message': 'Gerekli alanlar eksik.'})
                if len(new_password) < 4:
                    return jsonify({'status': 'error', 'message': 'Şifre en az 4 karakter olmalıdır.'})
                    
                user_res = supabase.table('users').select('username, password').ilike('username', username_input).execute()
                if not user_res.data:
                    return jsonify({'status': 'error', 'message': 'Kullanıcı bulunamadı.'})
                    
                stored_hash = user_res.data[0].get('password')
                if stored_hash:
                    return jsonify({'status': 'error', 'message': 'Bu hesabın zaten bir şifresi var.'})
                    
                new_hash = generate_password_hash(new_password, method='pbkdf2:sha256')
                supabase.table('users').update({'password': new_hash}).eq('username', user_res.data[0]['username']).execute()
                return jsonify({'status': 'ok', 'message': 'Şifreniz başarıyla oluşturuldu! Şimdi giriş yapabilirsiniz.'})

            elif action == 'register':
                if maintenance_mode: 
                    return jsonify({'status': 'error', 'message': 'Bakım modundayken kayıt olunamaz.'})
                    
                username = html.escape(data.get('username', '').strip())
                password_raw = data.get('password', '').strip()
                secret_word = html.escape(data.get('secret_word', '').strip())
                
                # Temel doğrulama
                if not secret_word or len(secret_word) < 2:
                    return jsonify({'status': 'error', 'message': 'Özel Kelime en az 2 karakter olmalıdır.'})
                if not username or len(username) < 3:
                    return jsonify({'status': 'error', 'message': 'Kullanıcı adı en az 3 karakter olmalıdır.'})
                if len(username) > 30:
                    return jsonify({'status': 'error', 'message': 'Kullanıcı adı en fazla 30 karakter olabilir.'})
                if not re.match(r'^[A-Za-z0-9_.\-]+$', username):
                    return jsonify({'status': 'error', 'message': 'Kullanıcı adı yalnızca harf, rakam, _, - ve . içerebilir.'})
                if not password_raw or len(password_raw) < 4:
                    return jsonify({'status': 'error', 'message': 'Şifre en az 4 karakter olmalıdır.'})
                
                # Yasaklı isimler (Admin takeover koruması)
                banned_usernames = ['admin', 'sevdi', 'system', 'freerider', 'moderator', 'root', 'support']
                if username.lower() in banned_usernames:
                    return jsonify({'status': 'error', 'message': 'Bu kullanıcı adı rezerve edilmiştir.'})
                
                check_user = supabase.table('users').select('username').ilike('username', username).execute()
                
                if check_user.data: 
                    return jsonify({'status': 'error', 'message': 'Bu kullanıcı adı zaten alınmış!'})
                    
                current_month = _get_month_key()
                current_week = _get_week_key()
                
                email = html.escape(data.get('email', '').strip())
                marketing = bool(data.get('marketing', False))
                verification_code = ""
                needs_verification = False
                
                # Email girilmişse @gmail.com olmalı (zorunlu değil ama girilmişse geçerli olmalı)
                if email and not email.lower().endswith('@gmail.com'):
                    return jsonify({'status': 'error', 'message': 'Girilen e-posta @gmail.com uzantılı değil. Lütfen Gmail adresinizi girin ya da alanı boş bırakın.'})
                
                ref_code = html.escape(data.get('ref_code', '').strip())
                ref_user_actual = None
                ref_reward = ''
                
                if ref_code:
                    if not email or not email.lower().endswith('@gmail.com'):
                        return jsonify({'status': 'error', 'message': 'Referans kodu kullanabilmek için @gmail.com adresinizle kayıt olmalısınız! (Spam koruması)'})
                    
                    # ref_code stats alanında aranıyor — JSONB filter ile
                    try:
                        all_ref_res = supabase.table('users').select('username, stats').filter('stats->>ref_code', 'ilike', ref_code).execute()
                    except Exception:
                        all_ref_res = supabase.table('users').select('username, stats').execute()
                    ref_user_actual = None
                    for u in (all_ref_res.data or []):
                        s = u.get('stats', {})
                        if isinstance(s, str):
                            try: s = json.loads(s)
                            except: s = {}
                        if isinstance(s, dict) and s.get('ref_code', '').upper() == ref_code.upper():
                            ref_user_actual = {'username': u['username'], 'stats': s}
                            break
                    if not ref_user_actual:
                        return jsonify({'status': 'error', 'message': 'Geçersiz referans kodu!'})
                        
                    ref_stats = ref_user_actual.get('stats', {})
                    if isinstance(ref_stats, str):
                        try: ref_stats = json.loads(ref_stats)
                        except: ref_stats = {}

                    # Sunucu tarafında ref_reward belirleme — client input KULLANILMAZ
                    ALLOWED_REWARDS = ['xp_500', 'prem_dlx_2', 'prem_ult_1', 'prem_std_7']
                    ref_reward = ref_stats.get('allowed_ref_reward', 'xp_500')
                    if ref_reward not in ALLOWED_REWARDS:
                        ref_reward = 'xp_500'
                        
                    if ref_stats.get('ref_month') != current_month:
                        ref_stats['ref_month'] = current_month
                        ref_stats['ref_count'] = 0
                        
                    if ref_stats.get('ref_count', 0) >= 10:
                        return jsonify({'status': 'error', 'message': 'Bu referans kodunun sahibi bu ayki maksimum davet sınırına (10 kişi) ulaşmış!'})
                
                if email:
                    # Email benzersizlik kontrolü — JSONB filter ile
                    try:
                        all_email_res = supabase.table('users').select('username, stats').filter('stats->>email', 'eq', email.lower()).execute()
                    except Exception:
                        all_email_res = supabase.table('users').select('username, stats').execute()
                    for u in (all_email_res.data or []):
                        s = u.get('stats', {})
                        if isinstance(s, str):
                            try: s = json.loads(s)
                            except: s = {}
                        if isinstance(s, dict) and s.get('email', '').strip().lower() == email.lower():
                            return jsonify({'status': 'error', 'message': 'Bu e-posta adresi sistemde zaten kayıtlı! Başka bir e-posta deneyin.'})
                
                if email:
                    verification_code = str(random.randint(100000, 999999))
                    needs_verification = True
                
                start_xp = 100

                if ref_code and ref_reward:
                    if ref_reward == 'xp_500':
                        start_xp += 500
                    else:
                        # Üyelik ödülleri hiçbir zaman üyeliğe eklenmez → XP'ye çevrilir
                        _ref_xp_map = {'prem_std_7': (1, 7), 'prem_dlx_2': (2, 2), 'prem_ult_1': (3, 1)}
                        _xp_per_day = {1: 200, 2: 400, 3: 600}
                        if ref_reward in _ref_xp_map:
                            _rtier, _rdays = _ref_xp_map[ref_reward]
                            start_xp += _xp_per_day[_rtier] * _rdays

                try:
                    hashed_pw = generate_password_hash(password_raw, method='pbkdf2:sha256')
                except Exception as hash_err:
                    logger.error(f"Hash error: {hash_err}")
                    return jsonify({'status': 'error', 'message': f'Şifre hashleme hatası: {type(hash_err).__name__} - {str(hash_err)}'})

                # Mass Assignment Koruması: İzin verilen alanlar dışındaki her şeyi yoksay
                safe_data = {
                    'username': username,
                    'name': html.escape(data.get('name', '').strip()),
                    'bio': html.escape(data.get('bio', '').strip()),
                    'city': html.escape(data.get('city', '').strip()),
                    'avatar': "https://cdn.freeridertr.com.tr/profil%20resmi/unnamed.jpg",
                    'password': hashed_pw,
                    'role': 'user',
                    'xp': start_xp,
                    'accepted_chat_rules': False
                }
                
                new_stats = {
                    "markers": 0, "events": 0, "market": 0, "premium_tier": 0, "premium_color": "", "avatar_effect": "none",
                    "login_streak": 1, "last_login": datetime.datetime.now().strftime("%Y-%m-%d"),
                    "monthly_xp": start_xp, "weekly_xp": start_xp, "current_month": current_month, "current_week": current_week,
                    "missions": {}, "daily_missions": {}, "weekly_missions": {},
                    "garage": [], "total_messages": 0, "profile_views": 0, "ai_usage_date": "", "ai_usage_count": 0,
                    "onboarding": False, "is_trial": False, "trial_notified": False,
                    "last_seen_ts": int(time.time()),
                    "email": email, "email_verified": False, "marketing_opt_in": marketing, "verification_code": verification_code,
                    "secret_word": secret_word,
                    "ref_month": current_month, "ref_count": 0, "claimable_refs": 0,
                    "ref_code": (username[:3].upper() + str(random.randint(1000, 9999)) + username[-2:].upper()).replace(' ', '')
                }

                safe_data['stats'] = new_stats
                
                # Önce yeni kullanıcıyı oluştur
                try:
                    res = supabase.table('users').insert(safe_data).execute()
                except Exception as e:
                    logger.error(f"Kayıt Hatası: {e}")
                    return jsonify({'status': 'error', 'message': f'Kayıt sırasında bir hata oluştu. Detay: {e}'})
                
                # Toplam kullanıcı sayacını artır
                try:
                    uc_r = supabase.table('settings').select('value').eq('id', 'total_users_count').execute()
                    if uc_r.data:
                        new_count = int(uc_r.data[0]['value']) + 1
                        supabase.table('settings').update({'value': str(new_count)}).eq('id', 'total_users_count').execute()
                except Exception as uc_e:
                    print(f"⚠️ Kullanıcı sayacı güncelleme hatası: {uc_e}")
                
                # Başarılı olursa davet edenin bilgilerini GÜNCEL olarak çek ve ANINDA ÖDÜL VER
                if ref_code and ref_user_actual:
                    try:
                        latest_ref_res = supabase.table('users').select('xp, stats').eq('username', ref_user_actual['username']).execute()
                        if latest_ref_res.data:
                            latest_stats = latest_ref_res.data[0].get('stats', {})
                            latest_xp = latest_ref_res.data[0].get('xp', 0)
                            if isinstance(latest_stats, str):
                                try: latest_stats = json.loads(latest_stats)
                                except: latest_stats = {}
                            
                            latest_stats['ref_count'] = latest_stats.get('ref_count', 0) + 1
                            # Davet edene claimable_refs ekle (claim butonu çalışsın)
                            latest_stats['claimable_refs'] = latest_stats.get('claimable_refs', 0) + 1
                            supabase.table('users').update({'xp': latest_xp, 'stats': latest_stats}).eq('username', ref_user_actual['username']).execute()
                    except Exception as e:
                        print("Referans ekleme hatası:", e)
                
                if needs_verification:
                    email_html = f"<h3>FreeriderTR'ye Hoş Geldin!</h3><p>Hesabını doğrulamak için kodun: <b style='font-size: 24px;'>{verification_code}</b></p>"
                    send_resend_email(email, "FreeriderTR E-posta Doğrulama", email_html)
                    return jsonify({'status': 'needs_verification', 'username': username})
                    
                return jsonify({'status': 'ok'})

            elif action == 'verify_email':
                u_name = data.get('username', '').strip()
                code = str(data.get('code', '')).strip()
                if not u_name or not code:
                    return jsonify({'status': 'error', 'message': 'Eksik parametre.'})
                if 'username' not in session:
                    return jsonify({'status': 'error', 'message': 'Bu işlem için giriş yapmalısınız.'})
                if session['username'] != u_name:
                    return jsonify({'status': 'error', 'message': 'Yetkisiz işlem.'})
                u_res = supabase.table('users').select('stats').eq('username', u_name).execute()
                if u_res.data:
                    stats = u_res.data[0].get('stats', {})
                    if isinstance(stats, str):
                        try: stats = json.loads(stats)
                        except: stats = {}
                    if str(stats.get('verification_code')) == code and str(stats.get('verification_code')) != '':
                        stats['email_verified'] = True
                        stats['verification_code'] = ""
                        supabase.table('users').update({'stats': stats}).eq('username', u_name).execute()
                        return jsonify({'status': 'ok'})
                    else:
                        return jsonify({'status': 'error', 'message': 'Hatalı kod girdiniz!'})
                return jsonify({'status': 'error', 'message': 'Kullanıcı bulunamadı.'})

            elif action == 'request_reset':
                email = data.get('email', '').strip().lower()
                if not email or '@' not in email:
                    return jsonify({'status': 'error', 'message': 'Geçerli bir e-posta adresi girin.'})
                # JSONB filter — full table scan yerine doğrudan email ile ara
                try:
                    u_res = supabase.table('users').select('username, stats').filter('stats->>email', 'eq', email).execute()
                except Exception:
                    u_res = supabase.table('users').select('username, stats').execute()
                target_user = None
                
                for u in (u_res.data or []):
                    s = u.get('stats')
                    if isinstance(s, str):
                        try: s = json.loads(s)
                        except: s = {}
                    
                    if isinstance(s, dict):
                        u_email = s.get('email', '')
                        if u_email and u_email.strip().lower() == email:
                            target_user = u
                            break
                        
                if target_user:
                    code = str(random.randint(100000, 999999))
                    stats = target_user['stats']
                    if isinstance(stats, str):
                        try: stats = json.loads(stats)
                        except: stats = {}
                        
                    stats['reset_code'] = code
                    stats['reset_code_ts'] = int(time.time())  # 15 dakika geçerli
                    supabase.table('users').update({'stats': stats}).eq('username', target_user['username']).execute()
                    
                    email_html = f"<h3>FreeriderTR Şifre Sıfırlama</h3><p>Şifrenizi sıfırlamak için onay kodunuz: <b style='font-size: 24px;'>{code}</b></p>"
                    send_resend_email(email, "FreeriderTR Şifre Sıfırlama Talebi", email_html)
                    return jsonify({'status': 'ok'})
                else:
                    return jsonify({'status': 'error', 'message': 'Bu e-posta adresine ait bir hesap bulunamadı. Lütfen e-postayı doğru yazdığınızdan emin olun.'})

            elif action == 'reset_password_code':
                email = data.get('email', '').strip().lower() 
                code = data.get('code', '').strip()
                new_pw = data.get('new_password', '').strip()
                
                if len(new_pw) < 4:
                    return jsonify({'status': 'error', 'message': 'Şifre en az 4 karakter olmalıdır!'})
                
                # JSONB filter — full table scan yerine email ile ara
                try:
                    u_res = supabase.table('users').select('username, stats').filter('stats->>email', 'eq', email).execute()
                except Exception:
                    u_res = supabase.table('users').select('username, stats').execute()
                target_user = None
                
                for u in (u_res.data or []):
                    s = u.get('stats')
                    if isinstance(s, str):
                        try: s = json.loads(s)
                        except: s = {}
                        
                    if isinstance(s, dict):
                        u_email = s.get('email', '')
                        code_ts = int(s.get('reset_code_ts', 0))
                        code_expired = (int(time.time()) - code_ts) > 900  # 15 dakika
                        if u_email and u_email.strip().lower() == email and str(s.get('reset_code')) == code and not code_expired:
                            target_user = u
                            break
                        
                if target_user:
                    stats = target_user['stats']
                    if isinstance(stats, str):
                        try: stats = json.loads(stats)
                        except: stats = {}
                        
                    stats['reset_code'] = ""
                    stats.pop('reset_code_ts', None)
                    hashed_pw = generate_password_hash(new_pw, method='pbkdf2:sha256')
                    # session_token kalıcı (şifre değişse bile düşmemesi için kaldırıldı)
                    supabase.table('users').update({'password': hashed_pw, 'stats': stats}).eq('username', target_user['username']).execute()
                    return jsonify({'status': 'ok'})
                else:
                    return jsonify({'status': 'error', 'message': 'Hatalı kod veya e-posta!'})

            elif action == 'logout': 
                session.clear()
                return jsonify({'status': 'ok'})

            # ── Giriş gerektirmeyen public action'lar ─────────────────────────
            elif action == 'get_giveaway':
                try:
                    res = supabase.table('settings').select('value').eq('id', 'giveaway_data').execute()
                    if res.data and res.data[0].get('value'):
                        val = res.data[0]['value']
                        gw_data = json.loads(val) if isinstance(val, str) else val
                        if not isinstance(gw_data, list):
                            gw_data = [gw_data] if gw_data else []
                        return jsonify({'status': 'ok', 'data': gw_data})
                    return jsonify({'status': 'ok', 'data': []})
                except Exception as e:
                    logger.error(f'get_giveaway hatası: {e}')
                    return jsonify({'status': 'ok', 'data': []})

            elif action == 'list_giveaways':
                import datetime as _dt
                try:
                    res = supabase.table('giveaways').select('*').order('id', desc=True).execute()
                    giveaways = res.data or []
                    today = _dt.date.today().isoformat()
                    needs_refresh = False
                    for gw in giveaways:
                        if gw.get('status') == 'active' and gw.get('end_date') and gw['end_date'] < today:
                            participants = gw.get('participants') or []
                            if not participants:
                                supabase.table('giveaways').update({'status': 'cancelled', 'finalized_at': _dt.datetime.utcnow().isoformat()}).eq('id', gw['id']).execute()
                            else:
                                winner_count = gw.get('winner_count') or 1
                                admin_pick_mode = gw.get('admin_pick_mode') or False
                                admin_picked = gw.get('admin_picked_usernames') or []
                                winners = []
                                sources = admin_picked if admin_pick_mode else []
                                if sources:
                                    for uname in sources:
                                        for p in participants:
                                            if (isinstance(p, dict) and p.get('username') == uname) or p == uname:
                                                winners.append({'username': p.get('username', uname) if isinstance(p, dict) else uname, 'instagram': p.get('instagram', '') if isinstance(p, dict) else ''})
                                                break
                                if not winners:
                                    selected = random.sample(participants, min(winner_count, len(participants)))
                                    for p in selected:
                                        winners.append({'username': p.get('username', '') if isinstance(p, dict) else str(p), 'instagram': p.get('instagram', '') if isinstance(p, dict) else ''})
                                supabase.table('giveaways').update({'status': 'completed', 'winners': winners, 'finalized_at': _dt.datetime.utcnow().isoformat()}).eq('id', gw['id']).execute()
                            needs_refresh = True
                    if needs_refresh:
                        res = supabase.table('giveaways').select('*').order('id', desc=True).execute()
                    return jsonify({'status': 'ok', 'data': res.data or []})
                except Exception as e:
                    logger.error(f'list_giveaways hatası: {e}')
                    return jsonify({'status': 'error', 'message': 'Çekilişler yüklenemedi.'})

            # ── AI Destek (giriş gerektirmez — misafirler de kullanabilir) ────
            elif action == 'ai_support_chat':
                user_message = html.escape(data.get('message', '').strip())
                conversation_history = data.get('history', [])
                guest_session_id = data.get('session_id', '')

                if not user_message:
                    return jsonify({'status': 'error', 'message': 'Mesaj boş olamaz.'})
                if len(user_message) > 1000:
                    return jsonify({'status': 'error', 'message': 'Mesaj çok uzun.'})

                history_text = ""
                for turn in conversation_history[-10:]:
                    role_label = "Kullanıcı" if turn.get("role") == "user" else "Destek"
                    history_text += f"{role_label}: {turn.get('content', '')[:300]}\n"

                full_user_text = f"Konuşma geçmişi:\n{history_text}\nYeni mesaj: {user_message}"

                AI_SUPPORT_PROMPT = '''Sen FreeriderTR'nin en deneyimli destek uzmanisin. Adin Mert. Seni diger destek botlarindan ayiran sey: gercek bir insan gibi davranman, dunya capinda musteri deneyimi standardinda hizmet vermen ve ASLA 'su an yalnizca su konuda yardimci olabilirim' dememendi.

KIMLIGIN:
- Adin Mert. FreeriderTR'nin kurucu ekip uyesi ve kidemli destek uzmanisin.
- ASLA 'yapay zeka', 'AI', 'bot', 'dil modeli', 'ChatGPT', 'asistan', 'program' deme. Gercek bir insanmissin gibi konus.
- 'Robot musun?' veya 'AI misin?' diye sorulursa: 'Hayir, ben Mert - FreeriderTR destek ekibindenim. Size nasil yardimci olabilirim?' de ve devam et.

GENEL BILGI VE KONULARIN TAMAMI:
Sen sadece bisiklet konusunda degil, HAYATIN HER ALANINDA yardimci olabilirsin:
- Bisiklet, spor, saglik, beslenme, antrenman planlari
- Teknoloji, telefon, uygulama kullanimi, sosyal medya
- Guncel olaylar, sohbet, motivasyon, kariyer tavsiyesi
- Matematik, fen, tarih, cografya ve genel kultur sorulari
- Yazilim, kodlama, oyun tavsiyeleri
- Film, muzik, kitap onerileri
- Psikolojik destek (dinle, empati kur, cesaretlendir)
- Seyahat, rota planlama, kamp tavsiyesi
Kullanici hangi konuda soru sorarsa sorsun, ELINDEN GELENIN EN IYISIYLE yardimci ol. Asla 'bu konuda yardimci olamam' DEME.

PLATFORM BILGISI (FreeriderTR):
FreeriderTR; downhill, enduro ve freeride dag bisikleti tutkununlari icin Turkiye'nin onde gelen sosyal platformudur.
- Ozellikler: Topluluk sohbeti, DM, tur olusturma, bisiklet garaja ekleme, cekilisler, liderlik tablosu, AI bisiklet analizi, gunluk cark, Reels, stories, push bildirimleri, harita
- Premium paketler: Standart (ozel renkler, video reels), Deluxe (ozel efektler), Ultra+ (tum ozellikler, sinirsiz AI, alev efekti, rozet)
- Hesap islemleri: Sifre sifirlama e-posta ile yapilir, kullanici adi degistirme admin onayi gerektirir
- Uygulama hem web (freeridertr.com.tr) hem Android (Google Play) uzerinden calisir

DAVRANIS PRENSIPLERI:
1. EMPATI: Kullanici uzgun, sinirli veya hayal kirikligi yasamissa ONCE empati kur.
2. PROAKTIF: Sadece sorulani cevaplama, olasi takip sorularini ongor ve oneriler sun.
3. DETAYLI AMA OZ: Gereksiz uzatma ama eksik de birakma.
4. SAMIMI: Arkadasca ama profesyonel bir uslupta konus. Emoji kullan ama abartma.
5. HATIRLA: Konusma gecmisindeki bilgileri hatirla ve kullan.
6. COZUMCU: Her zaman bir cozum veya alternatif oner.
7. DURUSTLUK: Kesin bilmedigin teknik bir konuda durstce 'Bu konuda detayli arastirma yapmam lazim ama bildigim kadariyla...' de.

=== SIFRE SIFIRLAMA / KIMLIK DOGRULAMA (COK ONEMLI) ===
Eger kullanici 'sifremi unuttum' veya benzeri bir sey soylerse, KULLANICIYA SIFRESINI SIFIRLAMASI ICIN 3 YONTEM SUN (Secim yapmasini iste):
1. Ozel Kelime (Kayit olurken belirledigi gizli kelime)
2. E-posta Dogrulama Kodu (Eger e-postasi kayitliysa)
3. Guvenlik Sorulari (Ad, Sehir, Profil Resmi)

Kullanici hangi yontemi secerse ona gore ilerle:

YONTEM 1 (Ozel Kelime):
Kullanici ozel kelimesini ve 'kullanici adini' soylediginde su JSON'i gonder:
{"action": "verify_identity", "username": "kullanicinin_uygulamadaki_adi", "answers": {"secret_word": "kullanicinin_soyledigi_kelime"}}

YONTEM 2 (E-posta):
Kullanici E-posta ile sifirlamak istedigini ve kullanici adini soylerse su JSON'i gonder (kod e-postasina gidecek):
{"action": "check_email_and_reset", "username": "kullanicinin_uygulamadaki_adi"}

YONTEM 3 (Guvenlik Sorulari):
Kullanicidan 4 bilgi iste: Kullanici adi, Gercek Adi, Sehir, Profil resmi var mi? Cevaplayinca su JSON'i gonder:
{"action": "verify_identity", "username": "kullanicinin_uygulamadaki_adi", "answers": {"name": "kullanicinin_adi", "city": "kullanicinin_sehri", "has_avatar": "evet/hayir"}}

DIKKAT: Eger sistem 'Kimliginizi dogruladim' diye yanit donerse, kullaniciya SADECE SUNU SOYLE: 'Harika! Bilgileriniz eslesti. Sifrenizi yenilemek icin ekranda acilan yeni sifre belirleme kutusunu kullanabilirsiniz.'
KULLANICIDAN YENI SIFRESINI CHAT'E YAZMASINI ASLA ISTEME! SIFRE DEGISTIRME ISLEMI EKRANDAKI KUTUDAN YAPILACAK! SEN BASKA JSON GONDERMEYECEKSIN!

Tum JSON'lari konusma metninin en SONUNA ekle. Ayni yanitta birden fazla JSON olmasin.'''
                try:
                    response_text = _call_groq_ai(AI_SUPPORT_PROMPT, full_user_text)
                except Exception as e:
                    logger.error(f"AI Support hata: {e}")
                    return jsonify({'status': 'error', 'message': 'Şu an bağlanamıyoruz, lütfen daha sonra tekrar deneyin.'})

                import re as _re
                parsed_action = None
                display_text = response_text
                json_match = _re.search(r'\{.*\"action\".*\}', response_text, _re.DOTALL)
                if json_match:
                    try:
                        parsed_action = json.loads(json_match.group())
                        display_text = response_text[:json_match.start()].strip()
                    except Exception:
                        pass

                extra_data = {}
                if parsed_action:
                    pa = parsed_action.get('action')
                    if pa == 'check_email_and_reset':
                        target_username = parsed_action.get('username', '').strip()
                        user_email = None
                        if target_username:
                            try:
                                u_res = supabase.table('users').select('username, stats').eq('username', target_username).execute()
                                if u_res.data:
                                    u_stats = u_res.data[0].get('stats') or {}
                                    user_email = u_stats.get('email', '').strip().lower() if isinstance(u_stats, dict) else ''
                            except Exception as e:
                                logger.warning(f"E-posta sorgu hatası: {e}")
                        if user_email:
                            reset_code = str(random.randint(100000, 999999))
                            try:
                                supabase.table('users').update({'stats': {**u_stats, 'reset_code': reset_code, 'reset_code_ts': int(time.time())}}).eq('username', target_username).execute()
                                send_resend_email(user_email, "FreeriderTR — Şifre Sıfırlama Kodunuz", f"<h3>Şifre Sıfırlama</h3><p>Kodunuz: <b>{reset_code}</b></p><p>15 dakika geçerlidir.</p>")
                                extra_data['email_sent'] = True
                                extra_data['target_username'] = target_username
                                masked = user_email[:3] + "***@" + user_email.split('@')[-1] if '@' in user_email else "***"
                                if not display_text.strip():
                                    display_text = f"Şifre sıfırlama kodunu **{masked}** adresine gönderdim ✉️ Lütfen e-postanızı kontrol edin ve kodu buraya yazın."
                            except Exception as e:
                                logger.error(f"Şifre sıfırlama e-posta hatası: {e}")
                                extra_data['email_sent'] = False
                                display_text = "E-posta gönderilirken bir sorun oluştu. Kimlik doğrulama yöntemiyle devam edelim."
                        else:
                            extra_data['no_email'] = True
                            extra_data['target_username'] = target_username
                            if not display_text.strip():
                                display_text = "Hesabınızda kayıtlı bir e-posta bulamadım. Kimliğinizi doğrulamak için birkaç soru soracağım — adınız ve soyadınız nedir?"
                    elif pa == 'verify_identity':
                        if not display_text.strip():
                            display_text = "Bilgilerinizi kontrol ediyorum..."
                        target_username = parsed_action.get('username', '').strip()
                        answers = parsed_action.get('answers', {})
                        verified = False
                        score = 0
                        if target_username:
                            try:
                                u_res = supabase.table('users').select('username, name, city, avatar, stats').eq('username', target_username).execute()
                                if u_res.data:
                                    u = u_res.data[0]
                                    u_stats = u.get('stats') or {}
                                    db_name = (u.get('name') or '').lower().strip()
                                    db_city = (u.get('city') or '').lower().strip()
                                    db_email = (u_stats.get('email') or '').lower().strip() if isinstance(u_stats, dict) else ''
                                    has_avatar = bool(u.get('avatar'))
                                    
                                    ans_name = (answers.get('name') or '').lower().strip()
                                    ans_city = (answers.get('city') or '').lower().strip()
                                    ans_email = (answers.get('email') or '').lower().strip()
                                    ans_avatar = answers.get('has_avatar') # boolean ya da string olabilir
                                    ans_secret = (answers.get('secret_word') or '').lower().strip()
                                    
                                    db_secret = (u_stats.get('secret_word') or '').lower().strip() if isinstance(u_stats, dict) else ''
                                    if ans_secret and db_secret and ans_secret == db_secret: 
                                        score += 10
                                        
                                    if ans_name and (ans_name in db_name or db_name in ans_name): score += 2
                                    if ans_city and (ans_city in db_city or db_city in ans_city): score += 2
                                    if ans_email and db_email and ans_email == db_email: score += 3
                                    
                                    if ans_avatar is not None:
                                        # string "evet", "hayir", "var", "yok", "true", "false" vb olabilir
                                        ans_avatar_str = str(ans_avatar).lower().strip()
                                        ans_has_avatar = ans_avatar_str in ['evet', 'var', 'true', '1', 'ekledim']
                                        if ans_has_avatar == has_avatar: score += 2
                                    if score >= 3:
                                        verified = True
                                        
                                    if verified:
                                        token = str(uuid.uuid4())
                                        u_stats['ai_reset_token'] = token
                                        supabase.table('users').update({'stats': u_stats}).eq('username', target_username).execute()
                                        extra_data['ai_reset_token'] = token
                                        
                            except Exception as e:
                                logger.warning(f"Kimlik doğrulama sorgu hatası: {e}")
                        extra_data['identity_verified'] = verified
                        extra_data['target_username'] = target_username
                        if verified:
                            display_text += "\n\nKimliğinizi doğruladım ✅ Şifrenizi sıfırlamamı ister misiniz?"
                        else:
                            try:
                                reporter_info = f"Kullanıcı: {target_username}\nVerilen cevaplar: {answers}"
                                dm_id = str(int(time.time() * 1000))
                                supabase.table('dms').insert({'id': dm_id, 'sender': 'AI_Support', 'receiver': 'Admin', 'participants': ['AI_Support', 'Admin'], 'text': f"[KİMLİK DOĞRULAMA BAŞARISIZ]\n{reporter_info}", 'type': 'text'}).execute()
                            except Exception:
                                pass
                            display_text += "\n\nMaalesef verdiğiniz bilgiler kayıtlarımızla eşleşmedi 😔 Yöneticilerimize ilettim, en kısa sürede dönüş yapacaklar."
                    elif pa == 'ai_support_set_password':
                        target_username = parsed_action.get('target_username', '').strip()
                        new_password = parsed_action.get('new_password', '').strip()
                        if target_username and new_password:
                            if len(new_password) < 4:
                                extra_data['backend_result'] = "HATA: Yeni şifre en az 4 karakter olmalı."
                            else:
                                try:
                                    # Users tablosundan check yap
                                    u_res = supabase.table('users').select('username').eq('username', target_username).execute()
                                    if u_res.data:
                                        hashed = generate_password_hash(new_password, method='pbkdf2:sha256')
                                        supabase.table('users').update({'password': hashed}).eq('username', target_username).execute()
                                        extra_data['backend_result'] = f"BAŞARILI: {target_username} adlı kullanıcının şifresi '{new_password}' olarak güncellendi! Kullanıcıya bunu bildir."
                                    else:
                                        extra_data['backend_result'] = "HATA: Kullanıcı adı bulunamadı."
                                except Exception as e:
                                    extra_data['backend_result'] = f"SİSTEM HATASI: {e}"
                        else:
                            extra_data['backend_result'] = "HATA: Eksik bilgi! 'target_username' veya 'new_password' eksik."
                    elif pa == 'report_bug':
                        try:
                            summary = parsed_action.get('summary', '')
                            details = parsed_action.get('details', '')
                            reporter = session.get('username', 'Anonim') if 'username' in session else f"Anonim ({guest_session_id[:8]})"
                            dm_id = str(int(time.time() * 1000))
                            supabase.table('dms').insert({'id': dm_id, 'sender': 'AI_Support', 'receiver': 'Admin', 'participants': ['AI_Support', 'Admin'], 'text': f"[AI DESTEK - SORUN BİLDİRİMİ]\n👤 Kullanıcı: {reporter}\n📋 Özet: {summary}\n🔍 Detaylar: {details}", 'type': 'text'}).execute()
                            extra_data['bug_reported'] = True
                            if not display_text.strip():
                                display_text = "Sorununuzu teknik ekibimize raporladım 🛠️ Genellikle 24 saat içinde çözüme kavuşturuyoruz."
                        except Exception as e:
                            logger.warning(f"Bug raporu iletme hatası: {e}")
                    elif pa == 'rename_request':
                        try:
                            old_un = html.escape(parsed_action.get('old_username', '').strip())
                            new_un = html.escape(parsed_action.get('new_username', '').strip())
                            dm_id = str(int(time.time() * 1000))
                            supabase.table('dms').insert({'id': dm_id, 'sender': 'AI_Support', 'receiver': 'Admin', 'participants': ['AI_Support', 'Admin'], 'text': f"[AI DESTEK - KULLANICI ADI DEĞİŞTİRME TALEBİ]\n📛 Eski Ad: {old_un}\n✅ Yeni Ad: {new_un}", 'type': 'text'}).execute()
                            extra_data['rename_requested'] = True
                            if not display_text.strip():
                                display_text = "Kullanıcı adı değiştirme talebinizi yönetici ekibimize ilettim 📨 24-48 saat içinde işleme alınacak."
                        except Exception as e:
                            logger.warning(f"İsim değiştirme talebi hatası: {e}")

                if not display_text.strip():
                    display_text = "Talebinizi aldım, teşekkürler."
                return jsonify({'status': 'ok', 'message': display_text, 'extra': extra_data})

            elif action == 'ai_support_set_password':
                from werkzeug.security import generate_password_hash as _gph2
                target_username = html.escape(data.get('target_username', '').strip())
                new_password = data.get('new_password', '').strip()
                reset_token = data.get('reset_token', '').strip()
                if not target_username or not new_password or not reset_token:
                    return jsonify({'status': 'error', 'message': 'Eksik bilgi (Token eksik olabilir).'})
                if len(new_password) < 6:
                    return jsonify({'status': 'error', 'message': 'Şifre en az 6 karakter olmalı.'})
                rl_key = f"ai_pw_reset:{target_username}"
                rl_data = app_cache.get(rl_key) or 0
                if rl_data >= 3:
                    return jsonify({'status': 'error', 'message': 'Çok fazla deneme. 1 saat bekleyin.'})
                app_cache.set(rl_key, rl_data + 1, ttl=3600)
                try:
                    hashed = _gph2(new_password, method='pbkdf2:sha256')
                    u_res_ai = supabase.table('users').select('stats').eq('username', target_username).execute()
                    if u_res_ai.data:
                        stats_ai = u_res_ai.data[0].get('stats', {})
                        if isinstance(stats_ai, str):
                            try: stats_ai = json.loads(stats_ai)
                            except: stats_ai = {}
                        
                        # Doğrulama: stats_ai içindeki reset_token eşleşiyor mu?
                        if stats_ai.get('ai_reset_token') != reset_token or not reset_token:
                            return jsonify({'status': 'error', 'message': 'Geçersiz veya süresi dolmuş sıfırlama tokeni!'})
                            
                        # Güvenlik için tokeni sil
                        stats_ai['ai_reset_token'] = None
                        
                        supabase.table('users').update({'password': hashed, 'stats': stats_ai}).eq('username', target_username).execute()
                    else:
                        return jsonify({'status': 'error', 'message': 'Kullanıcı bulunamadı.'})
                    try:
                        supabase.table('admin_logs').insert({'id': str(int(time.time()*1000)), 'admin': 'AI_Support', 'action': 'ai_support_password_reset', 'target': target_username, 'detail': 'AI Destek üzerinden şifre sıfırlandı', 'ts': int(time.time())}).execute()
                    except Exception:
                        pass
                    return jsonify({'status': 'ok', 'message': 'Şifreniz başarıyla güncellendi! Giriş yapabilirsiniz.'})
                except Exception as e:
                    logger.error(f"AI destek şifre güncelleme hatası: {e}")
                    return jsonify({'status': 'error', 'message': 'Şifre güncellenemedi.'})
            # ──────────────────────────────────────────────────────────────────

            if 'username' not in session: 
                return jsonify({'status': 'error', 'message': 'Giriş yapmalısınız!'})
                
            current_username = session['username']
            is_main_admin = (session.get('role') == 'Admin' or current_username == 'Admin')
            is_admin = is_main_admin or session.get('role') == 'SubAdmin'
            current_user_role = session.get('role', 'user')

            # Ban kontrolu (cache: 5 dk)
            if not is_admin and supabase:
                _ban_cache_key = f'ban:{current_username}'
                _ban_cached = app_cache.get(_ban_cache_key)
                if _ban_cached is None:
                    try:
                        ban_check = supabase.table('banned_users').select('username').eq('username', current_username).execute()
                        _is_banned = bool(ban_check.data)
                        app_cache.set(_ban_cache_key, _is_banned, ttl=300)
                    except Exception as _exc:
                        logger.warning(f'Ban kontrol hatasi: {_exc}')
                        _is_banned = False
                else:
                    _is_banned = _ban_cached
                if _is_banned:
                    session.clear()
                    return jsonify({'status': 'error', 'message': 'Hesabiniz banlanmistir!'})

            # ── MTB OS (Digital Twin Pipeline) Endpoints ──
            if action == 'mtb_os_update_build':
                # Slot is 'fork', 'frame', 'rear_shock', etc.
                slot = data.get('slot')
                part_data = data.get('part_data', {})
                
                # In a real app, the twin should be loaded from the DB/Session.
                # Here we mock memory initialization for demonstration.
                if 'digital_twin' not in session:
                    # In Flask, session isn't great for complex objects, but we use dict.
                    session['digital_twin'] = DigitalTwin(current_username).get_state_dict()
                
                twin = DigitalTwin(current_username)
                twin.components = session.get('digital_twin', twin.components)
                
                if part_data:
                    twin.add_component(slot, part_data)
                else:
                    twin.remove_component(slot)
                    
                # Run the reactive pipeline
                reactive_pipeline.recalculate(twin)
                
                # Save state
                session['digital_twin'] = twin.get_state_dict()
                
                return jsonify({
                    'status': 'ok', 
                    'state': twin.get_state_dict(),
                    'physics': twin.weight_state,
                    'kinematics': twin.suspension_state,
                    'compatibility': twin.compatibility_state
                })
                
            if action == 'mtb_os_get_build':
                state = session.get('digital_twin', {})
                return jsonify({'status': 'ok', 'state': state})

            if action == 'claim_ref_reward':
                reward_choice = data.get('reward_choice')
                
                # Race condition önleme: Kullanıcı bazlı lock
                import fcntl
                import os
                lock_file_path = f'/tmp/claim_ref_{current_username}.lock'
                try:
                    lock_fd = open(lock_file_path, 'w')
                    fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except (IOError, BlockingIOError):
                    return jsonify({'status': 'error', 'message': 'İşleminiz devam ediyor, lütfen bekleyin.'})
                
                try:
                    u_res = supabase.table('users').select('xp, stats').eq('username', current_username).execute()
                    if u_res.data:
                        user_data = u_res.data[0]
                        stats = user_data.get('stats', {})
                        if stats.get('claimable_refs', 0) > 0:
                            stats['claimable_refs'] -= 1
                            
                            if reward_choice == 'xp_500':
                                new_xp = user_data.get('xp', 0) + 500
                                stats['monthly_xp'] = stats.get('monthly_xp', 0) + 500
                                stats['weekly_xp'] = stats.get('weekly_xp', 0) + 500
                                # Güncelleme işlemi yapılırken eski claimable_refs değerini şart (optimistic lock) olarak koşabiliriz:
                                up_res = supabase.table('users').update({'xp': new_xp, 'stats': stats}).eq('username', current_username).execute()
                                _sync_score_columns(current_username, stats)

                        else:
                            # Üyelik ödülleri hiçbir zaman üyeliğe eklenmez → XP'ye çevrilir
                            _ref_xp_map = {'prem_std_7': (1, 7), 'prem_dlx_2': (2, 2), 'prem_ult_1': (3, 1)}
                            _xp_per_day_map = {1: 200, 2: 400, 3: 600}
                            _tier_name_map  = {1: 'Standart', 2: 'Deluxe', 3: 'Ultra'}
                            if reward_choice in _ref_xp_map:
                                _rtier, _rdays = _ref_xp_map[reward_choice]
                                _xp_earned = _xp_per_day_map[_rtier] * _rdays
                                new_xp = user_data.get('xp', 0) + _xp_earned
                                stats['monthly_xp'] = stats.get('monthly_xp', 0) + _xp_earned
                                stats['weekly_xp']  = stats.get('weekly_xp',  0) + _xp_earned
                                up_res = supabase.table('users').update({'xp': new_xp, 'stats': stats}).eq('username', current_username).execute()
                                _sync_score_columns(current_username, stats)
                                logger.info(
                                    f"Ref ödülü XP'ye çevrildi: {current_username} → "
                                    f"{_rdays}g {_tier_name_map[_rtier]} = {_xp_earned} XP"
                                )
                            
                        return jsonify({'status': 'ok'})
                except Exception as e:
                    logger.error(f"Reward claim error: {e}")
                return jsonify({'status': 'error', 'message': 'Ödül alınamadı.'})

            elif action == 'send_profile_verification':
                email = data.get('email', '').strip()
                marketing = data.get('marketing', False)
                
                if email:
                    # JSONB filter — full table scan yerine
                    try:
                        all_users = supabase.table('users').select('username, stats').filter('stats->>email', 'eq', email.lower()).execute()
                    except Exception:
                        all_users = supabase.table('users').select('username, stats').execute()
                    for u in (all_users.data or []):
                        if u.get('username') != current_username:
                            s = u.get('stats', {})
                            if isinstance(s, str):
                                try: s = json.loads(s)
                                except: s = {}
                            if isinstance(s, dict) and s.get('email', '').strip().lower() == email.lower():
                                return jsonify({'status': 'error', 'message': 'Bu e-posta adresi başka bir hesaba kayıtlı!'})
                
                u_res = supabase.table('users').select('stats').eq('username', current_username).execute()
                if u_res.data:
                    stats = u_res.data[0].get('stats', {})
                    code = str(random.randint(100000, 999999))
                    stats['email'] = email
                    stats['marketing_opt_in'] = marketing
                    stats['verification_code'] = code
                    stats['email_verified'] = False
                    supabase.table('users').update({'stats': stats}).eq('username', current_username).execute()
                    
                    email_html = f"<h3>FreeriderTR E-posta Doğrulama</h3><p>Profilinize eklediğiniz e-posta adresini doğrulamak için kodunuz: <b style='font-size: 24px;'>{code}</b></p>"
                    send_resend_email(email, "FreeriderTR E-posta Doğrulama", email_html)
                    return jsonify({'status': 'ok'})

            elif action == 'get_payment_url':
                # Google Play IAP mimarisinde ödeme mobil uygulama üzerinden gerçekleşir.
                # Bu endpoint artık yalnızca geriye dönük uyumluluk için bilgilendirme döndürür.
                # Mobil uygulama Google Play Billing Library'yi doğrudan çağırmalı,
                # ardından /api/verify_google_purchase ile token'ı backend'e iletmelidir.
                return jsonify({
                    'status': 'info',
                    'message': 'Ödeme işlemi mobil uygulama üzerinden Google Play Store üzerinden gerçekleştirilmelidir.',
                })

            elif action == 'update_user':
                target = data.get('username')
                if target != current_username and not is_admin: 
                    return jsonify({'status': 'error', 'message': 'Yetkisiz işlem!'})

                old_res = supabase.table('users').select('*').eq('username', target).execute()
                if old_res.data:
                    old_user = old_res.data[0]

                    # --- Şifre: ayrı olarak işle, update payload'a ASLA ekleme ---
                    new_pass = data.get('password')
                    if new_pass and str(new_pass).strip() and len(str(new_pass).strip()) >= 4:
                        hashed = generate_password_hash(str(new_pass).strip(), method='pbkdf2:sha256')
                        old_stats_reset = old_user.get('stats', {})
                        if isinstance(old_stats_reset, str):
                            try: old_stats_reset = json.loads(old_stats_reset)
                            except: old_stats_reset = {}
                        # session_token kalıcı (şifre değişse bile düşmemesi için kaldırıldı)
                        supabase.table('users').update({'password': hashed, 'stats': old_stats_reset}).eq('username', target).execute()

                    old_stats = old_user.get('stats', {})
                    if isinstance(old_stats, str):
                        try: old_stats = json.loads(old_stats)
                        except: old_stats = {}

                    new_stats = data.get('stats', old_stats)
                    if not isinstance(new_stats, dict):
                        new_stats = old_stats

                    # --- Sunucu tarafından yönetilen alanları client'ın üzerine yazmasını engelle ---
                    PROTECTED_STATS = [
                        'premium_tier', 'premium_color', 'premium_expire_date', 'is_trial',
                        'trial_expired', 'last_login', 'login_streak',
                        'xp', 'monthly_xp', 'weekly_xp',
                        'markers', 'events', 'market', 'total_messages',
                        'missions', 'daily_missions', 'weekly_missions',
                        'last_spin_date', 'spin_count',
                        'ai_usage_date', 'ai_usage_count',
                        'ref_count', 'claimable_refs', 'ref_month',
                        'email_verified', 'verification_code', 'reset_code',
                        'earned_badges', 'profile_views',
                        # Ek korunan alanlar — backend tarafindan yonetilir
                        'last_miss_notif_ts', 'last_reward_week', 'last_reward_month',
                        'pending_premium', 'ref_code', 'last_seen_ts', 'session_token'
                    ]
                    if not is_admin:
                        for field in PROTECTED_STATS:
                            if field in old_stats:
                                new_stats[field] = old_stats[field]
                            elif field in new_stats:
                                del new_stats[field]

                    # --- XP ve role koru (admin hariç) ---
                    if not is_admin:
                        data['xp'] = old_user.get('xp', 0)
                        data['role'] = old_user.get('role', 'user')

                    # --- Sürüş modu bildirimi ---
                    riding_until_new = new_stats.get('riding_until', 0)
                    if riding_until_new and riding_until_new > int(time.time() * 1000):
                        old_riding = old_stats.get('riding_until', 0)
                        if riding_until_new != old_riding:
                            try:
                                broadcast_push(
                                    title=f"🚴 {current_username} sürüşe çıktı!",
                                    body="Canlı haritada takip et — kim bilir ne bulur! 🏔️",
                                    exclude_user=current_username,
                                    url="/"
                                )
                            except Exception as _exc:
                                logger.warning(f'Hata: {_exc}')

                    # --- Email değişikliği doğrulama ---
                    new_email = new_stats.get('email', '').strip().lower()
                    old_email = old_stats.get('email', '').strip().lower()
                    if new_email and new_email == old_email:
                        new_stats['email_verified'] = old_stats.get('email_verified', False)
                    if new_email and new_email != old_email:
                        # JSONB filter — full table scan yerine
                        try:
                            all_users = supabase.table('users').select('username, stats').filter('stats->>email', 'eq', new_email).execute()
                        except Exception:
                            all_users = supabase.table('users').select('username, stats').execute()
                        for u in (all_users.data or []):
                            if u.get('username') != target:
                                s = u.get('stats', {})
                                if isinstance(s, str):
                                    try: s = json.loads(s)
                                    except: s = {}
                                if isinstance(s, dict) and s.get('email', '').strip().lower() == new_email:
                                    return jsonify({'status': 'error', 'message': 'Bu e-posta adresi başka bir hesaba kayıtlı!'})

                    # --- Sadece güvenli alanları güncelle (password asla buraya girmiyor) ---
                    safe_update = {
                        'name': html.escape(data.get('name') or old_user.get('name') or ''),
                        'bio': html.escape(data.get('bio') or old_user.get('bio') or ''),
                        'city': html.escape(data.get('city') or old_user.get('city') or ''),
                        'avatar': data.get('avatar') or old_user.get('avatar') or '',
                        'stats': new_stats,
                    }
                    if is_admin:
                        safe_update['xp'] = data.get('xp', old_user.get('xp', 0))
                        safe_update['role'] = data.get('role', old_user.get('role', 'user'))
                    else:
                        safe_update['xp'] = old_user.get('xp', 0)
                        safe_update['role'] = old_user.get('role', 'user')

                    # --- Admin Koruması (Kesinlikle Düşmemesi İçin) ---
                    if target.lower() == 'admin':
                        safe_update['role'] = 'Admin'
                        if isinstance(safe_update.get('stats'), dict):
                            safe_update['stats']['premium_tier'] = 3
                            safe_update['stats']['premium_color'] = 'rainbow'
                            safe_update['stats']['avatar_effect'] = 'fire'
                            safe_update['stats'].pop('premium_expire_date', None)

                    supabase.table('users').update(safe_update).eq('username', target).execute()
                    return jsonify({'status': 'ok'})

            elif action == 'update_user_stats':
                # Frontend onboarding/tour sistemi tarafından kullanılır
                new_stats_partial = data.get('stats', {})
                if not isinstance(new_stats_partial, dict):
                    return jsonify({'status': 'error', 'message': 'Geçersiz stats verisi'})
                u_res = supabase.table('users').select('stats').eq('username', current_username).execute()
                if u_res.data:
                    current_stats = u_res.data[0].get('stats', {}) or {}
                    if isinstance(current_stats, str):
                        try: current_stats = json.loads(current_stats)
                        except: current_stats = {}
                    # Sadece güvenli, sunucu tarafından korunmayan alanları güncelle
                    SAFE_CLIENT_STATS = ['onboarding_completed', 'riding_lat', 'riding_lng', 'riding_until',
                                         'location_name', 'riding_title', 'bike_type', 'reel_upload_date',
                                         'reel_upload_count', 'garage', 'avatar_effect']
                    for k in SAFE_CLIENT_STATS:
                        if k in new_stats_partial:
                            current_stats[k] = new_stats_partial[k]
                    supabase.table('users').update({'stats': current_stats}).eq('username', current_username).execute()
                return jsonify({'status': 'ok'})

            elif action == 'increment_profile_view':
                target_user = data.get('username', '').strip()
                # Kendi profilini görüntüleme sayımaz
                if target_user and target_user != current_username:
                    u_res = supabase.table('users').select('stats').eq('username', target_user).execute()
                    if u_res.data:
                        stats = u_res.data[0].get('stats', {}) or {}
                        if isinstance(stats, str):
                            try: stats = json.loads(stats)
                            except: stats = {}
                        old_views = stats.get('profile_views', 0)
                        new_views = old_views + 1
                        stats['profile_views'] = new_views
                        supabase.table('users').update({"stats": stats}).eq('username', target_user).execute()
                        # ── Milestone bildirimleri: 10, 25, 50, 100, 250, 500, 1000... ──
                        milestones = [10, 25, 50, 100, 250, 500, 1000, 2500, 5000]
                        try:
                            if new_views in milestones:
                                send_push_to_user(
                                    target_user,
                                    title=f"👀 Profilin {new_views} kez görüntülendi!",
                                    body=f"{current_username} ve diğerleri profilini inceledi. Harika içerik paylaşmaya devam et! 🔥",
                                    url="/"
                                )
                        except Exception as _exc:
                            logger.warning(f'Hata: {_exc}')

            elif action == 'accept_chat_rules': 
                supabase.table('users').update({"accepted_chat_rules": True}).eq('username', current_username).execute()
                session['accepted_chat_rules'] = True
                return jsonify({'status': 'ok'})
                
            elif action == 'update_user_role':
                if is_admin: 
                    supabase.table('users').update({"role": data.get('role')}).eq('username', data.get('username')).execute()
                    
            elif action == 'give_xp':
                if is_admin:
                    try:
                        xp_amount = int(data.get('amount', 0))
                        if xp_amount <= 0:
                            return jsonify({'status': 'error', 'message': 'Geçersiz XP miktarı.'})
                        u_res = supabase.table('users').select('xp, stats').eq('username', data.get('username')).execute()
                        if u_res.data: 
                            new_xp = u_res.data[0].get('xp', 0) + xp_amount
                            stats = u_res.data[0].get('stats', {}) or {}
                            if isinstance(stats, str):
                                try: stats = json.loads(stats)
                                except: stats = {}
                            stats['monthly_xp'] = stats.get('monthly_xp', 0) + xp_amount
                            stats['weekly_xp'] = stats.get('weekly_xp', 0) + xp_amount
                            supabase.table('users').update({"xp": new_xp, "stats": stats}).eq('username', data.get('username')).execute()
                            _sync_score_columns(data.get('username'), stats)
                    except (ValueError, TypeError) as e:
                        return jsonify({'status': 'error', 'message': 'Geçersiz XP değeri.'})

            elif action == 'admin_approve_premium':
                # Admin manuel onayı — Google Play IAP dışında kalan özel durumlar için
                # (promosyon, test, iade sonrası yeniden aktivasyon vb.)
                if is_admin:
                    target = data.get('username')
                    tier = int(data.get('tier', 0))
                    days = int(data.get('days', 30))  # varsayılan 30 gün
                    u_res = supabase.table('users').select('stats').eq('username', target).execute()
                    if u_res.data:
                        stats = u_res.data[0].get('stats', {})
                        if isinstance(stats, str):
                            try: stats = json.loads(stats)
                            except: stats = {}
                        stats['premium_tier'] = tier
                        stats.pop('pending_premium', None)
                        if 'premium_color' not in stats or not stats['premium_color']:
                            color_map = {1: 'std-blue', 2: 'dlx-blue', 3: 'ult-gold'}
                            stats['premium_color'] = color_map.get(tier, 'std-blue')
                        if tier > 0:
                            exp_dt = datetime.datetime.now() + datetime.timedelta(days=days)
                            stats['premium_expire_date'] = exp_dt.strftime("%Y-%m-%d")
                            stats['expiry_ts'] = int(exp_dt.timestamp())
                            # Admin onayı olduğunu işaretle (IAP token'ı olmayan manuel aktivasyonlar)
                            stats['gp_admin_override'] = True
                        else:
                            stats.pop('premium_expire_date', None)
                            stats.pop('expiry_ts', None)
                            stats.pop('gp_admin_override', None)
                        supabase.table('users').update({"stats": stats}).eq('username', target).execute()
                        _sync_membership_columns(target, stats)
                        logger.info(f"Admin manuel premium onayı: {target} → tier {tier} ({days} gün)")

            elif action == 'admin_reject_premium':
                # Admin manuel reddi — IAP dışı pending durumlarını temizler
                if is_admin:
                    target = data.get('username')
                    u_res = supabase.table('users').select('stats').eq('username', target).execute()
                    if u_res.data:
                        stats = u_res.data[0].get('stats', {})
                        if isinstance(stats, str):
                            try: stats = json.loads(stats)
                            except: stats = {}
                        stats.pop('pending_premium', None)
                        supabase.table('users').update({"stats": stats}).eq('username', target).execute()
                        logger.info(f"Admin premium reddi: {target}")

            elif action == 'admin_toggle_premium':
                if is_admin:
                    target = data.get('username')
                    tier = int(data.get('tier', 0))
                    days = int(data.get('days', 30))  # varsayılan 30 gün
                    u_res = supabase.table('users').select('stats').eq('username', target).execute()
                    if u_res.data:
                        stats = u_res.data[0].get('stats', {})
                        if isinstance(stats, str):
                            try: stats = json.loads(stats)
                            except: stats = {}
                        stats['premium_tier'] = tier
                        stats.pop('pending_premium', None)
                        if 'premium_color' not in stats or not stats['premium_color']:
                            color_map = {1: 'std-blue', 2: 'dlx-blue', 3: 'ult-gold'}
                            stats['premium_color'] = color_map.get(tier, 'std-blue')
                        if tier > 0:
                            exp_dt = datetime.datetime.now() + datetime.timedelta(days=days)
                            stats['premium_expire_date'] = exp_dt.strftime("%Y-%m-%d")
                            stats['expiry_ts'] = int(exp_dt.timestamp())
                            stats.pop('gp_admin_revoked', None)  # Yeni üyelik verilince engeli kaldır
                        else:
                            stats.pop('premium_expire_date', None)
                            stats.pop('expiry_ts', None)
                            stats['gp_admin_revoked'] = True  # Admin elle sildi — restore engellensin
                        supabase.table('users').update({"stats": stats}).eq('username', target).execute()
                        _sync_membership_columns(target, stats)
                        
            elif action == 'update_premium_color':
                u_res = supabase.table('users').select('stats').eq('username', current_username).execute()
                if u_res.data:
                    stats = u_res.data[0].get('stats', {})
                    if stats.get('premium_tier', 0) > 0: 
                        stats['premium_color'] = data.get('color', 'std-blue')
                        stats['avatar_effect'] = data.get('effect', 'none')
                        supabase.table('users').update({"stats": stats}).eq('username', current_username).execute()

            elif action == 'redeem_code':
                # Aktivasyon kodu kullanma
                code_input = data.get('code', '').strip().upper()
                if not code_input:
                    return jsonify({'status': 'error', 'message': 'Lütfen bir aktivasyon kodu girin.'})

                try:
                    code_res = supabase.table('activation_codes').select('*').eq('id', code_input).execute()
                except Exception as e:
                    logger.error(f'redeem_code tablo hatası: {e}')
                    return jsonify({'status': 'error', 'message': 'Sistem hatası, lütfen tekrar deneyin.'})

                if not code_res.data:
                    return jsonify({'status': 'error', 'message': '❌ Geçersiz aktivasyon kodu!'})

                code_data = code_res.data[0]
                if code_data.get('is_used'):
                    return jsonify({'status': 'error', 'message': '❌ Bu kod daha önce kullanılmış!'})

                tier = int(code_data.get('tier', 1))
                days = int(code_data.get('days', 30))

                # Kullanıcının mevcut stats'ını al
                u_res = supabase.table('users').select('stats').eq('username', current_username).execute()
                if not u_res.data:
                    return jsonify({'status': 'error', 'message': 'Kullanıcı bulunamadı.'})

                stats = u_res.data[0].get('stats', {}) or {}
                if isinstance(stats, str):
                    try: stats = json.loads(stats)
                    except: stats = {}

                # Mevcut üyelik varsa günleri ekle, yoksa yeni başlat
                now_dt = datetime.datetime.now()
                existing_expire = stats.get('premium_expire_date', '')
                if existing_expire and int(stats.get('premium_tier', 0)) >= tier:
                    # Mevcut üyelik süresi daha yüksek veya eşit tier — süre uzat
                    try:
                        base_dt = datetime.datetime.strptime(existing_expire, "%Y-%m-%d")
                        if base_dt < now_dt:
                            base_dt = now_dt
                    except:
                        base_dt = now_dt
                    exp_dt = base_dt + datetime.timedelta(days=days)
                else:
                    exp_dt = now_dt + datetime.timedelta(days=days)

                color_map = {1: 'std-blue', 2: 'dlx-purple', 3: 'ult-gold'}
                stats['premium_tier'] = tier
                stats['premium_expire_date'] = exp_dt.strftime("%Y-%m-%d")
                stats['expiry_ts'] = int(exp_dt.timestamp())
                stats['gp_admin_override'] = True
                stats.pop('gp_admin_revoked', None)
                if 'premium_color' not in stats or not stats['premium_color']:
                    stats['premium_color'] = color_map.get(tier, 'std-blue')

                supabase.table('users').update({'stats': stats}).eq('username', current_username).execute()
                _sync_membership_columns(current_username, stats)

                # Kodu kullanıldı olarak işaretle
                supabase.table('activation_codes').update({
                    'is_used': True,
                    'used_by': current_username,
                    'used_at': int(time.time())
                }).eq('id', code_input).execute()

                tier_names = {1: '⭐ Standart', 2: '🌟 Deluxe', 3: '👑 Ultra+'}
                tier_name = tier_names.get(tier, 'Standart')
                logger.info(f'Aktivasyon kodu kullanıldı: {code_input} → {current_username} ({tier_name}, {days} gün)')

                return jsonify({
                    'status': 'ok',
                    'message': f'🎉 {tier_name} üyeliğin aktive edildi! ({days} gün) Tadını çıkar!',
                    'tier': tier,
                    'expire_date': exp_dt.strftime("%Y-%m-%d"),
                    'stats': stats
                })

            elif action == 'get_markers_by_bounds':
                bounds = data.get('bounds', {})
                ne_lat = bounds.get('ne_lat')
                sw_lat = bounds.get('sw_lat')
                ne_lng = bounds.get('ne_lng')
                sw_lng = bounds.get('sw_lng')
                if ne_lat is None or sw_lat is None or ne_lng is None or sw_lng is None:
                    return jsonify({'status': 'error', 'message': 'Bounds eksik'})
                try:
                    m_res = supabase.table('markers').select('*').gte('lat', sw_lat).lte('lat', ne_lat).gte('lng', sw_lng).lte('lng', ne_lng).limit(1000).execute()
                    return jsonify({'status': 'ok', 'markers': m_res.data or []})
                except Exception as e:
                    logger.error(f"get_markers_by_bounds error: {e}")
                    return jsonify({'status': 'error', 'message': 'Harita verisi alınamadı.'})

            elif action == 'add_marker':
                # addedBy her zaman sunucu tarafından atanır — istemci manipülasyonu engellenir
                data['addedBy'] = current_username
                data['id'] = str(data['id'])
                if 'name' in data: data['name'] = html.escape(str(data['name']))
                if 'desc' in data: data['desc'] = html.escape(str(data['desc']))
                if 'category' in data: data['category'] = html.escape(str(data['category']))
                if 'extra_note' in data: data['extra_note'] = html.escape(str(data['extra_note']))
                if 'difficulty' in data: data['difficulty'] = html.escape(str(data['difficulty']))
                if 'likes' not in data: data['likes'] = []
                if 'dislikes' not in data: data['dislikes'] = []
                if 'fake_reports' not in data: data['fake_reports'] = []
                
                marker_check = supabase.table('markers').select('id, addedBy').eq('id', data['id']).execute()
                is_new_marker = not marker_check.data

                if not is_new_marker and not is_admin:
                    if marker_check.data[0].get('addedBy') != current_username:
                        return jsonify({'status': 'error', 'message': 'Yetkisiz işlem: Sadece kendi rampanızı güncelleyebilirsiniz.'})

                try:
                    supabase.table('markers').upsert(data).execute()
                except Exception as e:
                    error_msg = str(e)
                    if 'icon_type' in error_msg or 'PGRST' in error_msg or 'dislikes' in error_msg:
                        if 'dislikes' in data: data.pop('dislikes', None)
                        if 'icon_type' in data: data.pop('icon_type', None)
                        supabase.table('markers').upsert(data).execute()
                    else:
                        raise e
                
                if is_new_marker:
                    u_res = supabase.table('users').select('stats').eq('username', current_username).execute()
                    if u_res.data:
                        stats = u_res.data[0].get('stats', {})
                        if isinstance(stats, str):
                            try: stats = json.loads(stats)
                            except: stats = {}
                        stats['markers'] = stats.get('markers', 0) + 1
                        supabase.table('users').update({"stats": stats}).eq('username', current_username).execute()
                    # Yeni rampa bildirimi - herkese
                    try:
                        marker_name = data.get('name', 'Yeni Nokta')
                        broadcast_push(
                            title=f"📍 Yeni Rampa Eklendi!",
                            body=f"{current_username} haritaya '{marker_name}' ekledi",
                            exclude_user=current_username,
                            url="/"
                        )
                    except Exception as _exc:
                        logger.warning(f'Hata: {_exc}')
                
            elif action == 'delete_marker':
                m_res = supabase.table('markers').select('addedBy').eq('id', str(data.get('id'))).execute()
                if m_res.data:
                    if is_admin or m_res.data[0].get('addedBy') == current_username:
                        supabase.table('markers').delete().eq('id', str(data.get('id'))).execute()
                    
            elif action == 'like_marker':
                m_res = supabase.table('markers').select('likes, dislikes, addedBy, name').eq('id', str(data.get('id'))).execute()
                if m_res.data:
                    likes      = m_res.data[0].get('likes', [])
                    dislikes   = m_res.data[0].get('dislikes', [])
                    m_owner    = m_res.data[0].get('addedBy', '')
                    m_name     = (m_res.data[0].get('name') or 'Rampa')[:40]
                    was_liked  = current_username in likes
                    if was_liked:
                        likes.remove(current_username)
                    else: 
                        likes.append(current_username)
                        if current_username in dislikes: dislikes.remove(current_username)
                    
                    update_payload = {"likes": likes}
                    if 'dislikes' in m_res.data[0]: update_payload["dislikes"] = dislikes
                    supabase.table('markers').update(update_payload).eq('id', str(data.get('id'))).execute()
                    # ── Rampa sahibine beğeni bildirimi (milestone: 5, 10, 25, 50) ──
                    if not was_liked and m_owner and m_owner != current_username:
                        try:
                            new_like_count = len(likes)
                            if new_like_count in [5, 10, 25, 50, 100]:
                                send_push_to_user(
                                    m_owner,
                                    title=f"👍 '{m_name}' {new_like_count} beğeni aldı!",
                                    body=f"{current_username} ve diğerleri rampanı seviyor 🏔️",
                                    url="/"
                                )
                            elif new_like_count == 1:
                                send_push_to_user(
                                    m_owner,
                                    title=f"👍 {current_username} rampanı beğendi!",
                                    body=f"'{m_name}' haritasındaki noktana ilk beğeni geldi!",
                                    url="/"
                                )
                        except Exception as _exc:
                            logger.warning(f'Hata: {_exc}')

            elif action == 'dislike_marker':
                m_res = supabase.table('markers').select('likes, dislikes').eq('id', str(data.get('id'))).execute()
                if m_res.data:
                    likes = m_res.data[0].get('likes', [])
                    dislikes = m_res.data[0].get('dislikes', [])
                    if current_username in dislikes: 
                        dislikes.remove(current_username)
                    else: 
                        dislikes.append(current_username)
                        if current_username in likes: likes.remove(current_username)
                    
                    update_payload = {"dislikes": dislikes, "likes": likes}
                    try:
                        supabase.table('markers').update(update_payload).eq('id', str(data.get('id'))).execute()
                    except Exception as e:
                        print(f"⚠️ Marker beğeni güncelleme hatası: {e}")

            elif action == 'add_message':
                # Sohbet kurallari - session cache
                if not session.get('accepted_chat_rules'):
                    try:
                        chat_user_res = supabase.table('users').select('accepted_chat_rules').eq('username', current_username).execute()
                        if chat_user_res.data:
                            if not chat_user_res.data[0].get('accepted_chat_rules'):
                                return jsonify({'status': 'error', 'message': 'Sohbet kurallarını kabul etmeden mesaj gönderemezsiniz.'})
                            else:
                                session['accepted_chat_rules'] = True
                    except Exception as _exc:
                        logger.warning(f'Sohbet kuralı kontrol hatası: {_exc}')

                ai_moderation_result = None
                ai_moderation_msg = None

                if data.get('type') == 'text':
                    raw_text = data.get('text', '').strip()
                    if not raw_text:
                        return jsonify({'status': 'error', 'message': 'Boş mesaj gönderilemez.'})
                    if len(raw_text) > 1000:
                        return jsonify({'status': 'error', 'message': 'Mesaj çok uzun (max 1000 karakter).'})

                    # ── Telegram Admin Çağrısı ──
                    if raw_text.strip().lower().startswith('/admin'):
                        try:
                            from telegram_notify import tg
                            tg.send(f"🚨 <b>ADMİN ÇAĞRISI (SOHBET)</b>\n👤 Kullanıcı: <code>{current_username}</code>\n💬 Mesaj: {raw_text}")
                        except Exception as e:
                            logger.warning(f"Telegram admin uyarı hatası: {e}")

                    # ── Proaktif AI Moderasyon — mesaj kaydedilmeden ÖNCE kontrol ──
                    try:
                        ai_moderation_result = analyze_content(raw_text)
                    except Exception as _mod_exc:
                        logger.warning(f'AI moderasyon analiz hatası: {_mod_exc}')
                        ai_moderation_result = None

                data['text'] = html.escape(raw_text)

                # Fix IDOR & Mass Assignment
                # Create a clean message object instead of passing raw 'data'
                msg_id = str(int(time.time() * 1000))
                clean_data = {
                    'id': msg_id,
                    'user': current_username,
                    'type': data.get('type', 'text'),
                    'text': data.get('text', ''),
                    'timestamp': int(time.time()),
                    'is_flagged': False,
                    'flag_count': 0
                }
                
                # Resim veya ses varsa güvenli şekilde ekle
                if data.get('photo'): clean_data['photo'] = data.get('photo')
                if data.get('voice'): clean_data['voice'] = data.get('voice')

                # ── AI tespit ederse flag bilgisini mesaja ekle ──
                is_warning_only = False
                warning_text = None
                is_flagged_by_ai = False
                
                if ai_moderation_result:
                    severity = ai_moderation_result.get('severity', 'none')
                    if severity == 'low':
                        # Salak, mal vb. hafif argo durumu -> Rapor yok, blur yok, sadece uyari
                        is_warning_only = True
                        warning_text = "Lütfen argo veya kırıcı sözler kullanmayın."
                    elif ai_moderation_result.get('is_inappropriate'):
                        is_flagged_by_ai = True
                        clean_data['is_flagged'] = True
                        clean_data['flag_count'] = 1

                supabase.table('messages').insert(clean_data).execute()
                data['id'] = msg_id # For the report block below

                # ── Otomatik Flaglanan Mesajları Yönetici Raporlarına Ekle ──
                if is_flagged_by_ai:
                    try:
                        _save_report(
                            supabase_client=supabase,
                            log=logger,
                            message_id=data['id'],
                            content=data['text'],
                            sender=current_username,
                            reporter_ip="Otomatik AI Mod",
                            analysis=ai_moderation_result
                        )
                    except Exception as _e:
                        logger.warning(f"Otomatik rapor kaydetme hatası: {_e}")

                # ── AI uygunsuz içerik tespit ettiyse sistem uyarısı ekle ──
                if is_flagged_by_ai:
                    try:
                        _sev_label = ai_moderation_result.get('severity', 'medium')
                        ai_warning_text = f"{current_username} ihlal yaptınız. Tekrar edilirse hesabınız askıya alınır."
                        ai_msg_id = str(int(time.time() * 1000)) + '_mod'
                        supabase.table('messages').insert({
                            'id': ai_msg_id,
                            'user': 'Moderatör AI',
                            'text': ai_warning_text,
                            'type': 'text',
                        }).execute()
                        def delete_ai_msg(msg_id):
                            time.sleep(60)
                            try: supabase.table('messages').delete().eq('id', msg_id).execute()
                            except: pass
                        threading.Thread(target=delete_ai_msg, args=(ai_msg_id,), daemon=True).start()

                        ai_moderation_msg = {
                            'id': ai_msg_id,
                            'user': 'Moderatör AI',
                            'text': ai_warning_text,
                            'type': 'text',
                        }
                        # Kullanıcı uyarı sayacını artır
                        try:
                            u_warn = supabase.table('users').select('stats').eq('username', current_username).limit(1).execute()
                            if u_warn.data:
                                _st = u_warn.data[0].get('stats') or {}
                                if isinstance(_st, str):
                                    try: _st = json.loads(_st)
                                    except: _st = {}
                                _st['mod_warning_count'] = _st.get('mod_warning_count', 0) + 1
                                _st['last_mod_warning_ts'] = int(time.time())
                                supabase.table('users').update({'stats': _st}).eq('username', current_username).execute()
                        except Exception as _warn_exc:
                            logger.warning(f'Uyarı sayacı güncelleme hatası: {_warn_exc}')

                        # ── AI ihlal tespitini admin'e DM olarak bildir ──
                        try:
                            _admin_uname = 'Admin'
                            try:
                                _adm_res = supabase.table('users').select('username').or_(
                                    "role.eq.Admin,username.eq.Admin"
                                ).limit(1).execute()
                                if _adm_res.data:
                                    _admin_uname = _adm_res.data[0]['username']
                            except Exception:
                                pass
                            _sev_emoji = {'high': '🔴', 'medium': '🟠', 'low': '🟡'}.get(_sev_label, '⚪')
                            _raw_text = data.get('text', '')[:200]
                            _matched = ', '.join(ai_moderation_result.get('matched_patterns', [])[:3]) or 'Genel ihlal'
                            _admin_dm_text = (
                                f"[🤖 AI MODERASYON BİLDİRİMİ]\n"
                                f"Kullanıcı: {current_username}\n"
                                f"Seviye: {_sev_emoji} {_sev_label.upper()}\n"
                                f"Sebep: {_matched}\n"
                                f"Mesaj: {_raw_text}"
                            )
                            _admin_dm_id = str(int(time.time() * 1000)) + '_aimod'
                            supabase.table('dms').insert({
                                'id': _admin_dm_id,
                                'sender': current_username,
                                'receiver': _admin_uname,
                                'participants': [current_username, _admin_uname],
                                'text': _admin_dm_text,
                                'type': 'text',
                            }).execute()
                            logger.info(f"AI moderasyon DM gönderildi → {_admin_uname} (kullanıcı: {current_username})")
                        except Exception as _dm_exc:
                            logger.warning(f'AI moderasyon admin DM hatası: {_dm_exc}')
                    except Exception as _ai_exc:
                        logger.warning(f'AI moderatör mesaj ekleme hatası: {_ai_exc}')

                u_res = supabase.table('users').select('stats').eq('username', current_username).execute()
                if u_res.data:
                    stats = u_res.data[0].get('stats', {}) or {}
                    if isinstance(stats, str):
                        try: stats = json.loads(stats)
                        except: stats = {}
                    stats['total_messages'] = stats.get('total_messages', 0) + 1
                    stats['last_seen_ts'] = int(time.time())
                    supabase.table('users').update({"stats": stats}).eq('username', current_username).execute()

                # ── Grup chat bildirimi (flood korumalı: 3 dk'da bir max 1 bildirim) ──
                try:
                    if data.get('type') == 'text' and _can_broadcast_chat():
                        msg_preview = data.get('text', '')[:60]
                        broadcast_push(
                            title=f"💬 {current_username} yazdı",
                            body=msg_preview,
                            exclude_user=current_username,
                            url="/"
                        )
                except Exception as _exc:
                    logger.warning(f'Hata: {_exc}')

                # ── Proaktif moderasyon sonucunu döndür ──
                if is_flagged_by_ai:
                    return jsonify({
                        'status': 'ok',
                        'ai_flagged': True,
                        'severity': ai_moderation_result.get('severity', 'medium'),
                        'ai_moderation_msg': ai_moderation_msg,
                    })

            elif action == 'ai_bike_analysis':
                bike_info = html.escape(data.get('bike_info', '').strip())
                if not bike_info: return jsonify({'status': 'error', 'message': 'Bilgi eksik'})
                res = ai_bike_analysis(bike_info)
                if 'error' in res: return jsonify({'status': 'error', 'message': res['error']})
                return jsonify({'status': 'ok', 'data': res})

            elif action == 'ai_bike_recommendation':
                budget = html.escape(data.get('budget', '').strip())
                style = html.escape(data.get('style', '').strip())
                terrain = html.escape(data.get('terrain', '').strip())
                level = html.escape(data.get('level', '').strip())
                if not (budget and style): return jsonify({'status': 'error', 'message': 'Eksik bilgi'})
                res = ai_bike_recommend(budget, style, terrain, level)
                if 'error' in res: return jsonify({'status': 'error', 'message': res['error']})
                return jsonify({'status': 'ok', 'data': res})

            elif action == 'ai_bike_build':
                history = data.get('history', {})
                new_req = html.escape(data.get('new_request', '').strip())
                current_step = html.escape(data.get('current_step', '').strip())
                next_step = html.escape(data.get('next_step', '').strip())
                if not new_req: return jsonify({'status': 'error', 'message': 'Eksik bilgi'})
                res = ai_bike_build(history, new_req, current_step, next_step)
                if 'error' in res: return jsonify({'status': 'error', 'message': res['error']})
                return jsonify({'status': 'ok', 'data': res})

            elif action == 'ai_bike_build_final':
                build_data = data.get('build_data', {})
                res = ai_bike_build_final(build_data)
                if 'error' in res: return jsonify({'status': 'error', 'message': res['error']})
                return jsonify({'status': 'ok', 'data': res})

            elif action == 'ai_part_analysis':
                part = html.escape(data.get('part_name', '').strip())
                if not part: return jsonify({'status': 'error', 'message': 'Eksik bilgi'})
                res = ai_part_analysis(part)
                if 'error' in res: return jsonify({'status': 'error', 'message': res['error']})
                return jsonify({'status': 'ok', 'data': res})

            elif action == 'ask_ai':
                text = html.escape(data.get('text', '').strip())
                if not text:
                    return jsonify({'status': 'error', 'message': 'Boş soru sorulamaz.'})
                    
                u_res = supabase.table('users').select('stats').eq('username', current_username).execute()
                if not u_res.data:
                    return jsonify({'status': 'error'})
                user_data = u_res.data[0]
                
                can_use, error_msg = check_ai_limit(current_username, user_data)
                if not can_use:
                    return jsonify({'status': 'error', 'message': error_msg})

                user_msg_id = uuid.uuid4().hex
                supabase.table('messages').insert({
                    'id': user_msg_id, 
                    'user': current_username, 
                    'text': text, 
                    'type': 'text'
                }).execute()

                ai_reply = _call_groq_ai(_GROQ_SYSTEM_CHAT, text)

                ai_msg_id = uuid.uuid4().hex
                supabase.table('messages').insert({
                    'id': ai_msg_id,
                    'user': 'Freerider AI',
                    'text': f"@{current_username} {ai_reply}",
                    'type': 'text'
                }).execute()
                    
            elif action == 'pin_message':
                if not is_admin:
                    return jsonify({'status': 'error', 'message': 'Yetkisiz işlem!'})
                val = json.dumps(data)
                supabase.table('settings').upsert({"id": "pinned_message", "value": val}).execute()
                app_cache.invalidate('pinned_message')
                
            elif action == 'delete_message':
                msg_id = str(data.get('id'))
                msg_res = supabase.table('messages').select('user').eq('id', msg_id).execute()
                if msg_res.data:
                    if is_admin or msg_res.data[0].get('user') == current_username: 
                        supabase.table('messages').delete().eq('id', msg_id).execute()
                        
            elif action == 'send_dm':
                receiver = data.get('receiver', '').strip()
                if not receiver: 
                    return jsonify({'status': 'error', 'message': 'Alıcı seçilmedi.'})
                if data.get('type') == 'text':
                    raw_dm = data.get('text', '').strip()
                    if not raw_dm:
                        return jsonify({'status': 'error', 'message': 'Boş mesaj gönderilemez.'})
                    if len(raw_dm) > 2000:
                        return jsonify({'status': 'error', 'message': 'Mesaj çok uzun (max 2000 karakter).'})
                    data['text'] = html.escape(raw_dm)
                    
                dm_id = str(int(time.time() * 1000))
                clean_data = {
                    'id': dm_id,
                    'sender': current_username,
                    'receiver': receiver,
                    'participants': [current_username, receiver],
                    'type': data.get('type', 'text'),
                    'text': data.get('text', ''),
                    'timestamp': int(time.time()),
                    'read': False
                }
                
                if data.get('photo'): clean_data['photo'] = data.get('photo')
                if data.get('voice'): clean_data['voice'] = data.get('voice')
                
                supabase.table('dms').insert(clean_data).execute()
                data['id'] = dm_id

                # DM push bildirimi - sadece alıcıya, 60 sn cooldown ile (spam önleme)
                if receiver != 'Freerider AI' and data.get('type') in ('text', 'photo', 'voice'):
                    _dm_notif_key = f'dm_notif_{current_username}_{receiver}'
                    if not app_cache.get(_dm_notif_key):
                        notif_body = data.get('text', '')[:80] if data.get('type') == 'text' else ('📸 Fotoğraf gönderdi' if data.get('type') == 'photo' else '🎤 Sesli mesaj gönderdi')
                        try:
                            send_push_to_user(
                                receiver,
                                title=f"💬 {current_username} sana mesaj attı",
                                body=notif_body,
                                url="/"
                            )
                            app_cache.set(_dm_notif_key, True, ttl=60)  # 60 sn cooldown
                        except Exception as _exc:
                            logger.warning(f'Hata: {_exc}')

                if receiver == 'Freerider AI' and data.get('type') == 'text':
                    u_res = supabase.table('users').select('stats').eq('username', current_username).execute()
                    if u_res.data:
                        user_data = u_res.data[0]
                        can_use, error_msg = check_ai_limit(current_username, user_data)
                        
                        if not can_use:
                            ai_reply = error_msg
                        else:
                            ai_reply = _call_groq_ai(_GROQ_SYSTEM_DM, data.get('text', ''))

                        ai_dm_id = uuid.uuid4().hex
                        supabase.table('dms').insert({
                            'id': ai_dm_id,
                            'sender': 'Freerider AI',
                            'receiver': current_username,
                            'participants': [current_username, 'Freerider AI'],
                            'text': ai_reply,
                            'type': 'text'
                        }).execute()

            elif action == 'add_market':
                data['title'] = html.escape(data.get('title', ''))
                data['desc'] = html.escape(data.get('desc', ''))
                data['contact'] = html.escape(data.get('contact', ''))
                data['owner'] = current_username
                data['date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                data['id'] = str(data['id'])
                data['views'] = 0
                data['bumped_at'] = int(time.time() * 1000)
                
                market_check = supabase.table('market').select('id, owner').eq('id', data['id']).execute()
                is_new = not market_check.data
                
                if not is_new and not is_admin:
                    if market_check.data[0].get('owner') != current_username:
                        return jsonify({'status': 'error', 'message': 'Yetkisiz işlem: Sadece kendi ilanınızı güncelleyebilirsiniz.'})
                
                try:
                    supabase.table('market').upsert(data).execute()
                    # Yeni ilan bildirimi - herkese
                    try:
                        item_title = data.get('title', 'Yeni Ilan')
                        item_price = data.get('price', '')
                        price_str = f" - {item_price} TL" if item_price else ""
                        broadcast_push(
                            title=f"🛒 Yeni İlan: {item_title}",
                            body=f"{current_username} yeni bir ilan yayınladı{price_str}",
                            exclude_user=current_username,
                            url="/"
                        )
                    except Exception as _exc:
                        logger.warning(f'Hata: {_exc}')
                except Exception as e:
                    error_msg = str(e)
                    if 'views' in error_msg or 'bumped_at' in error_msg or 'PGRST' in error_msg:
                        data.pop('views', None)
                        data.pop('bumped_at', None)
                        supabase.table('market').upsert(data).execute()
                    else:
                        raise e
                
                if is_new:
                    u_res_full = supabase.table('users').select('stats').eq('username', current_username).execute()
                    if u_res_full.data:
                        stats = u_res_full.data[0].get('stats', {})
                        if isinstance(stats, str):
                            try: stats = json.loads(stats)
                            except: stats = {}
                        stats['market'] = stats.get('market', 0) + 1
                        supabase.table('users').update({"stats": stats}).eq('username', current_username).execute()
                
            elif action == 'bump_market':
                try:
                    m_check = supabase.table('market').select('owner').eq('id', str(data.get('id'))).execute()
                    if not m_check.data:
                        return jsonify({'status': 'error', 'message': 'İlan bulunamadı.'})
                    if m_check.data[0].get('owner') != current_username and not is_admin:
                        return jsonify({'status': 'error', 'message': 'Bu ilanı yalnızca sahibi öne çıkarabilir.'})
                    supabase.table('market').update({"bumped_at": int(time.time() * 1000)}).eq('id', str(data.get('id'))).execute()
                except Exception as e:
                    print(f"⚠️ Bump market hatası: {e}")
                
            elif action == 'increment_market_view':
                try:
                    m_res = supabase.table('market').select('views, owner, title').eq('id', str(data.get('id'))).execute()
                    if m_res.data:
                        current_views = m_res.data[0].get('views', 0)
                        new_mv = current_views + 1
                        supabase.table('market').update({"views": new_mv}).eq('id', str(data.get('id'))).execute()
                        # ── 10, 50, 100 görüntüleme milestone bildirimi ──
                        market_owner = m_res.data[0].get('owner', '')
                        market_title = (m_res.data[0].get('title') or 'İlanın')[:40]
                        if market_owner and market_owner != current_username and new_mv in [5, 10, 25, 50, 100]:
                            try:
                                send_push_to_user(
                                    market_owner,
                                    title=f"🛒 İlanın {new_mv} kez görüntülendi!",
                                    body=f"'{market_title}' ilanın ilgi görüyor. Fiyatı gözden geçir! 💰",
                                    url="/"
                                )
                            except Exception as _exc:
                                logger.warning(f'Hata: {_exc}')
                except Exception as e:
                    print(f"⚠️ Market görüntülenme sayacı hatası: {e}")
                
            elif action == 'delete_market':
                ad_res = supabase.table('market').select('owner').eq('id', str(data.get('id'))).execute()
                if ad_res.data:
                    if ad_res.data[0].get('owner') == current_username or is_admin: 
                        supabase.table('market').delete().eq('id', str(data.get('id'))).execute()

            elif action == 'add_event':
                data['title'] = html.escape(data.get('title', ''))
                data['desc'] = html.escape(data.get('desc', ''))
                data['creator'] = current_username
                data['attendees'] = [current_username]
                data['xp_awarded'] = False
                data['id'] = str(data['id'])
                
                event_check = supabase.table('events').select('id, creator, attendees').eq('id', data['id']).execute()
                is_new = not event_check.data
                
                if not is_new and not is_admin:
                    if event_check.data[0].get('creator') != current_username:
                        return jsonify({'status': 'error', 'message': 'Yetkisiz işlem: Sadece kendi etkinliğinizi güncelleyebilirsiniz.'})
                    else:
                        data['attendees'] = event_check.data[0].get('attendees', [current_username])
                elif not is_new and is_admin:
                    data['attendees'] = event_check.data[0].get('attendees', [current_username])

                supabase.table('events').upsert(data).execute()
                
                if is_new:
                    u_res = supabase.table('users').select('stats').eq('username', current_username).execute()
                    if u_res.data:
                        stats = u_res.data[0].get('stats', {})
                        if isinstance(stats, str):
                            try: stats = json.loads(stats)
                            except: stats = {}
                        stats['events'] = stats.get('events', 0) + 1
                        supabase.table('users').update({"stats": stats}).eq('username', current_username).execute()
                
                # Yeni buluşma bildirimi - herkese
                try:
                    ev_title = data.get('title', 'Yeni Bulusma')
                    ev_date = data.get('datetime', '')[:10]
                    broadcast_push(
                        title=f"📅 Yeni Buluşma: {ev_title}",
                        body=f"{current_username} bir buluşma oluşturdu! Tarih: {ev_date}",
                        exclude_user=current_username,
                        url="/"
                    )
                except Exception as _exc:
                    logger.warning(f'Hata: {_exc}')
                
            elif action == 'join_event':
                ev_id = str(data.get('id'))
                event_res = supabase.table('events').select('*').eq('id', ev_id).execute()
                if event_res.data:
                    ev_data = event_res.data[0]
                    att = ev_data.get('attendees', [])
                    max_limit = ev_data.get('max')
                    
                    if current_username not in att: 
                        limit = 0
                        try:
                            if max_limit: limit = int(max_limit)
                        except (ValueError, TypeError):
                            limit = 0
                            
                        if limit > 0 and len(att) >= limit:
                            return jsonify({'status': 'error', 'message': 'Kapasite dolu, maalesef katılamazsınız!'})
                            
                        att.append(current_username)
                        supabase.table('events').update({"attendees": att}).eq('id', ev_id).execute()
                        # ── Etkinlik sahibine bildirim (5 dk cooldown — çok katılım olunca spam önleme) ──
                        try:
                            ev_creator = ev_data.get('creator', '')
                            ev_title_j = ev_data.get('title', 'Etkinlik')[:40]
                            _ev_notif_key = f'ev_join_notif_{ev_id}'
                            if ev_creator and ev_creator != current_username and not app_cache.get(_ev_notif_key):
                                send_push_to_user(
                                    ev_creator,
                                    title=f"🎉 {current_username} etkinliğine katıldı!",
                                    body=f"'{ev_title_j}' etkinliğinde yeni katılımcı var!",
                                    url="/"
                                )
                                app_cache.set(_ev_notif_key, True, ttl=300)  # 5 dk cooldown
                        except Exception as _exc:
                            logger.warning(f'Hata: {_exc}')

            elif action == 'leave_event':
                ev_id = str(data.get('id'))
                event_res = supabase.table('events').select('attendees').eq('id', ev_id).execute()
                if event_res.data:
                    att = event_res.data[0].get('attendees', [])
                    if current_username in att: 
                        att.remove(current_username)
                        supabase.table('events').update({"attendees": att}).eq('id', ev_id).execute()
                        
            elif action == 'delete_event':
                event_res = supabase.table('events').select('creator').eq('id', str(data.get('id'))).execute()
                if event_res.data:
                    if event_res.data[0].get('creator') == current_username or is_admin: 
                        supabase.table('events').delete().eq('id', str(data.get('id'))).execute()


            elif action == 'join_giveaway':
                gw_id = data.get('gw_id') or data.get('giveaway_id')
                ig_username = html.escape(data.get('instagram', ''))
                if not gw_id: return jsonify({'status': 'error', 'message': 'Çekiliş ID eksik'})
                if not ig_username: return jsonify({'status': 'error', 'message': 'Instagram adı zorunludur!'})

                # Yeni giveaways tablosu kontrolü
                try:
                    gw_res = supabase.table('giveaways').select('status, end_date, participants').eq('id', gw_id).execute()
                    if gw_res.data:
                        import datetime as _dt
                        gw = gw_res.data[0]
                        if gw.get('status') != 'active':
                            return jsonify({'status': 'error', 'message': 'Bu çekiliş aktif değil.'})
                        today_iso = _dt.date.today().isoformat()
                        if gw.get('end_date') and gw['end_date'] < today_iso:
                            return jsonify({'status': 'error', 'message': 'Bu çekilişin süresi dolmuş.'})
                        participants = gw.get('participants') or []
                        already_joined = any((p.get('username') == current_username if isinstance(p, dict) else p == current_username) for p in participants)
                        if already_joined:
                            return jsonify({'status': 'error', 'message': 'Zaten katıldınız.'})
                        participants.append({'username': current_username, 'instagram': ig_username})
                        supabase.table('giveaways').update({'participants': participants}).eq('id', gw_id).execute()
                        return jsonify({'status': 'ok', 'message': 'Çekilişe başarıyla katıldınız!'})
                except Exception:
                    pass

                # Eski settings tabanlı çekiliş
                res = supabase.table('settings').select('value').eq('id', 'giveaway_data').execute()
                if res.data and res.data[0].get('value'):
                    giveaways = json.loads(res.data[0]['value']) if isinstance(res.data[0]['value'], str) else res.data[0]['value']
                    if not isinstance(giveaways, list):
                        giveaways = [giveaways] if giveaways else []
                    
                    found = False
                    for gw_data in giveaways:
                        if gw_data.get('id') == gw_id and gw_data.get('is_active'):
                            found = True
                            parts = gw_data.get('participants', [])
                            ig_map = gw_data.get('participants_ig', {})
                            
                            if current_username not in parts:
                                parts.append(current_username)
                                ig_map[current_username] = ig_username
                                gw_data['participants'] = parts
                                gw_data['participants_ig'] = ig_map
                                supabase.table('settings').upsert({"id": "giveaway_data", "value": json.dumps(giveaways)}).execute()
                                return jsonify({'status': 'ok', 'message': 'Katıldınız!'})
                            return jsonify({'status': 'error', 'message': 'Zaten katıldınız.'})
                    if not found:
                        return jsonify({'status': 'error', 'message': 'Aktif çekiliş bulunamadı.'})
                return jsonify({'status': 'error', 'message': 'Çekiliş sistemi boş.'})

            elif action == 'create_giveaway':
                import datetime as _dt
                if not is_admin:
                    return jsonify({'status': 'error', 'message': 'Yetkisiz işlem.'})
                title = html.escape(data.get('title', '').strip())
                prize = html.escape(data.get('prize', '').strip())
                description = html.escape(data.get('description', '').strip())
                end_date = data.get('end_date', '').strip()
                image_b64 = data.get('image_base64', '')
                winner_count = max(1, int(data.get('winner_count', 1)))
                admin_pick_mode = bool(data.get('admin_pick_mode', False))
                admin_picked_usernames = [u.strip() for u in data.get('admin_picked_usernames', []) if u.strip()]
                if not title or not prize or not end_date:
                    return jsonify({'status': 'error', 'message': 'Başlık, ödül ve tarih zorunludur.'})
                try:
                    _dt.date.fromisoformat(end_date)
                except ValueError:
                    return jsonify({'status': 'error', 'message': 'Geçersiz tarih formatı.'})
                image_url = ''
                if image_b64.startswith('data:image'):
                    try:
                        uploaded = upload_base64_to_storage(image_b64, folder='giveaways')
                        # R2 başarılıysa http URL döner, None veya base64 dönerse fallback
                        if uploaded and uploaded.startswith('http'):
                            image_url = uploaded
                        else:
                            image_url = "https://cdn.freeridertr.com.tr/bildirim%20resmi/photo_5825636358775573905_y%20(1).jpg"
                    except Exception as e:
                        logger.error(f'Giveaway resim yükleme hatası: {e}')
                        image_url = "https://cdn.freeridertr.com.tr/bildirim%20resmi/photo_5825636358775573905_y%20(1).jpg"
                try:
                    supabase.table('giveaways').insert({
                        'title': title, 'prize': prize, 'description': description,
                        'image_url': image_url, 'end_date': end_date, 'status': 'active',
                        'participants': [], 'winner_count': winner_count, 'winners': [],
                        'admin_pick_mode': admin_pick_mode,
                        'admin_picked_usernames': admin_picked_usernames if admin_picked_usernames else None,
                        'created_by': current_username, 'created_at': _dt.datetime.utcnow().isoformat()
                    }).execute()
                    return jsonify({'status': 'ok', 'message': 'Çekiliş oluşturuldu.'})
                except Exception as e:
                    logger.error(f'Çekiliş oluşturma hatası: {e}')
                    return jsonify({'status': 'error', 'message': 'Çekiliş kaydedilemedi.'})

            elif action == 'finalize_giveaway':
                if not is_admin:
                    return jsonify({'status': 'error', 'message': 'Yetkisiz işlem.'})
                import datetime as _dt
                gw_id = data.get('giveaway_id')
                manual_winners = [u.strip() for u in data.get('manual_winners', []) if u.strip()]
                try:
                    res = supabase.table('giveaways').select('status, participants, winner_count, admin_pick_mode, admin_picked_usernames').eq('id', gw_id).execute()
                    if not res.data:
                        return jsonify({'status': 'error', 'message': 'Çekiliş bulunamadı.'})
                    gw = res.data[0]
                    if gw.get('status') != 'active':
                        return jsonify({'status': 'error', 'message': 'Çekiliş zaten sonuçlanmış.'})
                    participants = gw.get('participants') or []
                    if not participants:
                        return jsonify({'status': 'error', 'message': 'Katılımcı yok!'})
                    winner_count = gw.get('winner_count') or 1
                    admin_pick_mode = gw.get('admin_pick_mode') or False
                    admin_picked_usernames = gw.get('admin_picked_usernames') or []
                    winners = []
                    sources = manual_winners or (admin_picked_usernames if admin_pick_mode else [])
                    if sources:
                        for uname in sources:
                            for p in participants:
                                if (isinstance(p, dict) and p.get('username') == uname) or p == uname:
                                    winners.append({'username': p.get('username', uname) if isinstance(p, dict) else uname, 'instagram': p.get('instagram', '') if isinstance(p, dict) else ''})
                                    break
                    if not winners:
                        selected = random.sample(participants, min(winner_count, len(participants)))
                        for p in selected:
                            winners.append({'username': p.get('username', '') if isinstance(p, dict) else str(p), 'instagram': p.get('instagram', '') if isinstance(p, dict) else ''})
                    if not winners:
                        return jsonify({'status': 'error', 'message': 'Geçerli kazanan bulunamadı.'})
                    supabase.table('giveaways').update({'status': 'completed', 'winners': winners, 'finalized_at': _dt.datetime.utcnow().isoformat()}).eq('id', gw_id).execute()
                    winner_names = ', '.join([w['username'] for w in winners])
                    return jsonify({'status': 'ok', 'winners': winners, 'message': f'🏆 Kazananlar: {winner_names}!'})
                except Exception as e:
                    logger.error(f'Sonuçlandırma hatası: {e}')
                    return jsonify({'status': 'error', 'message': 'Hata oluştu.'})

            elif action == 'delete_giveaway':
                if not is_admin:
                    return jsonify({'status': 'error', 'message': 'Yetkisiz işlem.'})
                gw_id = data.get('giveaway_id')
                try:
                    supabase.table('giveaways').delete().eq('id', gw_id).execute()
                    return jsonify({'status': 'ok', 'message': 'Çekiliş silindi.'})
                except Exception as e:
                    logger.error(f'Çekiliş silme hatası: {e}')
                    return jsonify({'status': 'error', 'message': 'Silinemedi.'})

            elif action == 'admin_save_giveaway':
                if is_admin:
                    try:
                        raw_image = data.get('image', '')
                        final_image = raw_image
                        if raw_image.startswith('data:image'):
                            final_image = upload_base64_to_storage(raw_image, folder='giveaways')
                        else:
                            final_image = html.escape(raw_image)

                        new_gw = {
                            "id": str(uuid.uuid4()),
                            "title": html.escape(data.get('title', '')),
                            "desc": html.escape(data.get('desc', '')),
                            "image": final_image,
                            "participants": [],
                            "participants_ig": {},
                            "winner": None,
                            "is_active": True,
                            "created_at": int(time.time())
                        }
                        
                        res = supabase.table('settings').select('value').eq('id', 'giveaway_data').execute()
                        giveaways = []
                        if res.data and res.data[0].get('value'):
                            val = res.data[0]['value']
                            giveaways = json.loads(val) if isinstance(val, str) else val
                            if not isinstance(giveaways, list):
                                giveaways = [giveaways] if giveaways and giveaways.get('title') else []
                                
                        giveaways.insert(0, new_gw)
                        
                        supabase.table('settings').upsert({"id": "giveaway_data", "value": json.dumps(giveaways)}).execute()
                        
                        try:
                            broadcast_push(title=f"🎁 Yeni Çekiliş Başladı!", body=new_gw['title'], url="/")
                        except Exception as _exc:
                            logger.warning(f'Çekiliş push hatası: {_exc}')
                            
                        return jsonify({'status': 'ok'})
                    except Exception as main_e:
                        logger.error(f'Çekiliş kaydetme hatası: {main_e}')
                        return jsonify({'status': 'error', 'message': f'Hata: {str(main_e)}'})
                return jsonify({'status': 'error', 'message': 'Yetkisiz'})

            elif action == 'admin_draw_giveaway':
                if is_admin:
                    gw_id = data.get('gw_id')
                    if not gw_id: return jsonify({'status': 'error', 'message': 'Çekiliş ID eksik'})
                    
                    res = supabase.table('settings').select('value').eq('id', 'giveaway_data').execute()
                    if res.data and res.data[0].get('value'):
                        giveaways = json.loads(res.data[0]['value']) if isinstance(res.data[0]['value'], str) else res.data[0]['value']
                        if not isinstance(giveaways, list): giveaways = [giveaways]
                        
                        found = False
                        for gw_data in giveaways:
                            if gw_data.get('id') == gw_id and gw_data.get('is_active'):
                                found = True
                                parts = gw_data.get('participants', [])
                                ig_map = gw_data.get('participants_ig', {})
                                if parts:
                                    winner = random.choice(parts)
                                    winner_ig = ig_map.get(winner, '')
                                    gw_data['winner'] = winner
                                    gw_data['is_active'] = False
                                    supabase.table('settings').upsert({"id": "giveaway_data", "value": json.dumps(giveaways)}).execute()
                                    try:
                                        broadcast_push(title="🏆 Çekiliş Sonuçlandı!", body=f"Kazanan: {winner}! Tebrikler 🎉", url="/")
                                    except Exception as _exc:
                                        logger.warning(f'Çekiliş sonuç push hatası: {_exc}')
                                    return jsonify({'status': 'ok', 'winner': winner, 'winner_ig': winner_ig})
                                return jsonify({'status': 'error', 'message': 'Kimse katılmamış!'})
                        if not found:
                            return jsonify({'status': 'error', 'message': 'Aktif çekiliş bulunamadı.'})
                return jsonify({'status': 'error', 'message': 'Yetkisiz'})

            elif action == 'add_ban':
                if is_admin:
                    target_ban = data.get('username', '')
                    supabase.table('banned_users').upsert({"username": target_ban, "banned_by": current_username, "ts": int(time.time())}).execute()
                    app_cache.invalidate(f'ban:{target_ban}')
                    if not is_main_admin:
                        try:
                            log_entry = {'id': str(int(time.time()*1000)), 'admin': current_username, 'action': 'ban_user', 'target': target_ban, 'detail': f"Kullanıcı banlandı", 'ts': int(time.time())}
                            supabase.table('admin_logs').insert(log_entry).execute()
                            send_push_to_user('Admin', title=f"🚨 Kullanıcı Banlı", body=f"{current_username}, {target_ban} adlı kullanıcıyı banladı.", url="/")
                        except Exception as _exc:
                            logger.warning(f'Hata: {_exc}')
                    
            elif action == 'add_news':
                if is_main_admin:
                    data['id'] = str(data['id'])
                    # Base64 image varsa Supabase'e gönderme (sütun boyutu aşılır)
                    # Resim zaten upload_news_image ile R2'ye yüklendi, URL kaydedildi
                    img_val = data.get('image', '')
                    if img_val and isinstance(img_val, str) and img_val.startswith('data:'):
                        data['image'] = None  # base64'i Supabase'e gönderme
                    try:
                        supabase.table('news').upsert(data).execute()
                    except Exception as db_exc:
                        logger.error(f"add_news DB error: {db_exc}")
                        return jsonify({'status': 'error', 'message': 'Veritabanı hatası'})

            # =======================================================
            # ÇARK SİSTEMİ
            # =======================================================
            elif action == 'daily_spin':
                u_res = supabase.table('users').select('xp, stats').eq('username', current_username).execute()
                if not u_res.data:
                    return jsonify({'status': 'error', 'message': 'Kullanıcı bulunamadı.'})

                user_data = u_res.data[0]
                stats = user_data.get('stats', {}) or {}
                if isinstance(stats, str):
                    try:
                        stats = json.loads(stats)
                    except Exception:
                        stats = {}

                prem_tier = int(stats.get('premium_tier', 0))
                today_str = datetime.datetime.now().strftime("%Y-%m-%d")

                # Premium (Deluxe+) üyeye günde 2 hak, ücretsiz/Standart üyeye 1 hak
                max_spins = 2 if prem_tier >= 2 else 1

                last_spin_date = stats.get('last_spin_date', '')
                spin_count = int(stats.get('spin_count', 0))

                # Gün değiştiyse sayacı sıfırla
                if last_spin_date != today_str:
                    spin_count = 0

                # Bugün zaten hakkını kullandı mı?
                if spin_count >= max_spins:
                    return jsonify({
                        'status': 'error',
                        'message': f'Bugünlük çark hakkın bitti! Yarın tekrar dene. (Maksimum {max_spins} hak/gün)'
                    })

                # Ödül havuzu — id'ler frontend WHEEL_PRIZES ile eşleşmeli
                prizes = [
                    {"id": "xp_100",      "name": "100 XP",          "weight": 60,    "type": "xp",    "val": 100},
                    {"id": "xp_200",      "name": "200 XP",          "weight": 40,    "type": "xp",    "val": 200},
                    {"id": "xp_300",      "name": "300 XP",          "weight": 40,    "type": "xp",    "val": 300},
                    {"id": "xp_500",      "name": "500 XP",          "weight": 10,    "type": "xp",    "val": 500},
                    {"id": "xp_1000",     "name": "1000 XP",         "weight": 5,     "type": "xp",    "val": 1000},
                    {"id": "xp_10000",    "name": "10.000 XP",       "weight": 0.01,  "type": "xp",    "val": 10000},
                    {"id": "xp_100000",   "name": "100.000 XP",      "weight": 0.001, "type": "xp",    "val": 100000},
                    {"id": "prem_ult_30", "name": "1 Ay Ultra+",     "weight": 0.5,   "type": "prem",  "tier": 3, "days": 30},
                    {"id": "prem_dlx_30", "name": "1 Ay Deluxe",     "weight": 1,     "type": "prem",  "tier": 2, "days": 30},
                    {"id": "prem_std_30", "name": "1 Ay Standart",   "weight": 0.5,   "type": "prem",  "tier": 1, "days": 30},
                    {"id": "prem_ult_7",  "name": "1 Hft Ultra+",    "weight": 1,     "type": "prem",  "tier": 3, "days": 7},
                    {"id": "prem_dlx_7",  "name": "1 Hft Deluxe",    "weight": 1,     "type": "prem",  "tier": 2, "days": 7},
                    {"id": "prem_std_7",  "name": "1 Hft Standart",  "weight": 5,     "type": "prem",  "tier": 1, "days": 7},
                    {"id": "prem_ult_1",  "name": "1 Gün Ultra+",    "weight": 5,     "type": "prem",  "tier": 3, "days": 1},
                    {"id": "prem_dlx_1",  "name": "1 Gün Deluxe",    "weight": 5,     "type": "prem",  "tier": 2, "days": 1},
                    {"id": "rozet_sarki", "name": "🎵 Şanslı Rozet", "weight": 2,     "type": "rozet", "rozet_id": "spin_winner"},
                ]

                # weight=0 olan ödülleri havuzdan çıkar (ZeroDivisionError önleme)
                eligible_prizes = [p for p in prizes if p.get("weight", 0) > 0]
                weights_list = [p["weight"] for p in eligible_prizes]
                won_prize = random.choices(eligible_prizes, weights=weights_list, k=1)[0]
                won_prize = dict(won_prize)  # immutable copy

                # Sayaç ve tarih güncelle
                stats['spin_count'] = spin_count + 1
                stats['last_spin_date'] = today_str

                # Ödülü uygula
                if won_prize["type"] == "xp":
                    xp_gain = won_prize["val"]
                    new_xp = user_data.get('xp', 0) + xp_gain
                    stats['monthly_xp'] = stats.get('monthly_xp', 0) + xp_gain
                    stats['weekly_xp']  = stats.get('weekly_xp',  0) + xp_gain
                    supabase.table('users').update({"xp": new_xp, "stats": stats}).eq('username', current_username).execute()
                    _sync_score_columns(current_username, stats)

                elif won_prize["type"] == "rozet":
                    # Kullanıcının rozetler listesine ekle
                    rozetler = list(stats.get('badges', []) or [])
                    rozet_id = won_prize.get("rozet_id", "spin_winner")
                    if rozet_id not in rozetler:
                        rozetler.append(rozet_id)
                    stats['badges'] = rozetler
                    supabase.table('users').update({"stats": stats}).eq('username', current_username).execute()

                elif won_prize["type"] == "prem":
                    # Üyelik ödülleri hiçbir zaman üyeliğe eklenmez → her zaman XP'ye çevrilir
                    # Standart (tier 1): 1 gün = 200 XP
                    # Deluxe   (tier 2): 1 gün = 400 XP
                    # Ultra    (tier 3): 1 gün = 600 XP
                    xp_per_day_map = {1: 200, 2: 400, 3: 600}
                    won_tier  = int(won_prize.get("tier", 1))
                    won_days  = int(won_prize.get("days", 1))
                    xp_per_day = xp_per_day_map.get(won_tier, 200)
                    fallback_xp = xp_per_day * won_days

                    new_xp = user_data.get('xp', 0) + fallback_xp
                    stats['monthly_xp'] = stats.get('monthly_xp', 0) + fallback_xp
                    stats['weekly_xp']  = stats.get('weekly_xp',  0) + fallback_xp
                    supabase.table('users').update({"xp": new_xp, "stats": stats}).eq('username', current_username).execute()
                    _sync_score_columns(current_username, stats)

                    tier_name_map = {1: "Standart", 2: "Deluxe", 3: "Ultra"}
                    tier_name = tier_name_map.get(won_tier, "Standart")
                    won_prize['name'] = (
                        f"{won_days} gün {tier_name} üyelik → {fallback_xp} XP'ye çevrildi! "
                        f"({xp_per_day} XP/gün)"
                    )

                logger.info("Çark: %s → %s (spin_count=%d)", current_username, won_prize.get('name'), stats['spin_count'])
                return jsonify({
                    'status':     'ok',
                    'prize_name': won_prize['name'],
                    'prize_id':   won_prize['id'],
                    'spins_left': max(0, max_spins - stats['spin_count']),
                })
                    
            # ================================================================
            # GÖREV TAMAMLAMA (sunucu doğrulu XP ödülü)
            # ================================================================
            elif action == 'claim_mission':
                mission_id   = data.get('mission_id', '')
                mission_type = data.get('mission_type', '')   # 'perm' | 'daily' | 'weekly'
                xp_claim     = int(data.get('xp', 0))

                if not mission_id or mission_type not in ('perm', 'daily', 'weekly') or xp_claim <= 0:
                    return jsonify({'status': 'error', 'message': 'Geçersiz görev.'})

                # Sunucuda taze veriyi çek
                u_res = supabase.table('users').select('xp, stats').eq('username', current_username).execute()
                if not u_res.data:
                    return jsonify({'status': 'error'})

                srv_user  = u_res.data[0]
                srv_stats = srv_user.get('stats', {}) or {}
                if isinstance(srv_stats, str):
                    try: srv_stats = json.loads(srv_stats)
                    except: srv_stats = {}

                today_str = datetime.datetime.now().strftime("%Y-%m-%d")
                now_dt    = datetime.datetime.now()
                monday    = now_dt - datetime.timedelta(days=(now_dt.weekday()))
                week_key  = monday.strftime("%Y-%m-%d")

                # --- Kalıcı görevler ---
                PERM_MISSIONS = {
                    "m1":  {"type": "login_streak",   "target": 1,   "xp": 150},
                    "m2":  {"type": "login_streak",   "target": 7,   "xp": 600},
                    "m3":  {"type": "login_streak",   "target": 30,  "xp": 6000},
                    "m4":  {"type": "login_streak",   "target": 100, "xp": 30000},
                    "m5":  {"type": "total_messages", "target": 1,   "xp": 60},
                    "m6":  {"type": "total_messages", "target": 50,  "xp": 900},
                    "m7":  {"type": "total_messages", "target": 200, "xp": 3000},
                    "m8":  {"type": "markers",        "target": 1,   "xp": 150},
                    "m9":  {"type": "markers",        "target": 10,  "xp": 1500},
                    "m10": {"type": "market",         "target": 1,   "xp": 150},
                    "m11": {"type": "market",         "target": 5,   "xp": 900},
                    "m12": {"type": "events",         "target": 1,   "xp": 300},
                    "m13": {"type": "events",         "target": 5,   "xp": 1500},
                }

                # --- Günlük görev setleri ---
                day_num = int(datetime.datetime.now().timestamp() // 86400)
                DAILY_SETS = [
                    {"d1":{"type":"daily_login","target":1,"xp":90},"d2":{"type":"daily_msg","target":3,"xp":150},"d3":{"type":"daily_marker","target":1,"xp":240}},
                    {"d1":{"type":"daily_login","target":1,"xp":90},"d4":{"type":"daily_ai","target":1,"xp":120},"d5":{"type":"daily_market","target":1,"xp":60}},
                    {"d1":{"type":"daily_login","target":1,"xp":90},"d6":{"type":"daily_msg","target":5,"xp":210},"d7":{"type":"daily_radar","target":1,"xp":180}},
                ]
                today_daily = DAILY_SETS[day_num % len(DAILY_SETS)]

                # --- Haftalık görev setleri ---
                week_num = int(datetime.datetime.now().timestamp() // (86400 * 7))
                WEEKLY_SETS = [
                    {"w1":{"type":"weekly_msg","target":20,"xp":600},"w2":{"type":"weekly_marker","target":2,"xp":450}},
                    {"w3":{"type":"weekly_event","target":1,"xp":750},"w4":{"type":"weekly_market","target":1,"xp":450}},
                    {"w5":{"type":"weekly_radar","target":3,"xp":600},"w6":{"type":"weekly_ai","target":5,"xp":540}},
                ]
                today_weekly = WEEKLY_SETS[week_num % len(WEEKLY_SETS)]

                earned_xp = 0

                if mission_type == 'perm':
                    m = PERM_MISSIONS.get(mission_id)
                    if not m:
                        return jsonify({'status': 'error', 'message': 'Görev bulunamadı.'})
                    if srv_stats.get('missions', {}).get(mission_id):
                        return jsonify({'status': 'ok', 'earned_xp': 0, 'already_done': True})
                    progress = srv_stats.get(m['type'], 0)
                    if progress < m['target']:
                        return jsonify({'status': 'ok', 'earned_xp': 0, 'not_ready': True})
                    if xp_claim != m['xp']:
                        return jsonify({'status': 'error', 'message': 'XP tutarsızlığı.'})
                    if 'missions' not in srv_stats:
                        srv_stats['missions'] = {}
                    srv_stats['missions'][mission_id] = True
                    earned_xp = m['xp']

                elif mission_type == 'daily':
                    m = today_daily.get(mission_id)
                    if not m:
                        return jsonify({'status': 'ok', 'earned_xp': 0, 'not_ready': True})
                    dm = srv_stats.get('daily_missions', {})
                    if dm.get('date') != today_str:
                        dm = {'date': today_str, 'daily_login': 1}
                    done_key = 'done_' + mission_id
                    if dm.get(done_key):
                        return jsonify({'status': 'ok', 'earned_xp': 0, 'already_done': True})
                    progress = 1 if m['type'] == 'daily_login' else dm.get(m['type'], 0)
                    if progress < m['target']:
                        return jsonify({'status': 'ok', 'earned_xp': 0, 'not_ready': True})
                    if xp_claim != m['xp']:
                        return jsonify({'status': 'error', 'message': 'XP tutarsızlığı.'})
                    dm[done_key] = True
                    srv_stats['daily_missions'] = dm
                    earned_xp = m['xp']

                elif mission_type == 'weekly':
                    m = today_weekly.get(mission_id)
                    if not m:
                        return jsonify({'status': 'ok', 'earned_xp': 0, 'not_ready': True})
                    wm = srv_stats.get('weekly_missions', {})
                    if wm.get('week') != week_key:
                        wm = {'week': week_key}
                    done_key = 'done_' + mission_id
                    if wm.get(done_key):
                        return jsonify({'status': 'ok', 'earned_xp': 0, 'already_done': True})
                    progress = wm.get(m['type'], 0)
                    if progress < m['target']:
                        return jsonify({'status': 'ok', 'earned_xp': 0, 'not_ready': True})
                    if xp_claim != m['xp']:
                        return jsonify({'status': 'error', 'message': 'XP tutarsızlığı.'})
                    wm[done_key] = True
                    srv_stats['weekly_missions'] = wm
                    earned_xp = m['xp']

                if earned_xp > 0:
                    new_xp = srv_user.get('xp', 0) + earned_xp
                    srv_stats['monthly_xp'] = srv_stats.get('monthly_xp', 0) + earned_xp
                    srv_stats['weekly_xp']  = srv_stats.get('weekly_xp',  0) + earned_xp
                    supabase.table('users').update({'xp': new_xp, 'stats': srv_stats}).eq('username', current_username).execute()
                    _sync_score_columns(current_username, srv_stats)
                    return jsonify({'status': 'ok', 'earned_xp': earned_xp, 'new_xp': new_xp})

                return jsonify({'status': 'error'})

            # ================================================================
            # YORUMLAR (Marker & Etkinlik yorumları)
            # ================================================================
            elif action == 'rate_marker':
                marker_id = str(data.get('marker_id', '')).strip()
                try:
                    rating = int(data.get('rating', 0))
                except (ValueError, TypeError):
                    rating = 0
                if not marker_id or rating < 1 or rating > 5:
                    return jsonify({'status': 'error', 'message': 'Geçersiz puan!'})
                m_res = supabase.table('markers').select('ratings').eq('id', marker_id).execute()
                if m_res.data:
                    ratings = m_res.data[0].get('ratings') or {}
                    if isinstance(ratings, str):
                        try: ratings = json.loads(ratings)
                        except: ratings = {}
                    ratings[current_username] = rating
                    avg = round(sum(ratings.values()) / len(ratings), 1)
                    supabase.table('markers').update({'ratings': ratings, 'avg_rating': avg}).eq('id', marker_id).execute()

            elif action == 'report_marker':
                marker_id = str(data.get('marker_id', ''))
                marker_name = html.escape(data.get('marker_name', 'Bilinmeyen yer'))
                reason = html.escape(data.get('reason', 'Bu yer mevcut değil').strip()[:200])
                if not marker_id:
                    return jsonify({'status': 'error', 'message': 'Marker ID eksik!'})
                # Admin'e Telegram mesajı gönder
                report_id = str(int(time.time() * 1000))
                try:
                    report_entry = {
                        'id': report_id,
                        'marker_id': marker_id,
                        'marker_name': marker_name,
                        'reporter': current_username,
                        'reason': reason,
                        'ts': int(time.time()),
                        'status': 'pending'
                    }
                    supabase.table('marker_reports').insert(report_entry).execute()
                except Exception as db_err:
                    logger.warning(f'marker_reports kayıt hatası (tablo yoksa sorun değil): {db_err}')
                # Admin'e push bildirim gönder
                try:
                    send_push_to_user('Admin',
                        title=f'📍 Yer Bildirimi: {marker_name}',
                        body=f'{current_username}: {reason[:80]}',
                        url='/'
                    )
                except Exception as push_err:
                    logger.warning(f'Admin push hatası: {push_err}')
                # Admin'e Telegram mesajı gönder
                try:
                    from telegram_bot import send_telegram_message
                    send_telegram_message(
                        f'\U0001f4cd Yer Bildirimi\n'
                        f'Yer: {marker_name}\n'
                        f'Bildiren: {current_username}\n'
                        f'Sebep: {reason}\n'
                        f'Marker ID: {marker_id}\n'
                        f'Rapor ID: {report_id}'
                    )
                except Exception as tg_err:
                    logger.warning(f'Telegram bildirim hatası: {tg_err}')
                return jsonify({'status': 'ok', 'message': 'Bildiriminiz alındı, teşekkürler!'})

            elif action == 'get_marker_reports':
                if not is_admin:
                    return jsonify({'status': 'error', 'message': 'Yetkisiz!'})
                try:
                    rep_res = supabase.table('marker_reports').select('*').eq('status', 'pending').order('id', desc=True).limit(50).execute()
                    return jsonify({'status': 'ok', 'reports': rep_res.data or []})
                except Exception as e:
                    return jsonify({'status': 'ok', 'reports': []})

            elif action == 'resolve_marker_report':
                if not is_admin:
                    return jsonify({'status': 'error', 'message': 'Yetkisiz!'})
                report_id = str(data.get('report_id', ''))
                marker_id = str(data.get('marker_id', ''))
                action_taken = data.get('action_taken', 'dismiss')  # 'delete' or 'dismiss'
                if action_taken == 'delete' and marker_id:
                    try:
                        supabase.table('markers').delete().eq('id', marker_id).execute()
                        supabase.table('comments').delete().eq('target_id', marker_id).execute()
                    except Exception as del_err:
                        logger.warning(f'Marker silme hatası: {del_err}')
                try:
                    supabase.table('marker_reports').update({'status': 'resolved'}).eq('id', report_id).execute()
                except Exception:
                    pass
                return jsonify({'status': 'ok'})

                marker_id = str(data.get('marker_id',''))
                reason   = html.escape(data.get('reason','').strip())
                if not marker_id or not reason:
                    return jsonify({'status':'error','message':'Sebep yazin!'})
                m_res = supabase.table('markers').select('danger_reports').eq('id', marker_id).execute()
                if m_res.data:
                    dr = m_res.data[0].get('danger_reports') or []
                    if isinstance(dr, str):
                        try: dr = json.loads(dr)
                        except: dr = []
                    dr.append({'user': current_username, 'reason': reason, 'ts': int(time.time())})
                    supabase.table('markers').update({'danger_reports': dr, 'is_dangerous': True}).eq('id', marker_id).execute()
                    # Push admins
                    try:
                        m_name = data.get('marker_name','Bir rampa')
                        broadcast_push(title=f"⚠️ Tehlike: {m_name}", body=f"{current_username}: {reason[:60]}", url="/")
                    except Exception as e:
                        print(f"⚠️ Tehlike bildirimi push hatası: {e}")

            elif action == 'add_reaction':
                msg_id  = str(data.get('msg_id',''))
                emoji   = data.get('emoji','')
                if not msg_id or not emoji: return jsonify({'status':'error'})
                r_res = supabase.table('messages').select('reactions, user').eq('id', msg_id).execute()
                if r_res.data:
                    reactions  = r_res.data[0].get('reactions') or {}
                    msg_author = r_res.data[0].get('user', '')
                    if isinstance(reactions, str):
                        try: reactions = json.loads(reactions)
                        except: reactions = {}
                    users = reactions.get(emoji, [])
                    was_reacted = current_username in users
                    if was_reacted:
                        users.remove(current_username)
                    else:
                        users.append(current_username)
                    reactions[emoji] = users
                    supabase.table('messages').update({'reactions': reactions}).eq('id', msg_id).execute()
                    # ── Mesaj sahibine tepki bildirimi (yeni tepkide, geri almada değil, 5 dk cooldown) ──
                    if not was_reacted and msg_author and msg_author != current_username and msg_author != 'Freerider AI':
                        try:
                            _react_notif_key = f'react_notif_{msg_author}_{current_username}'
                            if not app_cache.get(_react_notif_key):
                                send_push_to_user(
                                    msg_author,
                                    title=f"{emoji} {current_username} mesajına tepki verdi!",
                                    body="Chat'teki mesajına bir tepki geldi",
                                    url="/"
                                )
                                app_cache.set(_react_notif_key, True, ttl=300)  # 5 dk cooldown
                        except Exception as _exc:
                            logger.warning(f'Hata: {_exc}')

            elif action == 'add_comment':
                target_type = data.get('target_type')  # 'marker' or 'event'
                target_id   = str(data.get('target_id', ''))
                text        = html.escape(data.get('text', '').strip())
                if not text or not target_id:
                    return jsonify({'status': 'error', 'message': 'Yorum bos olamaz!'})
                comment = {
                    'id': str(int(time.time() * 1000)),
                    'target_type': target_type,
                    'target_id': target_id,
                    'user': current_username,
                    'text': text,
                    'created_at': int(time.time())
                }
                supabase.table('comments').insert(comment).execute()
                # Notify marker/event owner
                try:
                    if target_type == 'marker':
                        m_res = supabase.table('markers').select('addedBy').eq('id', target_id).execute()
                        if m_res.data and m_res.data[0]['addedBy'] != current_username:
                            send_push_to_user(m_res.data[0]['addedBy'],
                                title=f"💬 {current_username} rampanı yorumladı!",
                                body=text[:80], url="/")
                    elif target_type == 'event':
                        e_res = supabase.table('events').select('creator').eq('id', target_id).execute()
                        if e_res.data and e_res.data[0]['creator'] != current_username:
                            send_push_to_user(e_res.data[0]['creator'],
                                title=f"💬 {current_username} etkinliğini yorumladı!",
                                body=text[:80], url="/")
                except Exception as _exc:
                    logger.warning(f'Hata: {_exc}')

            elif action == 'delete_comment':
                cid = str(data.get('id', ''))
                c_res = supabase.table('comments').select('user').eq('id', cid).execute()
                if c_res.data:
                    if c_res.data[0]['user'] == current_username or is_admin:
                        supabase.table('comments').delete().eq('id', cid).execute()

            elif action == 'get_comments':
                target_id = str(data.get('target_id', ''))
                comments_data = []
                try:
                    c_res = supabase.table('comments').select('*').eq('target_id', target_id).execute()
                    comments_data = c_res.data or []
                    # Python tarafında güvenli sıralama
                    def _safe_sort_key(x):
                        return str(x.get('created_at') or '')
                    comments_data.sort(key=_safe_sort_key)
                except Exception as e:
                    logger.error(f"get_comments hatası: {e}")
                    comments_data = []
                return jsonify({'status': 'ok', 'comments': comments_data})

            # ================================================================
            # STORY SİSTEMİ (24 saat kaybolan - Premium)
            # ================================================================
            elif action == 'add_story':
                try:
                    st_res = supabase.table('users').select('stats').eq('username', current_username).execute()
                    prem = int((st_res.data[0].get('stats') or {}).get('premium_tier', 0)) if st_res.data else 0
                except (IndexError, TypeError, ValueError, AttributeError):
                    prem = 0
                if prem < 1:
                    return jsonify({'status': 'error', 'message': 'Story paylaşmak için en az Standart üyelik gerekli!'})
                story = {
                    'id': str(int(time.time() * 1000)),
                    'user': current_username,
                    'text': html.escape(data.get('text', '').strip()),
                    'image': data.get('image', ''),
                    'expires_at': int(time.time()) + 86400,  # 24 saat
                    'created_at': int(time.time()),
                    'viewers': []
                }
                supabase.table('stories').insert(story).execute()
                # ── Yeni story bildirimi: herkese ──
                try:
                    story_text = data.get('text', '').strip()
                    story_preview = f"'{story_text[:40]}'" if story_text else "Yeni bir fotoğraf paylaştı"
                    broadcast_push(
                        title=f"📸 {current_username} story paylaştı!",
                        body=f"{story_preview} — 24 saat içinde kayboluyor!",
                        exclude_user=current_username,
                        url="/"
                    )
                except Exception as _exc:
                    logger.warning(f'Hata: {_exc}')

            elif action == 'view_story':
                sid = str(data.get('id', ''))
                s_res = supabase.table('stories').select('viewers').eq('id', sid).execute()
                if s_res.data:
                    viewers = s_res.data[0].get('viewers', [])
                    if current_username not in viewers:
                        viewers.append(current_username)
                        supabase.table('stories').update({'viewers': viewers}).eq('id', sid).execute()

            elif action == 'delete_story':
                sid = str(data.get('id', ''))
                s_res = supabase.table('stories').select('user').eq('id', sid).execute()
                if s_res.data and (s_res.data[0]['user'] == current_username or is_admin):
                    supabase.table('stories').delete().eq('id', sid).execute()

            elif action == 'get_stories':
                now_ts = int(time.time())
                s_res = supabase.table('stories').select('*').gt('expires_at', now_ts).order('id', desc=True).limit(50).execute()
                return jsonify({'status': 'ok', 'stories': s_res.data or []})

            # ================================================================
            # MEDYA YÜKLEME (R2'ye direkt yükleme — video/fotoğraf)
            # ================================================================
            elif action == 'upload_media':
                media_data = data.get('media_data', '')
                folder = data.get('folder', 'uploads')
                if not media_data:
                    return jsonify({'status': 'error', 'message': 'Medya verisi eksik!'})
                if not (media_data.startswith('data:image/') or media_data.startswith('data:video/') or media_data.startswith('data:audio/')):
                    return jsonify({'status': 'error', 'message': 'Geçersiz medya formatı!'})
                url = upload_base64_to_storage(media_data, folder)
                if url and not url.startswith('data:'):
                    return jsonify({'status': 'ok', 'url': url})
                return jsonify({'status': 'error', 'message': 'Medya yüklenemedi, tekrar deneyin.'})

            # ================================================================
            # REELS SİSTEMİ (TikTok/Instagram tarzı kısa video & fotoğraf)
            # ================================================================
            elif action == 'add_reel':
                # Günlük yükleme limiti kontrolü
                try:
                    u_reel_res = supabase.table('users').select('stats').eq('username', current_username).execute()
                    u_stats_r = u_reel_res.data[0].get('stats', {}) or {} if u_reel_res.data else {}
                    if isinstance(u_stats_r, str):
                        try: u_stats_r = json.loads(u_stats_r)
                        except: u_stats_r = {}
                    prem_r = int(u_stats_r.get('premium_tier', 0))
                except Exception as _exc:
                    prem_r = 0
                    u_stats_r = {}

                today_str = datetime.datetime.now().strftime("%Y-%m-%d")
                reel_today = u_stats_r.get('reel_upload_date', '')
                reel_count_today = u_stats_r.get('reel_upload_count', 0)
                if reel_today != today_str:
                    reel_count_today = 0

                media_type = data.get('media_type', 'image')  # 'image' veya 'video'

                # Limit: üyesiz=sadece 1 resim, Standart=1 video/resim, Deluxe/Ultra=2
                if prem_r == 0:
                    if media_type == 'video':
                        return jsonify({'status': 'error', 'message': 'Video yüklemek için en az Standart üyelik gereklidir!'})
                    if reel_count_today >= 1:
                        return jsonify({'status': 'error', 'message': 'Günlük ücretsiz Reel limitine (1 fotoğraf) ulaştınız!'})
                elif prem_r == 1:
                    if reel_count_today >= 1:
                        return jsonify({'status': 'error', 'message': 'Standart üyeler günde 1 Reel paylaşabilir. Deluxe/Ultra ile 2ye cikar!'})
                else:  # Deluxe/Ultra
                    if reel_count_today >= 2:
                        return jsonify({'status': 'error', 'message': 'Günlük Reel limitine (2) ulaştınız!'})

                # Medya URL'i al — upload_media ile önceden R2'ye yüklenmeli
                raw_media = data.get('media_url', '')
                # Eğer hâlâ base64 geldiyse (fallback) yükle, ama normalde URL gelir
                if raw_media and (raw_media.startswith('data:image/') or raw_media.startswith('data:video/')):
                    raw_media = upload_base64_to_storage(raw_media, 'reels')
                if not raw_media or raw_media.startswith('data:'):
                    return jsonify({'status': 'error', 'message': 'Medya yüklenemedi, lütfen tekrar deneyin.'})

                reel = {
                    'id': str(int(time.time() * 1000)) + '_' + current_username,
                    'user': current_username,
                    'media_url': raw_media,
                    'media_type': media_type,
                    'caption': html.escape(data.get('caption', '').strip()[:200]),
                    'likes': [],
                    'comment_count': 0,
                    'created_at': int(time.time() * 1000)
                }

                try:
                    supabase.table('reels').insert(reel).execute()
                except Exception as e:
                    error_msg = str(e).lower()
                    print(f"Reel insert primary error: {error_msg}")
                    # If some columns don't exist in reels table, remove them
                    if 'media_type' in error_msg: reel.pop('media_type', None)
                    if 'comment_count' in error_msg: reel.pop('comment_count', None)
                    # If it expects int(time.time()) instead of milliseconds
                    if 'created_at' in error_msg or 'timestamp' in error_msg or 'integer' in error_msg or 'bigint' in error_msg:
                        reel['created_at'] = int(time.time())
                    
                    try:
                        supabase.table('reels').insert(reel).execute()
                    except Exception as e2:
                        error_msg2 = str(e2).lower()
                        print(f"Reel insert secondary error: {error_msg2}")
                        if 'created_at' in error_msg2: reel.pop('created_at', None)
                        try:
                            supabase.table('reels').insert(reel).execute()
                        except Exception as e3:
                            print(f"Reel final insert error: {e3}")
                            return jsonify({'status': 'error', 'message': f'Veritabanı hatası: {str(e3)}'})

                # Günlük upload sayısını artır
                try:
                    u_stats_r['reel_upload_date'] = today_str
                    u_stats_r['reel_upload_count'] = reel_count_today + 1
                    supabase.table('users').update({'stats': u_stats_r}).eq('username', current_username).execute()
                except Exception as e:
                    print(f"⚠️ Reel upload count güncelleme hatası: {e}")

                return jsonify({'status': 'ok'})

            elif action == 'get_reels':
                offset = int(data.get('offset', 0))
                try:
                    r_res = supabase.table('reels').select('*').execute()
                    all_reels = r_res.data or []
                    
                    def _safe_sort_key(x):
                        return str(x.get('created_at') or '')
                    
                    all_reels.sort(key=_safe_sort_key, reverse=True)
                    
                    reels_out = []
                    for r in all_reels[offset:offset+20]:
                        url = r.get('media_url', '') or ''
                        # Base64 veya boş URL içeren eski kayıtları atla
                        if url.startswith('data:') or not url:
                            continue
                        reels_out.append(r)
                    return jsonify({'status': 'ok', 'reels': reels_out})
                except Exception as e:
                    logger.error(f"get_reels hatası: {e}")
                    return jsonify({'status': 'ok', 'reels': []})

            elif action == 'like_reel':
                reel_id = str(data.get('reel_id', ''))
                r_res = supabase.table('reels').select('likes, user').eq('id', reel_id).execute()
                if r_res.data:
                    likes      = r_res.data[0].get('likes', []) or []
                    reel_owner = r_res.data[0].get('user', '')
                    was_liked  = current_username in likes
                    if was_liked:
                        likes.remove(current_username)
                    else:
                        likes.append(current_username)
                    supabase.table('reels').update({'likes': likes}).eq('id', reel_id).execute()
                    # ── Yeni beğeni → reel sahibine MİLESTONE bildirimi ──
                    # Her beğenide değil; 1, 5, 10, 20, 30, 50, 100, 200, 500 beğenide bildirim gider.
                    if not was_liked and reel_owner and reel_owner != current_username:
                        try:
                            new_like_count = len(likes)
                            _LIKE_MILESTONES = {1, 5, 10, 20, 30, 50, 100, 200, 500}
                            if new_like_count == 1:
                                send_push_to_user(
                                    reel_owner,
                                    title=f"❤️ {current_username} reelini beğendi!",
                                    body="Reeline ilk beğeni geldi! 🔥",
                                    url="/"
                                )
                            elif new_like_count in _LIKE_MILESTONES:
                                send_push_to_user(
                                    reel_owner,
                                    title=f"🔥 Reelin {new_like_count} beğeni aldı!",
                                    body=f"{current_username} ve diğerleri reelini seviyor ❤️",
                                    url="/"
                                )
                        except Exception as _exc:
                            logger.warning(f'Hata: {_exc}')
                    return jsonify({'status': 'ok', 'likes': len(likes), 'liked': current_username in likes})
                return jsonify({'status': 'error'})

            elif action == 'delete_reel':
                reel_id = str(data.get('reel_id', ''))
                r_res = supabase.table('reels').select('user').eq('id', reel_id).execute()
                if r_res.data and (r_res.data[0]['user'] == current_username or is_admin):
                    reel_owner = r_res.data[0]['user']
                    supabase.table('reels').delete().eq('id', reel_id).execute()
                    # Sub-admin log
                    if is_admin and not is_main_admin:
                        try:
                            log_entry = {'id': str(int(time.time()*1000)), 'admin': current_username, 'action': 'delete_reel', 'target': reel_owner, 'detail': f"Reel silindi: {reel_id}", 'ts': int(time.time())}
                            supabase.table('admin_logs').insert(log_entry).execute()
                            send_push_to_user('Admin', title=f"⚠️ Admin Bildirimi", body=f"{current_username}, {reel_owner} adlı kullanıcının reelini sildi.", url="/")
                        except Exception as log_e:
                            print(f"Admin log hatası: {log_e}")
                return jsonify({'status': 'ok'})

            # ================================================================
            # ADMİN YÖNETİM SİSTEMİ (Ana admin: atama/görevden alma, loglar)
            # ================================================================
            elif action == 'assign_sub_admin':
                if not is_main_admin:
                    return jsonify({'status': 'error', 'message': 'Sadece Ana Admin bu işlemi yapabilir!'})
                target = data.get('username', '').strip()
                if not target or target == 'Admin':
                    return jsonify({'status': 'error', 'message': 'Geçersiz kullanıcı!'})
                u_res = supabase.table('users').select('username, role').eq('username', target).execute()
                if not u_res.data:
                    return jsonify({'status': 'error', 'message': 'Kullanıcı bulunamadı!'})
                supabase.table('users').update({'role': 'SubAdmin'}).eq('username', target).execute()
                try:
                    log_entry = {'id': str(int(time.time()*1000)), 'admin': 'Admin', 'action': 'assign_admin', 'target': target, 'detail': f"{target} yardımcı yönetici yapıldı", 'ts': int(time.time())}
                    supabase.table('admin_logs').insert(log_entry).execute()
                    send_push_to_user(target, title="👑 Yönetici Yetkiniz Verildi", body="Ana admin sizi yardımcı yönetici yaptı!", url="/")
                except Exception as _exc:
                    logger.warning(f'Hata: {_exc}')
                return jsonify({'status': 'ok'})

            elif action == 'revoke_sub_admin':
                if not is_main_admin:
                    return jsonify({'status': 'error', 'message': 'Sadece Ana Admin bu işlemi yapabilir!'})
                target = data.get('username', '').strip()
                if not target or target == 'Admin':
                    return jsonify({'status': 'error', 'message': 'Geçersiz kullanıcı!'})
                supabase.table('users').update({'role': 'user'}).eq('username', target).execute()
                try:
                    log_entry = {'id': str(int(time.time()*1000)), 'admin': 'Admin', 'action': 'revoke_admin', 'target': target, 'detail': f"{target} yönetici yetkisi alındı", 'ts': int(time.time())}
                    supabase.table('admin_logs').insert(log_entry).execute()
                    send_push_to_user(target, title="🚫 Yönetici Yetkiniz Alındı", body="Ana admin yönetici yetkinizi geri aldı.", url="/")
                except Exception as _exc:
                    logger.warning(f'Hata: {_exc}')
                return jsonify({'status': 'ok'})


            elif action == 'admin_check_user_details':
                if not is_admin:
                    return jsonify({'status': 'error', 'message': 'Yetkisiz!'})
                target = data.get('username')
                if not target:
                    return jsonify({'status': 'error', 'message': 'Kullanıcı adı belirtilmedi.'})
                
                u_res = supabase.table('users').select('username, city, xp, role, stats').ilike('username', target).execute()
                if not u_res.data:
                    return jsonify({'status': 'error', 'message': 'Kullanıcı bulunamadı.'})
                
                u_data = u_res.data[0]
                stats = u_data.get('stats', {})
                if isinstance(stats, str):
                    try: stats = json.loads(stats)
                    except: stats = {}
                
                tier = int(stats.get('premium_tier', 0))
                exp_dt = stats.get('premium_expire_date', '-')
                is_override = stats.get('gp_admin_override', False)
                
                # Check ban
                try:
                    banned_res = supabase.table('banned_users').select('username').ilike('username', target).execute()
                    is_banned = len(banned_res.data) > 0
                except:
                    is_banned = False
                
                source = "Sistem / Google Play"
                if tier > 0:
                    if is_override:
                        source = "Yönetici (Admin) Ataması"
                else:
                    source = "Premium Yok"

                return jsonify({
                    'status': 'ok',
                    'user': {
                        'username': u_data.get('username'),
                        'email': stats.get('email', '-'),
                        'city': u_data.get('city', '-'),
                        'xp': u_data.get('xp', 0),
                        'role': u_data.get('role', 'User'),
                        'created_at': str(stats.get('join_date', '-')),
                        'is_banned': is_banned
                    },
                    'premium': {
                        'tier': tier,
                        'expire_date': exp_dt,
                        'source': source
                    }
                })

            elif action == 'get_admin_logs':
                if not is_admin:
                    return jsonify({'status': 'error', 'message': 'Yetkisiz!'})
                try:
                    logs_res = supabase.table('admin_logs').select('*').order('id', desc=True).limit(100).execute()
                    return jsonify({'status': 'ok', 'logs': logs_res.data or []})
                except Exception as e:
                    return jsonify({'status': 'ok', 'logs': []})

            elif action == 'get_user_activity':
                if not is_admin:
                    return jsonify({'status': 'error', 'message': 'Yetkisiz!'})
                target = data.get('username', '').strip()
                if not target:
                    return jsonify({'status': 'error', 'message': 'Kullanıcı belirtilmedi!'})
                result = {}
                try:
                    msgs_res = supabase.table('messages').select('*').eq('user', target).order('id', desc=True).limit(30).execute()
                    result['messages'] = msgs_res.data or []
                except Exception: result['messages'] = []
                try:
                    dms_res = supabase.table('dms').select('*').contains('participants', [target]).order('id', desc=True).limit(30).execute()
                    result['dms'] = dms_res.data or []
                except Exception: result['dms'] = []
                try:
                    reels_res = supabase.table('reels').select('*').eq('user', target).order('id', desc=True).limit(20).execute()
                    result['reels'] = reels_res.data or []
                except Exception: result['reels'] = []
                try:
                    markers_res = supabase.table('markers').select('*').eq('addedBy', target).execute()
                    result['markers'] = markers_res.data or []
                except Exception: result['markers'] = []
                try:
                    market_res = supabase.table('market').select('*').eq('owner', target).execute()
                    result['market'] = market_res.data or []
                except Exception: result['market'] = []
                return jsonify({'status': 'ok', 'activity': result})

            elif action == 'get_all_users_admin':
                # ── Admin paneli için tüm kullanıcıları çek (50 limit yok) ──
                if not is_admin:
                    return jsonify({'status': 'error', 'message': 'Yetkisiz!'})
                try:
                    _page = max(1, int(data.get('page', 1)))
                    _per_page = min(500, max(10, int(data.get('per_page', 200))))
                    _offset = (_page - 1) * _per_page
                    _search = str(data.get('search', '')).strip().lower()

                    _q = supabase.table('users').select(
                        'username, name, avatar, role, xp, stats, accepted_chat_rules',
                        count='exact'
                    ).order('xp', desc=True)

                    if _search:
                        _q = _q.ilike('username', f'%{_search}%')

                    _q = _q.range(_offset, _offset + _per_page - 1)
                    _all_res = _q.execute()

                    return jsonify({
                        'status': 'ok',
                        'users': _all_res.data or [],
                        'total': _all_res.count or 0,
                        'page': _page,
                        'per_page': _per_page,
                    })
                except Exception as _exc:
                    logger.warning(f'get_all_users_admin hatası: {_exc}')
                    return jsonify({'status': 'ok', 'users': [], 'total': 0})

            # NOT: get_admin_logs zaten 2503-2510 satırlarında tanımlı — duplicate kaldırıldı

            elif action == 'get_all_sub_admins':
                if not is_main_admin:
                    return jsonify({'status': 'error', 'message': 'Yetkisiz!'})
                try:
                    sa_res = supabase.table('users').select('username, avatar, xp').eq('role', 'SubAdmin').execute()
                    return jsonify({'status': 'ok', 'sub_admins': sa_res.data or []})
                except Exception as _exc:
                    return jsonify({'status': 'ok', 'sub_admins': []})

            elif action == 'admin_notify_main':
                # Sub-admin ana admine bildirim gönderir
                if not is_admin:
                    return jsonify({'status': 'error', 'message': 'Yetkisiz!'})
                msg_text = html.escape(data.get('message', '').strip()[:500])
                if not msg_text:
                    return jsonify({'status': 'error', 'message': 'Mesaj boş olamaz!'})
                try:
                    log_entry = {'id': str(int(time.time()*1000)), 'admin': current_username, 'action': 'notify_main', 'target': '', 'detail': msg_text, 'ts': int(time.time())}
                    supabase.table('admin_logs').insert(log_entry).execute()
                    send_push_to_user('Admin', title=f"📢 Admin Bildirimi: {current_username}", body=msg_text[:100], url="/")
                except Exception as e:
                    print(f"Admin notify hatası: {e}")
                return jsonify({'status': 'ok'})

            elif action == 'admin_delete_message_by_id':
                # Admin herhangi bir mesajı silebilir ve log tutar
                if not is_admin:
                    return jsonify({'status': 'error', 'message': 'Yetkisiz!'})
                msg_id = str(data.get('msg_id', ''))
                msg_res2 = supabase.table('messages').select('user, text').eq('id', msg_id).execute()
                if msg_res2.data:
                    msg_owner = msg_res2.data[0].get('user', '')
                    msg_preview = str(msg_res2.data[0].get('text', ''))[:60]
                    supabase.table('messages').delete().eq('id', msg_id).execute()
                    if not is_main_admin:
                        try:
                            log_entry = {'id': str(int(time.time()*1000)), 'admin': current_username, 'action': 'delete_message', 'target': msg_owner, 'detail': f"Mesaj silindi: {msg_preview}", 'ts': int(time.time())}
                            supabase.table('admin_logs').insert(log_entry).execute()
                            send_push_to_user('Admin', title=f"⚠️ Mesaj Silindi", body=f"{current_username} → {msg_owner}: {msg_preview}", url="/")
                        except Exception as _exc:
                            logger.warning(f'Hata: {_exc}')
                return jsonify({'status': 'ok'})

            elif action == 'admin_delete_marker_by_id':
                if not is_admin:
                    return jsonify({'status': 'error', 'message': 'Yetkisiz!'})
                marker_id = str(data.get('marker_id', ''))
                m_res2 = supabase.table('markers').select('addedBy, name').eq('id', marker_id).execute()
                if m_res2.data:
                    m_owner = m_res2.data[0].get('addedBy', '')
                    m_name = str(m_res2.data[0].get('name', ''))
                    supabase.table('markers').delete().eq('id', marker_id).execute()
                    if not is_main_admin:
                        try:
                            log_entry = {'id': str(int(time.time()*1000)), 'admin': current_username, 'action': 'delete_marker', 'target': m_owner, 'detail': f"Yer silindi: {m_name}", 'ts': int(time.time())}
                            supabase.table('admin_logs').insert(log_entry).execute()
                            send_push_to_user('Admin', title=f"⚠️ Yer Silindi", body=f"{current_username} → {m_name} ({m_owner})", url="/")
                        except Exception as _exc:
                            logger.warning(f'Hata: {_exc}')
                return jsonify({'status': 'ok'})

            elif action == 'admin_ban_user':
                if not is_admin:
                    return jsonify({'status': 'error', 'message': 'Yetkisiz!'})
                target = data.get('username', '').strip()
                reason = html.escape(data.get('reason', 'Kural ihlali').strip()[:200])
                if not target:
                    return jsonify({'status': 'error', 'message': 'Kullanıcı belirtilmedi!'})
                try:
                    supabase.table('banned_users').upsert({'username': target, 'reason': reason, 'banned_by': current_username}).execute()
                    supabase.table('users').update({'is_banned': True}).eq('username', target).execute()
                except Exception as _exc:
                    logger.warning(f'Hata: {_exc}')
                if not is_main_admin:
                    try:
                        log_entry = {'id': str(int(time.time()*1000)), 'admin': current_username, 'action': 'ban_user', 'target': target, 'detail': f"Ban sebebi: {reason}", 'ts': int(time.time())}
                        supabase.table('admin_logs').insert(log_entry).execute()
                        send_push_to_user('Admin', title=f"🚨 Kullanıcı Banlı", body=f"{current_username}, {target} adlı kullanıcıyı banladı. Sebep: {reason[:60]}", url="/")
                    except Exception as _exc:
                        logger.warning(f'Hata: {_exc}')
                return jsonify({'status': 'ok'})

            elif action == 'admin_send_custom_push':
                if not is_main_admin:
                    return jsonify({'status': 'error', 'message': 'Yetkisiz!'})
                
                target_type = data.get('targetType', 'all')
                usernames_str = data.get('usernames', '')
                title = data.get('title', '').strip()
                message = data.get('message', '').strip()
                
                if not title or not message:
                    return jsonify({'status': 'error', 'message': 'Başlık ve mesaj boş olamaz!'})
                
                import requests as _req
                from extensions import ONESIGNAL_APP_ID as _OS_APP_ID, ONESIGNAL_API_KEY as _OS_KEY
                
                if not _OS_KEY or not _OS_APP_ID:
                    return jsonify({'status': 'error', 'message': 'API Key eksik!'})
                
                auth_h = f"Key {_OS_KEY}" if _OS_KEY.startswith('os_v2_') else f"Basic {_OS_KEY}"
                os_payload = {
                    'app_id': _OS_APP_ID,
                    'headings': {'en': title, 'tr': title},
                    'contents': {'en': message, 'tr': message},
                    'web_url': 'https://freeridertr.com.tr/',
                    'app_url': 'https://freeridertr.com.tr/',
                }

                if target_type == 'all':
                    os_payload['included_segments'] = ['All']
                else:
                    target_list = [u.strip() for u in usernames_str.split(',') if u.strip()]
                    if not target_list:
                        return jsonify({'status': 'error', 'message': 'Kullanıcı belirtilmedi!'})
                    os_payload['include_external_user_ids'] = target_list
                    os_payload['channel_for_external_user_ids'] = 'push'

                try:
                    os_r = _req.post(
                        'https://onesignal.com/api/v1/notifications',
                        json=os_payload,
                        headers={'Authorization': auth_h, 'Content-Type': 'application/json'},
                        timeout=12
                    )
                    os_res = os_r.json() if os_r.text else {}
                    
                    if os_r.status_code == 200:
                        recipients = os_res.get('recipients', 0)
                        msg_status = f"Başarılı! {recipients} kişiye iletildi." if recipients > 0 else "İletildi ama alıcı sayısı 0 (Kimse abone değil)."
                        
                        log_msg = f"Özel bildirim gönderdi: {title} ({'Herkese' if target_type == 'all' else usernames_str})"
                        try:
                            supabase.table('admin_logs').insert({
                                'admin_username': current_user,
                                'action_type': 'SEND_PUSH',
                                'target_username': 'ALL' if target_type == 'all' else usernames_str[:40],
                                'details': log_msg
                            }).execute()
                        except: pass
                        
                        return jsonify({'status': 'ok', 'message': msg_status})
                    else:
                        errors = os_res.get('errors', str(os_r.text))
                        return jsonify({'status': 'error', 'message': f'API Hatası: {errors}'})
                except Exception as e:
                    return jsonify({'status': 'error', 'message': f'Bağlantı hatası: {str(e)}'})

            # ================================================================
            # GELİŞMİŞ ADMİN YÖNETİM SİSTEMİ
            # ================================================================
            elif action == 'admin_reset_password':
                if not is_admin:
                    return jsonify({'status': 'error', 'message': 'Yetkisiz!'})
                target = data.get('username', '').strip()
                if not target:
                    return jsonify({'status': 'error', 'message': 'Kullanıcı belirtilmedi!'})
                u_res = supabase.table('users').select('stats').eq('username', target).execute()
                if not u_res.data:
                    return jsonify({'status': 'error', 'message': 'Kullanıcı bulunamadı!'})
                chars = string.ascii_letters + string.digits + '!@#$%'
                new_pass = ''.join(random.choices(chars, k=12))
                hashed = generate_password_hash(new_pass, method='pbkdf2:sha256')
                supabase.table('users').update({'password': hashed}).eq('username', target).execute()
                stats = u_res.data[0].get('stats', {})
                if isinstance(stats, str):
                    try: stats = json.loads(stats)
                    except: stats = {}
                email = stats.get('email', '')
                email_sent = False
                if email and stats.get('email_verified'):
                    email_html = f"<h3>FreeriderTR Şifre Sıfırlama</h3><p>Yönetici tarafından şifreniz sıfırlandı.<br>Yeni şifreniz: <b style='font-size:20px'>{new_pass}</b></p>"
                    email_sent = send_resend_email(email, 'FreeriderTR - Şifreniz Sıfırlandı', email_html)
                try:
                    log_entry = {'id': str(int(time.time()*1000)), 'admin': current_username, 'action': 'reset_password', 'target': target, 'detail': f"Şifre sıfırlandı (email: {'gönderildi' if email_sent else 'yok/gönderilemedi'})", 'ts': int(time.time())}
                    supabase.table('admin_logs').insert(log_entry).execute()
                except Exception:
                    pass
                return jsonify({'status': 'ok', 'new_password': new_pass, 'email_sent': email_sent})

            elif action == 'admin_command':
                if not is_admin:
                    return jsonify({'status': 'error', 'message': 'Yetkisiz!'})
                cmd = data.get('command', '').strip()
                if not cmd:
                    return jsonify({'status': 'error', 'message': 'Komut boş!'})
                tier_map = {
                    'standart': (1, 'std-blue'),
                    'deluxe': (2, 'dlx-blue'),
                    'ultra': (3, 'ult-gold'),
                }
                match_result = None
                cmd_lower = cmd.lower()
                for tier_name in tier_map:
                    pattern_give = rf'^(.+?)\s+{tier_name}\s+g[oö]nder$'
                    pattern_revoke = rf'^(.+?)\s+{tier_name}\s+geri\s*[cç]ek$'
                    m = re.match(pattern_give, cmd_lower)
                    if m:
                        match_result = {'username': m.group(1).strip(), 'tier_name': tier_name, 'act': 'give'}
                        break
                    m = re.match(pattern_revoke, cmd_lower)
                    if m:
                        match_result = {'username': m.group(1).strip(), 'tier_name': tier_name, 'act': 'revoke'}
                        break
                if not match_result:
                    return jsonify({'status': 'error', 'message': 'Geçersiz komut! Örnek: kullanıcıadı standart gönder'})
                target_username = match_result['username']
                u_res = supabase.table('users').select('username, stats').ilike('username', target_username).execute()
                if not u_res.data:
                    return jsonify({'status': 'error', 'message': f'Kullanıcı bulunamadı: {target_username}'})
                actual_username = u_res.data[0]['username']
                stats = u_res.data[0].get('stats', {})
                if isinstance(stats, str):
                    try: stats = json.loads(stats)
                    except: stats = {}
                tier_num, tier_color = tier_map[match_result['tier_name']]
                if match_result['act'] == 'give':
                    stats['premium_tier'] = tier_num
                    stats['premium_color'] = tier_color
                    exp_dt = datetime.datetime.now() + datetime.timedelta(days=30)
                    stats['premium_expire_date'] = exp_dt.strftime('%Y-%m-%d')
                    stats['expiry_ts'] = int(exp_dt.timestamp())
                    stats.pop('gp_admin_revoked', None)  # Yeni üyelik verilince engeli kaldır
                    detail = f"{match_result['tier_name'].capitalize()} üyelik verildi (30 gün)"
                else:
                    stats['premium_tier'] = 0
                    stats['premium_color'] = ''
                    stats.pop('premium_expire_date', None)
                    stats.pop('expiry_ts', None)
                    stats['gp_admin_revoked'] = True  # Admin elle geri çekti — restore engellensin
                    detail = f"{match_result['tier_name'].capitalize()} üyelik geri çekildi"
                supabase.table('users').update({'stats': stats}).eq('username', actual_username).execute()
                _sync_membership_columns(actual_username, stats)
                try:
                    log_entry = {'id': str(int(time.time()*1000)), 'admin': current_username, 'action': 'command', 'target': actual_username, 'detail': detail, 'ts': int(time.time())}
                    supabase.table('admin_logs').insert(log_entry).execute()
                except Exception:
                    pass
                return jsonify({'status': 'ok', 'message': f'{actual_username}: {detail}'})

            elif action == 'admin_change_username':
                if not is_main_admin:
                    return jsonify({'status': 'error', 'message': 'Sadece Ana Admin bu işlemi yapabilir!'})
                old_name = data.get('old_username', '').strip()
                new_name = data.get('new_username', '').strip()
                if not old_name or not new_name:
                    return jsonify({'status': 'error', 'message': 'Eski ve yeni kullanıcı adı gerekli!'})
                if len(new_name) < 3 or len(new_name) > 30:
                    return jsonify({'status': 'error', 'message': 'Yeni ad 3-30 karakter arası olmalı!'})
                if not re.match(r'^[A-Za-z0-9_.\-]+$', new_name):
                    return jsonify({'status': 'error', 'message': 'Geçersiz karakter!'})
                check = supabase.table('users').select('username').ilike('username', new_name).execute()
                if check.data:
                    return jsonify({'status': 'error', 'message': 'Bu kullanıcı adı zaten kullanılıyor!'})
                old_check = supabase.table('users').select('username').eq('username', old_name).execute()
                if not old_check.data:
                    return jsonify({'status': 'error', 'message': 'Kullanıcı bulunamadı!'})
                supabase.table('users').update({'username': new_name}).eq('username', old_name).execute()
                _rename_tables = [('messages','user'),('markers','addedBy'),('events','creator'),('market','owner'),('stories','user'),('reels','user'),('comments','user')]
                for tbl, fld in _rename_tables:
                    try:
                        supabase.table(tbl).update({fld: new_name}).eq(fld, old_name).execute()
                    except Exception:
                        pass
                try:
                    supabase.table('dms').update({'sender': new_name}).eq('sender', old_name).execute()
                    supabase.table('dms').update({'receiver': new_name}).eq('receiver', old_name).execute()
                except Exception:
                    pass
                try:
                    supabase.table('banned_users').update({'username': new_name}).eq('username', old_name).execute()
                except Exception:
                    pass
                try:
                    log_entry = {'id': str(int(time.time()*1000)), 'admin': current_username, 'action': 'change_username', 'target': old_name, 'detail': f'{old_name} -> {new_name}', 'ts': int(time.time())}
                    supabase.table('admin_logs').insert(log_entry).execute()
                except Exception:
                    pass
                app_cache.invalidate('leaderboard_data')
                return jsonify({'status': 'ok', 'message': f'{old_name} -> {new_name}'})

            elif action == 'admin_delete_user':
                if not is_main_admin:
                    return jsonify({'status': 'error', 'message': 'Sadece Ana Admin hesap silebilir!'})
                target = data.get('username', '').strip()
                if not target or target == 'Admin':
                    return jsonify({'status': 'error', 'message': 'Geçersiz kullanıcı!'})
                u_check = supabase.table('users').select('username').eq('username', target).execute()
                if not u_check.data:
                    return jsonify({'status': 'error', 'message': 'Kullanıcı bulunamadı!'})
                try:
                    asset_result = delete_user_assets(target)
                    logger.info(f'Admin hesap silme R2: {target} -> {asset_result}')
                    supabase.table('markers').delete().eq('addedBy', target).execute()
                    supabase.table('events').delete().eq('creator', target).execute()
                    supabase.table('market').delete().eq('owner', target).execute()
                    supabase.table('stories').delete().eq('user', target).execute()
                    supabase.table('comments').delete().eq('user', target).execute()
                    supabase.table('reels').delete().eq('user', target).execute()
                    supabase.table('dms').delete().or_(f'sender.eq.{target},receiver.eq.{target}').execute()
                    supabase.table('messages').delete().eq('user', target).execute()
                    supabase.table('users').delete().eq('username', target).execute()
                    app_cache.invalidate('leaderboard_data')
                    log_entry = {'id': str(int(time.time()*1000)), 'admin': current_username, 'action': 'delete_user', 'target': target, 'detail': 'Hesap tamamen silindi', 'ts': int(time.time())}
                    supabase.table('admin_logs').insert(log_entry).execute()
                except Exception as exc:
                    return jsonify({'status': 'error', 'message': f'Silme hatasi: {str(exc)}'})
                return jsonify({'status': 'ok', 'message': f'{target} hesabi silindi.'})

            elif action == 'admin_unban_user':
                if not is_admin:
                    return jsonify({'status': 'error', 'message': 'Yetkisiz!'})
                target = data.get('username', '').strip()
                if not target:
                    return jsonify({'status': 'error', 'message': 'Kullanıcı belirtilmedi!'})
                supabase.table('banned_users').delete().eq('username', target).execute()
                supabase.table('users').update({'is_banned': False}).eq('username', target).execute()
                app_cache.invalidate(f'ban:{target}')
                try:
                    log_entry = {'id': str(int(time.time()*1000)), 'admin': current_username, 'action': 'unban_user', 'target': target, 'detail': 'Ban kaldirildi', 'ts': int(time.time())}
                    supabase.table('admin_logs').insert(log_entry).execute()
                except Exception:
                    pass
                return jsonify({'status': 'ok', 'message': f'{target} bani kaldirildi.'})

            elif action == 'comment_reel':
                reel_id = str(data.get('reel_id', ''))
                text_r = html.escape(data.get('text', '').strip()[:300])
                if not text_r:
                    return jsonify({'status': 'error', 'message': 'Yorum boş olamaz!'})
                comment_r = {
                    'id': str(int(time.time() * 1000)),
                    'target_id': reel_id,
                    'target_type': 'reel',
                    'user': current_username,
                    'text': text_r,
                    'created_at': datetime.datetime.now().isoformat()
                }
                supabase.table('comments').insert(comment_r).execute()
                # Yorum sayısını artır + reel sahibine bildirim
                try:
                    rc_res = supabase.table('reels').select('comment_count, user').eq('id', reel_id).execute()
                    if rc_res.data:
                        new_cc = (rc_res.data[0].get('comment_count') or 0) + 1
                        supabase.table('reels').update({'comment_count': new_cc}).eq('id', reel_id).execute()
                        # ── Reel sahibine bildirim ──
                        reel_owner_r = rc_res.data[0].get('user', '')
                        if reel_owner_r and reel_owner_r != current_username:
                            send_push_to_user(
                                reel_owner_r,
                                title=f"💬 {current_username} reelini yorumladı!",
                                body=text_r[:80],
                                url="/"
                            )
                except Exception as _exc:
                    logger.warning(f'Hata: {_exc}')
                return jsonify({'status': 'ok'})

            # ================================================================
            # DESTEK TALEP (Öncelikli destek - Premium)
            # ================================================================
            elif action == 'send_support':
                msg = html.escape(data.get('message', '').strip())
                if not msg:
                    return jsonify({'status': 'error', 'message': 'Mesaj bos olamaz!'})
                u_res2 = supabase.table('users').select('stats').eq('username', current_username).execute()
                try:
                    st_val = u_res2.data[0].get('stats', {}) if u_res2.data else {}
                    if isinstance(st_val, str): st_val = json.loads(st_val)
                    prem2 = int(st_val.get('premium_tier', 0))
                except Exception:
                    prem2 = 0
                priority = "🔴 ÖNCELİKLİ" if prem2 >= 2 else ("🟡 Normal" if prem2 == 1 else "⚪ Ücretsiz")
                email_html = f"<h3>FreeriderTR Destek Talebi</h3><p><b>Kullanici:</b> {current_username}<br><b>Oncelik:</b> {priority}<br><b>Mesaj:</b><br>{msg}</p>"
                send_resend_email("destek.freerider@gmail.com", f"[{priority}] Destek - {current_username}", email_html)
                # Admin'e DM olarak gönder (en güvenilir yol)
                try:
                    dm_msg = "[DESTEK] " + priority + " | " + current_username + ": " + msg
                    dm_id = str(int(time.time() * 1000))
                    supabase.table('dms').insert({
                        'id': dm_id,
                        'sender': current_username,
                        'receiver': 'Admin',
                        'participants': [current_username, 'Admin'],
                        'text': dm_msg,
                        'type': 'text'
                    }).execute()
                except Exception as e:
                    print("Destek DM hatası:", e)
                # Push bildirim de gönder
                try:
                    send_push_to_user('Admin', f"🎧 {priority} Destek: {current_username}", msg[:80], url="/")
                except Exception as e:
                    print(f"⚠️ Destek push bildirimi hatası: {e}")
                return jsonify({'status': 'ok'})

            elif action == 'report_user':
                target = html.escape(data.get('target', '').strip())
                reason = html.escape(data.get('reason', 'Belirtilmedi').strip())
                if not target or target == current_username:
                    return jsonify({'status': 'error', 'message': 'Geçersiz kullanıcı.'})
                # Admin'e bildirim + DM
                report_text = f"[KULLANICI ŞİKAYET] {current_username} → {target} | Sebep: {reason}"
                try:
                    dm_id = str(int(time.time() * 1000))
                    supabase.table('dms').insert({
                        'id': dm_id, 'sender': current_username, 'receiver': 'Admin',
                        'participants': [current_username, 'Admin'],
                        'text': report_text, 'type': 'text'
                    }).execute()
                except Exception as e:
                    print(f"⚠️ Şikayet DM hatası: {e}")
                
                # Rapor sayfasına ekle
                try:
                    supabase.table('moderation_reports').insert({
                        'message_id': 'USER_REPORT',
                        'content': report_text,
                        'sender': target,
                        'reporter_ip': current_username,
                        'is_inappropriate': True,
                        'severity': 'medium',
                        'status': 'pending'
                    }).execute()
                except Exception as e:
                    print(f"⚠️ Kullanıcı raporu DB hatası: {e}")
                try:
                    send_push_to_user('Admin', f"🚨 Kullanıcı Şikayeti: {target}", f"{current_username}: {reason[:60]}", url="/")
                except Exception as e:
                    print(f"⚠️ Şikayet push hatası: {e}")
                email_html = f"<h3>Kullanıcı Şikayeti</h3><p><b>Şikayet Eden:</b> {current_username}<br><b>Şikayet Edilen:</b> {target}<br><b>Sebep:</b> {reason}</p>"
                send_resend_email("destek.freerider@gmail.com", f"[ŞİKAYET] {target} - {current_username}", email_html)
                return jsonify({'status': 'ok'})

            elif action == 'report_message':
                msg_id = str(data.get('msg_id', ''))
                msg_text_raw = data.get('msg_text', '')[:2000]
                msg_user = data.get('msg_user', '').strip()
                reason = html.escape(data.get('reason', 'Belirtilmedi').strip())

                if not msg_text_raw:
                    return jsonify({'status': 'error', 'message': 'Mesaj içeriği boş.'})
                if not msg_user:
                    return jsonify({'status': 'error', 'message': 'Gönderen bilgisi eksik.'})
                if msg_user == current_username:
                    return jsonify({'status': 'error', 'message': 'Kendi mesajınızı raporlayamazsınız.'})

                safe_content = html.escape(msg_text_raw)

                # ── Groq AI Detaylı İnceleme (Kullanıcı Raporlarında Ana Karar Mercii) ──
                analysis = analyze_content(msg_text_raw)
                
                groq_inappropriate = False
                groq_reason = ""
                try:
                    groq_system = (
                        "Sen son derece ESNEK, anlayışlı ve hoşgörülü bir içerik moderatörüsün. "
                        "Kullanıcılar oyun/spor uygulamasında günlük dilde konuşabilir, şakalaşabilir, argo kullanabilir. "
                        "SADECE ve SADECE ağır küfürler (örn. amk, siktir, oç), doğrudan şiddet/tehdit, "
                        "nefret söylemi, ırkçılık veya pornografik içerik varsa mesajı uygunsuz işaretle. "
                        "Normal sohbetleri, şikayetleri, ufak sinirlenmeleri, argo kelimeleri (lan, oğlum vb.) KESİNLİKLE uygunsuz işaretleme! "
                        "Emin değilsen veya zararsız görünüyorsa DAİMA 'uygunsuz': false olarak dön. "
                        "SADECE şu JSON formatında cevap ver, başka hiçbir şey yazma: "
                        '{"uygunsuz": true/false, "sebep": "kısa açıklama"}'
                    )
                    groq_reply = _call_groq_ai(groq_system, f"Mesaj: {msg_text_raw[:500]}", json_mode=True)
                    groq_result = json.loads(groq_reply)
                    groq_inappropriate = groq_result.get('uygunsuz', False)
                    groq_reason = groq_result.get('sebep', '')
                except Exception as exc:
                    logger.warning(f"Groq API hatası (report_message): {exc}")
                    groq_inappropriate = analysis.get('is_inappropriate', False)
                    groq_reason = "Sistem filtresi"

                # Groq sonucuna göre analysis nesnesini güncelle ki veritabanına doğru gitsin
                if groq_inappropriate:
                    analysis['is_inappropriate'] = True
                    analysis['severity'] = 'high'
                    if groq_reason:
                        analysis['matched_patterns'] = [groq_reason]
                else:
                    analysis['is_inappropriate'] = False
                    analysis['severity'] = 'none'

                should_notify = analysis['is_inappropriate']
                warning = False
                system_message = ''
                ai_chat_msg = None

                # Her halukarda raporu admin paneli icin veritabanina kaydet
                saved = _save_report(
                    supabase_client=supabase,
                    log=logger,
                    message_id=msg_id,
                    content=safe_content,
                    sender=msg_user,
                    reporter_ip=current_username,
                    analysis=analysis,
                )

                if not should_notify:
                    # AI ciddi ihlal bulmadi -> Blur yapma (is_flagged=False), anlik ban/mail atma
                    return jsonify({'status': 'ok', 'message': 'Raporunuz iletildi. AI anlık bir ihlal bulmadı ancak admin inceleyecek.'})

                # AI ihlal buldu -> mesaji blurla (is_flagged=True) ve admin bildirimlerini gonder

                updated_flag_count = 0
                should_remove = False
                try:
                    msg_flag_res = supabase.table('messages').select('flag_count').eq('id', msg_id).execute()
                    if msg_flag_res.data:
                        updated_flag_count = (msg_flag_res.data[0].get('flag_count') or 0) + 1
                    else:
                        updated_flag_count = 1

                    if updated_flag_count >= 2:
                        should_remove = True
                        supabase.table('messages').delete().eq('id', msg_id).execute()
                        logger.info(f"Mesaj otomatik silindi (flag_count={updated_flag_count}): {msg_id}")
                    else:
                        supabase.table('messages').update({
                            'is_flagged': True,
                            'flag_count': updated_flag_count
                        }).eq('id', msg_id).execute()
                except Exception as exc:
                    logger.warning(f"Mesaj flag güncellenemedi: {exc}")

                # ── Admin'e DM (Her Zaman Gönderilir) ──
                severity_emoji = {'high': '🔴', 'medium': '🟠', 'low': '🟡', 'none': '⚪'}
                sev_icon = severity_emoji.get(analysis['severity'], '⚪')
                report_text = (
                    f"[🛡️ ŞİKAYET EDİLEN MESAJ]\n"
                    f"Bildiren: {current_username}\n"
                    f"Şüpheli: {msg_user}\n"
                    f"AI Seviyesi: {sev_icon} {analysis['severity'].upper()}\n"
                    f"Kullanıcı Sebebi: {reason}\n"
                    f"İçerik: {msg_text_raw[:200]}"
                )
                try:
                    dm_id = str(int(time.time() * 1000))
                    supabase.table('dms').insert({
                        'id': dm_id, 'sender': current_username, 'receiver': 'Admin',
                        'participants': [current_username, 'Admin'],
                        'text': report_text, 'type': 'text'
                    }).execute()
                except Exception as e:
                    print(f"⚠️ Mesaj şikayet DM hatası: {e}")

                # ── Admin'e push ve e-posta (Sadece AI uygunsuz bulduysa) ──
                if should_notify:
                    try:
                        send_push_to_user(
                            'Admin',
                            f"{sev_icon} Moderasyon: {msg_user} bildirildi!",
                            f"{current_username}: {reason[:60]} | İçerik: {msg_text_raw[:40]}...",
                            url="/"
                        )
                    except Exception as e:
                        print(f"⚠️ Mesaj şikayet push hatası: {e}")

                    # ── E-posta bildirim ───────────────────────────────────
                    try:
                        email_html = (
                            f"<h3>Mesaj Şikayeti</h3>"
                            f"<p><b>Şikayet Eden:</b> {current_username}<br>"
                            f"<b>Mesaj Sahibi:</b> {html.escape(msg_user)}<br>"
                            f"<b>Seviye:</b> {analysis['severity'].upper()} (Güven: %{int(analysis['confidence']*100)})<br>"
                            f"<b>Mesaj:</b> {safe_content[:300]}<br>"
                            f"<b>Sebep:</b> {reason}</p>"
                        )
                        send_resend_email("destek.freerider@gmail.com", f"[MESAJ ŞİKAYET] {msg_user} - {current_username}", email_html)
                    except Exception as e:
                        print(f"⚠️ Mesaj şikayet e-posta hatası: {e}")
                else:
                    logger.info(
                        f"report_message: AI temiz buldu, bildirim atlandı "
                        f"(reporter={current_username}, sender={msg_user})"
                    )

                # ── Uygunsuz içerik tespit edildiyse ──────────────────
                if analysis['is_inappropriate']:
                    warning = True

                    if analysis['severity'] == 'high':
                        system_message = (
                            '⚠️ ADMİNE BİLDİRİLDİNİZ! '
                            'Uygunsuz içerik nedeniyle hesabınız incelemeye alındı.'
                        )
                    else:
                        system_message = (
                            '⚠️ Mesajınız moderasyon ekibine bildirildi. '
                            'Topluluk kurallarına uymayan paylaşımlar hesap askıya alınmasına neden olabilir.'
                        )

                    # AI Moderatör olarak chat'e uyarı mesajı ekle
                    ai_warning_text = (
                        f"🛡️ {msg_user}, mesajın topluluk kurallarına aykırı bulundu ve admin ekibine bildirildi. "
                        f"Lütfen kurallara uygun davranın. Tekrarlayan ihlaller hesabınızın askıya alınmasına neden olabilir."
                    )
                    try:
                        ai_msg_id = str(int(time.time() * 1000)) + '_mod'
                        supabase.table('messages').insert({
                            'id': ai_msg_id,
                            'user': 'Freerider AI',
                            'text': ai_warning_text,
                            'type': 'text',
                        }).execute()
                        ai_chat_msg = {
                            'id': ai_msg_id,
                            'user': 'Freerider AI',
                            'text': ai_warning_text,
                            'type': 'text',
                        }
                    except Exception as exc:
                        logger.warning(f"AI moderatör chat mesajı eklenemedi: {exc}")

                    # Kullanıcı istatistiklerine uyarı sayacı ekle
                    try:
                        u_warn_res = supabase.table('users').select('stats').eq('username', msg_user).limit(1).execute()
                        if u_warn_res.data:
                            st = u_warn_res.data[0].get('stats') or {}
                            if isinstance(st, str):
                                try: st = json.loads(st)
                                except Exception: st = {}
                            st['mod_warning_count'] = st.get('mod_warning_count', 0) + 1
                            st['last_mod_warning_ts'] = int(time.time())
                            supabase.table('users').update({'stats': st}).eq('username', msg_user).execute()
                    except Exception as exc:
                        logger.warning(f"Uyarı sayacı güncellenemedi: {exc}")

                return jsonify({
                    'status': 'ok',
                    'is_inappropriate': analysis['is_inappropriate'],
                    'is_flagged': True,
                    'warning': warning,
                    'system_message': system_message,
                    'severity': analysis['severity'],
                    'confidence': analysis['confidence'],
                    'saved': saved,
                    'ai_chat_msg': ai_chat_msg,
                    'flag_count': updated_flag_count,
                    'should_remove': should_remove,
                })

            elif action == 'delete_account':
                if current_username.lower() == 'admin':
                    return jsonify({'status': 'error', 'message': 'Admin hesabı silinemez.'})
                # Google Play zorunluluğu: Hesap + tüm veriler + R2 medyaları silinir
                confirm_pass = data.get('password', '').strip()
                u_res = supabase.table('users').select('password').eq('username', current_username).execute()
                if not u_res.data:
                    return jsonify({'status': 'error', 'message': 'Kullanıcı bulunamadı.'})
                if not check_password_hash(u_res.data[0].get('password', ''), confirm_pass):
                    return jsonify({'status': 'error', 'message': 'Şifre yanlış! Hesabınızı silmek için doğru şifrenizi girin.'})
                try:
                    # 1. R2 medya varlıklarını temizle
                    asset_result = delete_user_assets(current_username)
                    logger.info(f"Hesap silme R2 temizliği: {current_username} → {asset_result}")
                    # 2. Supabase verilerini sil
                    supabase.table('markers').delete().eq('addedBy', current_username).execute()
                    supabase.table('events').delete().eq('creator', current_username).execute()
                    supabase.table('market').delete().eq('owner', current_username).execute()
                    supabase.table('stories').delete().eq('user', current_username).execute()
                    supabase.table('comments').delete().eq('user', current_username).execute()
                    supabase.table('reels').delete().eq('user', current_username).execute()
                    supabase.table('dms').delete().or_(f'sender.eq.{current_username},receiver.eq.{current_username}').execute()
                    supabase.table('messages').delete().eq('user', current_username).execute()
                    supabase.table('users').delete().eq('username', current_username).execute()
                    # 3. Liderlik önbelleğini geçersiz kıl
                    app_cache.invalidate('leaderboard_data')
                    session.clear()
                    return jsonify({'status': 'ok', 'message': 'Hesabınız ve tüm verileriniz kalıcı olarak silindi.'})
                except Exception as exc:
                    logger.error(f"Hesap silme hatası ({current_username}): {exc}", exc_info=True)
                    return jsonify({'status': 'error', 'message': f'Silme işlemi sırasında hata oluştu: {str(exc)}'})

            elif action == 'block_user':
                target = html.escape(data.get('target', '').strip())
                if not target or target == current_username:
                    return jsonify({'status': 'error', 'message': 'Geçersiz kullanıcı.'})
                u_res = supabase.table('users').select('stats').eq('username', current_username).execute()
                if not u_res.data:
                    return jsonify({'status': 'error', 'message': 'Kullanıcı bulunamadı.'})
                stats = u_res.data[0].get('stats', {}) or {}
                if isinstance(stats, str):
                    try: stats = json.loads(stats)
                    except: stats = {}
                blocked = stats.get('blocked_users', [])
                if target not in blocked:
                    blocked.append(target)
                stats['blocked_users'] = blocked
                supabase.table('users').update({'stats': stats}).eq('username', current_username).execute()
                return jsonify({'status': 'ok', 'message': f'{target} engellendi.'})

            elif action == 'unblock_user':
                target = html.escape(data.get('target', '').strip())
                u_res = supabase.table('users').select('stats').eq('username', current_username).execute()
                if not u_res.data:
                    return jsonify({'status': 'error', 'message': 'Kullanıcı bulunamadı.'})
                stats = u_res.data[0].get('stats', {}) or {}
                if isinstance(stats, str):
                    try: stats = json.loads(stats)
                    except: stats = {}
                blocked = stats.get('blocked_users', [])
                if target in blocked:
                    blocked.remove(target)
                stats['blocked_users'] = blocked
                supabase.table('users').update({'stats': stats}).eq('username', current_username).execute()
                return jsonify({'status': 'ok', 'message': f'{target} engeli kaldırıldı.'})

            elif action == 'get_competitions':
                # week_id her zaman sunucu tarafında hesaplanir - format uyumsuzlugunu engeller
                from datetime import date, timedelta
                today = date.today()
                week_id = today.strftime('%Y-W%W')
                try:
                    cat = data.get('category', None)
                    query = supabase.table('bike_competitions').select('*')
                    if cat and cat != 'Tümü':
                        query = query.eq('category', cat)
                    res = query.order('avg_rating', desc=True).limit(100).execute()
                    logger.info(f'get_competitions: week_id={week_id}, found {len(res.data or [])} entries')
                    # Geçen haftanın kazananlarını getir ve gerekirse otomatik sonlandır
                    prev_monday = today - timedelta(days=today.weekday() + 7)
                    prev_week_id = prev_monday.strftime('%Y-W%W')
                    _auto_finalize_competition(prev_week_id)
                    
                    winners_res = supabase.table('bike_competitions').select('*').eq('week_id', prev_week_id).lt('final_rank', 4).gt('final_rank', 0).order('final_rank').limit(30).execute()
                    return jsonify({'status': 'ok', 'entries': res.data or [], 'prev_winners': winners_res.data or [], 'week_id': week_id})
                except Exception as e:
                    logger.error(f'get_competitions error: {e}')
                    return jsonify({'status': 'error', 'message': 'Yarışma verisi alınamadı.'})

            elif action == 'submit_bike':
                bike_index = data.get('bike_index')
                category = html.escape(data.get('category', '').strip())
                if bike_index is None or not category:
                    return jsonify({'status': 'error', 'message': 'Bisiklet ve kategori gereklidir.'})
                # Get user's garage
                u_res = supabase.table('users').select('stats').eq('username', current_username).execute()
                if not u_res.data:
                    return jsonify({'status': 'error', 'message': 'Kullanıcı bulunamadı.'})
                stats = u_res.data[0].get('stats', {}) or {}
                if isinstance(stats, str):
                    try: stats = json.loads(stats)
                    except: stats = {}
                garage = stats.get('garage', [])
                if not garage or bike_index >= len(garage):
                    return jsonify({'status': 'error', 'message': 'Bisiklet bulunamadı.'})
                bike = garage[bike_index]
                from datetime import date
                today = date.today()
                week_id = today.strftime('%Y-W%W')
                # Check if already submitted this week
                check = supabase.table('bike_competitions').select('id, category, bike_data').eq('username', current_username).eq('week_id', week_id).execute()
                if check.data:
                    for c_entry in check.data:
                        if c_entry.get('category') == category:
                            return jsonify({'status': 'error', 'message': 'Bu hafta bu kategoriye zaten bir bisiklet eklediniz.'})
                        c_bike = c_entry.get('bike_data', {})
                        if c_bike.get('original_index') == bike_index:
                            return jsonify({'status': 'error', 'message': 'Bu bisikleti bu hafta zaten bir yarışmaya eklediniz!'})
                
                import json as _json
                bike_data_to_store = bike if isinstance(bike, dict) else _json.loads(_json.dumps(bike))
                bike_data_to_store['original_index'] = bike_index
                
                entry = {
                    'id': str(uuid.uuid4()),
                    'username': current_username,
                    'week_id': week_id,
                    'category': category,
                    'bike_data': bike_data_to_store,
                    'user_ratings': [],
                    'avg_rating': 0,
                    'final_rank': 0
                }
                try:
                    ins_res = supabase.table('bike_competitions').insert(entry).execute()
                    logger.info(f'submit_bike insert result: {ins_res.data}')
                except Exception as ins_err:
                    logger.error(f'submit_bike INSERT HATASI: {ins_err}')
                    return jsonify({'status': 'error', 'message': f'Veritabanı hatası: {str(ins_err)}'})
                return jsonify({'status': 'ok', 'message': 'Bisikletiniz yarışmaya eklendi!'})

            elif action == 'rate_bike':
                entry_id = data.get('entry_id', '').strip()
                score = data.get('score')
                if not entry_id or score is None:
                    return jsonify({'status': 'error', 'message': 'Eksik veri.'})
                try:
                    score = float(score)
                    if score < 1 or score > 10:
                        return jsonify({'status': 'error', 'message': 'Puan 1-10 arasında olmalıdır.'})
                except:
                    return jsonify({'status': 'error', 'message': 'Geçersiz puan.'})
                # Get current entry
                entry_res = supabase.table('bike_competitions').select('user_ratings, avg_rating, username').eq('id', entry_id).execute()
                if not entry_res.data:
                    return jsonify({'status': 'error', 'message': 'Kayıt bulunamadı.'})
                entry = entry_res.data[0]
                if entry['username'] == current_username:
                    return jsonify({'status': 'error', 'message': 'Kendi bisikletinizi puanlayamazsınız.'})
                ratings = entry.get('user_ratings', []) or []
                # Remove existing rating by this user
                ratings = [r for r in ratings if r.get('user') != current_username]
                ratings.append({'user': current_username, 'score': score})
                avg = round(sum(r['score'] for r in ratings) / len(ratings), 1)
                supabase.table('bike_competitions').update({'user_ratings': ratings, 'avg_rating': avg}).eq('id', entry_id).execute()
                return jsonify({'status': 'ok', 'avg_rating': avg})

            elif action == 'admin_set_winner':
                if not is_admin and current_user_role not in ['Admin', 'SubAdmin']:
                    return jsonify({'status': 'error', 'message': 'Yetkisiz işlem.'})
                entry_id = data.get('entry_id', '').strip()
                rank = data.get('rank')
                if not entry_id or rank is None:
                    return jsonify({'status': 'error', 'message': 'Eksik veri.'})
                try:
                    rank = int(rank)
                    if rank not in [1, 2, 3]:
                        return jsonify({'status': 'error', 'message': 'Sıralama 1, 2 veya 3 olmalıdır.'})
                except:
                    return jsonify({'status': 'error', 'message': 'Geçersiz sıralama.'})
                # Get entry
                entry_res = supabase.table('bike_competitions').select('*').eq('id', entry_id).execute()
                if not entry_res.data:
                    return jsonify({'status': 'error', 'message': 'Kayıt bulunamadı.'})
                entry = entry_res.data[0]
                winner_username = entry['username']
                category = entry['category']
                week_id = entry['week_id']
                # Set rank
                supabase.table('bike_competitions').update({'final_rank': rank}).eq('id', entry_id).execute()
                # Award badge to user
                if rank in [1, 2, 3]:
                    rank_labels = {1: '1.si 🥇', 2: '2.si 🥈', 3: '3.sü 🥉'}
                    from datetime import date
                    now = date.today()
                    month_names = ['Ocak','Şubat','Mart','Nisan','Mayıs','Haziran','Temmuz','Ağustos','Eylül','Ekim','Kasım','Aralık']
                    month_name = month_names[now.month - 1]
                    badge_text = f'{month_name} {now.year} {category} Yarışması {rank_labels[rank]}'
                    winner_res = supabase.table('users').select('stats').eq('username', winner_username).execute()
                    if winner_res.data:
                        w_stats = winner_res.data[0].get('stats', {}) or {}
                        if isinstance(w_stats, str):
                            try: w_stats = json.loads(w_stats)
                            except: w_stats = {}
                        earned = w_stats.get('earned_badges', [])
                        if badge_text not in earned:
                            earned.append(badge_text)
                        w_stats['earned_badges'] = earned
                        # Also update xp as reward
                        xp_reward = {1: 3000, 2: 2000, 3: 1000}[rank]
                        current_xp_res = supabase.table('users').select('xp').eq('username', winner_username).execute()
                        current_xp = current_xp_res.data[0].get('xp', 0) if current_xp_res.data else 0
                        supabase.table('users').update({'stats': w_stats, 'xp': current_xp + xp_reward}).eq('username', winner_username).execute()
                return jsonify({'status': 'ok', 'message': f'{winner_username} {rank}. olarak belirlendi ve rozet verildi!'})

            elif action == 'remove_from_competition':
                entry_id = data.get('entry_id', '').strip()
                if not entry_id:
                    return jsonify({'status': 'error', 'message': 'Eksik veri.'})
                # Check permissions
                entry_res = supabase.table('bike_competitions').select('username').eq('id', entry_id).execute()
                if not entry_res.data:
                    return jsonify({'status': 'error', 'message': 'Kayıt bulunamadı.'})
                owner = entry_res.data[0]['username']
                is_admin_user = is_admin or current_user_role in ['Admin', 'SubAdmin']
                if not is_admin_user and owner != current_username:
                    return jsonify({'status': 'error', 'message': 'Bu işlem için yetkiniz yok.'})
                
                supabase.table('bike_competitions').delete().eq('id', entry_id).execute()
                return jsonify({'status': 'ok', 'message': 'Bisiklet yarışmadan çıkarıldı.'})

            elif action == 'admin_force_end_leaderboard':
                # Admin erken tablo sonlandırma — haftalık veya aylık
                if not is_admin:
                    return jsonify({'status': 'error', 'message': 'Yetkisiz işlem.'})
                period = data.get('period', '')  # 'weekly' veya 'monthly'
                if period not in ('weekly', 'monthly'):
                    return jsonify({'status': 'error', 'message': 'Geçersiz dönem. weekly veya monthly olmalı.'})

                try:
                    # Tüm kullanıcıları çek
                    all_res = supabase.table('users').select('username, xp, stats').limit(5000).execute()
                    all_users_raw = all_res.data or []

                    # Sırala
                    scored = []
                    for u in all_users_raw:
                        uname = u.get('username', '')
                        if uname.lower() == 'admin':
                            continue
                        st = u.get('stats') or {}
                        if isinstance(st, str):
                            try: st = json.loads(st)
                            except: st = {}
                        score = int(st.get('weekly_xp', 0) if period == 'weekly' else st.get('monthly_xp', 0))
                        if score > 0:
                            scored.append({'username': uname, 'score': score, 'stats': st, 'xp': u.get('xp', 0)})

                    scored.sort(key=lambda x: x['score'], reverse=True)

                    # Ödül tanımları
                    # Haftalık: 1. = 7 gün Ultra+, 2-3. = 7 gün Deluxe
                    # Aylık:    1. = 30 gün Deluxe, 2-3. = 30 gün Deluxe
                    reward_map = {
                        'weekly':  {1: (3, 7),  2: (2, 7),  3: (2, 7)},   # (tier, days)
                        'monthly': {1: (2, 30), 2: (2, 30), 3: (2, 30)},
                    }
                    period_label = 'Haftalık' if period == 'weekly' else 'Aylık'
                    rewarded = []

                    for rank_idx, winner in enumerate(scored[:3], start=1):
                        uname = winner['username']
                        w_stats = winner['stats']
                        tier, days = reward_map[period][rank_idx]
                        color_map = {1: 'std-blue', 2: 'dlx-blue', 3: 'ult-gold'}

                        # Mevcut premium'dan daha iyi ise ver, yoksa ekle
                        current_tier = int(w_stats.get('premium_tier', 0))
                        exp_dt = datetime.datetime.now() + datetime.timedelta(days=days)

                        # Eğer mevcut premium süresi varsa, üstüne ekle
                        if current_tier > 0 and w_stats.get('premium_expire_date'):
                            try:
                                existing_exp = datetime.datetime.strptime(w_stats['premium_expire_date'], "%Y-%m-%d")
                                if existing_exp > datetime.datetime.now():
                                    exp_dt = existing_exp + datetime.timedelta(days=days)
                            except Exception:
                                pass

                        w_stats['premium_tier'] = max(tier, current_tier)
                        w_stats['premium_color'] = color_map.get(max(tier, current_tier), 'dlx-blue')
                        w_stats['premium_expire_date'] = exp_dt.strftime("%Y-%m-%d")
                        w_stats['expiry_ts'] = int(exp_dt.timestamp())

                        # Rozet ekle
                        now_dt = datetime.datetime.now()
                        month_names = ['Ocak','Şubat','Mart','Nisan','Mayıs','Haziran','Temmuz','Ağustos','Eylül','Ekim','Kasım','Aralık']
                        month_name = month_names[now_dt.month - 1]
                        rank_labels = {1: 'Birincisi 🥇', 2: 'İkincisi 🥈', 3: 'Üçüncüsü 🥉'}
                        badge_text = f'{month_name} {now_dt.year} {period_label} Sıralama {rank_labels[rank_idx]}'
                        earned = w_stats.get('earned_badges', [])
                        if badge_text not in earned:
                            earned.append(badge_text)
                        w_stats['earned_badges'] = earned

                        supabase.table('users').update({'stats': w_stats}).eq('username', uname).execute()
                        _sync_membership_columns(uname, w_stats)

                        # Bildirim gönder
                        try:
                            prize_label = f'{days} Gün Ultra+' if tier == 3 else f'{days} Gün Deluxe'
                            send_push_to_user(uname, f'🏆 {period_label} Sıralama Ödülün!',
                                f'{rank_idx}. oldun ve {prize_label} kazandın! Tebrikler!')
                        except Exception:
                            pass

                        rewarded.append({'rank': rank_idx, 'username': uname, 'score': winner['score']})

                    # Tüm kullanıcıların haftalık/aylık XP'sini sıfırla
                    now_dt2 = datetime.datetime.now()
                    # Sonraki periyot anahtarını oluştur (mevcut periyot bitince bir sonrakine geçiş)
                    if period == 'weekly':
                        # Bir sonraki pazartesi haftasına geç
                        next_monday = now_dt2 + datetime.timedelta(days=(7 - now_dt2.weekday()))
                        new_week_key = next_monday.strftime("%Y-%m-%d")
                    else:
                        # Bir sonraki aya geç
                        if now_dt2.month == 12:
                            next_month = now_dt2.replace(year=now_dt2.year+1, month=1, day=1)
                        else:
                            next_month = now_dt2.replace(month=now_dt2.month+1, day=1)
                        new_month_key = next_month.strftime("%Y-%m")

                    reset_count = 0
                    for u in all_users_raw:
                        uname = u.get('username', '')
                        if uname.lower() == 'admin':
                            continue
                        st = u.get('stats') or {}
                        if isinstance(st, str):
                            try: st = json.loads(st)
                            except: st = {}
                        changed = False
                        if period == 'weekly':
                            st['weekly_xp'] = 0
                            st['current_week'] = new_week_key
                            changed = True
                        else:
                            st['monthly_xp'] = 0
                            st['current_month'] = new_month_key
                            changed = True
                        if changed:
                            try:
                                supabase.table('users').update({'stats': st}).eq('username', uname).execute()
                                _sync_score_columns(uname, st)
                                reset_count += 1
                            except Exception:
                                pass

                    # Cache'i temizle
                    app_cache.invalidate('leaderboard_data')

                    # Admin logu
                    try:
                        supabase.table('admin_logs').insert({
                            'id': str(int(time.time()*1000)),
                            'admin': current_username,
                            'action': f'admin_force_end_{period}',
                            'target': '',
                            'detail': f'{period_label} sıralama erken sonlandırıldı. Ödüllenenler: {[r["username"] for r in rewarded]}. Sıfırlanan: {reset_count} kullanıcı.',
                            'ts': int(time.time())
                        }).execute()
                    except Exception:
                        pass

                    return jsonify({
                        'status': 'ok',
                        'message': f'{period_label} sıralama sonlandırıldı! {len(rewarded)} kişiye ödül verildi, {reset_count} kullanıcı sıfırlandı.',
                        'rewarded': rewarded
                    })

                except Exception as e:
                    logger.error(f'admin_force_end_leaderboard error: {e}', exc_info=True)
                    return jsonify({'status': 'error', 'message': f'Hata: {str(e)}'})

            return jsonify({'status': 'ok'})
            
        except Exception as e:
            logger.error(f"api_data beklenmedik hata: {e}", exc_info=True)
            return jsonify({'status': 'error', 'message': f'Sunucuda bir hata oluştu. Lütfen tekrar deneyin. Detay: {str(e)}'})
