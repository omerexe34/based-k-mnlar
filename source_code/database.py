"""
database.py
===========
Supabase veritabanı yardımcı fonksiyonları:
  - send_resend_email  : E-posta gönderimi (Resend API)
  - delete_user_assets : Kullanıcıya ait R2 varlıklarını temizler
  - init_db            : Uygulama başlangıcında DB yapısını doğrular
"""

import json
import logging
import requests

from extensions import (
    supabase, r2_client, logger,
    RESEND_API_KEY, R2_PUBLIC_URL, R2_BUCKET_NAME,
)

# ==============================================================================
# RESEND API ENTEGRASYONU (ŞİFRE SIFIRLAMA VE DOĞRULAMA)
# ==============================================================================
def send_resend_email(to_email, subject, html_content):
    if not RESEND_API_KEY:
        print("⚠️ Email gönderilemedi: RESEND_API_KEY environment variable eksik.")
        return False
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "from":"FreeriderTR <iletisim@freeridertr.com.tr>",
        "to": [to_email],
        "subject": subject,
        "html": html_content
    }
    try:
        resp = requests.post("https://api.resend.com/emails", json=data, headers=headers, timeout=10)
        if resp.status_code not in (200, 201, 202):
            print(f"⚠️ Email gönderilemedi ({resp.status_code}): {resp.text[:200]}")
            return False
        return True
    except Exception as e:
        print("Email gönderme hatası:", e)
        return False

# ==============================================================================
# R2 VARLIK TEMİZLEME — Google Play hesap silme zorunluluğu
# ==============================================================================
def delete_user_assets(username: str) -> dict:
    """Kullanıcıya ait R2 üzerindeki tüm medya dosyalarını siler.
    Supabase'deki URL'leri tarayarak gerçek key'leri çıkarır, toplu silme yapar.
    Dönen dict: {'deleted': int, 'failed': int, 'skipped': int}"""
    result = {'deleted': 0, 'failed': 0, 'skipped': 0}
    if not r2_client or not supabase:
        logger.warning(f"delete_user_assets: R2 veya Supabase eksik, {username} varlıkları atlandı.")
        result['skipped'] = -1
        return result

    cdn_base = (R2_PUBLIC_URL or "").rstrip("/")
    r2_keys: list = []

    def _extract_keys_from_url_fields(rows: list, *fields):
        """Verilen satır listesinden URL alanlarını tarar, R2 key'i çıkarır."""
        for row in rows:
            for field in fields:
                val = row.get(field)
                if not val:
                    continue
                urls = val if isinstance(val, list) else [val]
                for url in urls:
                    if isinstance(url, str) and cdn_base and url.startswith(cdn_base):
                        key = url[len(cdn_base):].lstrip("/")
                        if key:
                            r2_keys.append(key)

    # Profil avatarı
    try:
        u_res = supabase.table('users').select('avatar').eq('username', username).execute()
        _extract_keys_from_url_fields(u_res.data or [], 'avatar')
    except Exception as exc:
        logger.warning(f"delete_user_assets: avatar sorgu hatası: {exc}")

    # Reel medyaları
    try:
        reels_res = supabase.table('reels').select('media_url').eq('user', username).execute()
        _extract_keys_from_url_fields(reels_res.data or [], 'media_url')
    except Exception as exc:
        logger.warning(f"delete_user_assets: reels sorgu hatası: {exc}")

    # Mesaj fotoğrafları / sesleri
    try:
        msgs_res = supabase.table('messages').select('photo, voice').eq('user', username).execute()
        _extract_keys_from_url_fields(msgs_res.data or [], 'photo', 'voice')
    except Exception as exc:
        logger.warning(f"delete_user_assets: messages sorgu hatası: {exc}")

    # Harita marker fotoğrafları
    try:
        mk_res = supabase.table('markers').select('photos').eq('addedBy', username).execute()
        _extract_keys_from_url_fields(mk_res.data or [], 'photos')
    except Exception as exc:
        logger.warning(f"delete_user_assets: markers sorgu hatası: {exc}")

    # Market ilanı fotoğrafları
    try:
        mkt_res = supabase.table('market').select('photos').eq('owner', username).execute()
        _extract_keys_from_url_fields(mkt_res.data or [], 'photos')
    except Exception as exc:
        logger.warning(f"delete_user_assets: market sorgu hatası: {exc}")

    # Stats içindeki garage bisiklet fotoğrafları
    try:
        st_res = supabase.table('users').select('stats').eq('username', username).execute()
        if st_res.data:
            st = st_res.data[0].get('stats') or {}
            if isinstance(st, str):
                try: st = json.loads(st)
                except json.JSONDecodeError: st = {}
            garage = st.get('garage', [])
            for bike in (garage if isinstance(garage, list) else []):
                _extract_keys_from_url_fields([bike], 'photos', 'cover')
    except Exception as exc:
        logger.warning(f"delete_user_assets: stats/garage sorgu hatası: {exc}")

    if not r2_keys:
        logger.info(f"delete_user_assets: {username} için silinecek R2 varlığı bulunamadı.")
        return result

    # R2 delete_objects: maks 1000 key/istek
    unique_keys = list(dict.fromkeys(r2_keys))  # sıra koruyarak deduplicate
    for i in range(0, len(unique_keys), 1000):
        batch = unique_keys[i:i + 1000]
        objects = [{"Key": k} for k in batch]
        try:
            resp = r2_client.delete_objects(
                Bucket=R2_BUCKET_NAME,
                Delete={"Objects": objects, "Quiet": True}
            )
            errors = resp.get("Errors", [])
            deleted = len(batch) - len(errors)
            result['deleted'] += deleted
            result['failed']  += len(errors)
            if errors:
                for err in errors:
                    logger.warning(f"R2 silme hatası: key={err.get('Key')} msg={err.get('Message')}")
        except Exception as exc:
            logger.error(f"delete_user_assets: batch silme hatası: {exc}", exc_info=True)
            result['failed'] += len(batch)

    logger.info(f"delete_user_assets: {username} → silindi={result['deleted']}, hata={result['failed']}")
    return result

# ==============================================================================
# VERİTABANI BAŞLATMA
# ==============================================================================
def init_db():
    """Uygulama başlangıcında zorunlu settings kayıtlarını ve admin_logs tablosunu kontrol eder.
    Kritik tablo yoksa ya oluşturmayı dener ya da EnvironmentError fırlatır."""
    if not supabase:
        logger.error("init_db: Supabase bağlantısı yok, başlatma atlandı.")
        return

    # ── settings tablosu varsayılan kayıtları ──────────────────────────────────
    _defaults = {
        'maintenance':      'false',
        'pinned_message':   '{}',
    }
    for key, default_val in _defaults.items():
        try:
            chk = supabase.table('settings').select('id').eq('id', key).execute()
            if not chk.data:
                supabase.table('settings').insert({"id": key, "value": default_val}).execute()
                logger.info(f"init_db: settings[{key}] varsayılan değerle oluşturuldu.")
        except Exception as exc:
            logger.error(f"init_db: settings[{key}] kontrolü başarısız: {exc}", exc_info=True)
            raise EnvironmentError(f"init_db kritik hata — settings tablosu erişilemiyor: {exc}") from exc

    # ── total_users_count ──────────────────────────────────────────────────────
    try:
        uc_check = supabase.table('settings').select('id').eq('id', 'total_users_count').execute()
        if not uc_check.data:
            try:
                real_count = len(supabase.table('users').select('username').execute().data or [])
            except Exception as _exc:
                real_count = 0
            base_count = max(300, 300 + real_count)
            supabase.table('settings').insert({"id": "total_users_count", "value": str(base_count)}).execute()
            logger.info(f"init_db: total_users_count başlatıldı → {base_count}")
    except EnvironmentError:
        raise
    except Exception as exc:
        logger.error(f"init_db: total_users_count hatası: {exc}", exc_info=True)

    # ── admin_logs tablosu ─────────────────────────────────────────────────────
    try:
        supabase.table('admin_logs').select('id').limit(1).execute()
    except Exception as exc:
        _ddl = (
            "CREATE TABLE IF NOT EXISTS admin_logs ("
            "  id text PRIMARY KEY,"
            "  admin text,"
            "  action text,"
            "  target text,"
            "  detail text,"
            "  ts bigint"
            ");"
        )
        logger.critical(
            f"init_db: 'admin_logs' tablosuna erişilemiyor. "
            f"Supabase SQL Editöründe şu DDL'yi çalıştırın:\n{_ddl}\nHata: {exc}"
        )
        raise EnvironmentError(
            "init_db kritik hata — 'admin_logs' tablosu eksik. "
            "Supabase SQL Editöründe tabloyu oluşturun ve uygulamayı yeniden başlatın."
        ) from exc

    # ── messages tablosu flag sütun doğrulaması ──────────────────────────────────
    # is_flagged ve flag_count sütunları yoksa moderasyon sistemi çalışmaz.
    # Migration SQL'i (migration_add_flag_columns.sql) çalıştırılmalıdır.
    try:
        flag_check = (
            supabase.table('messages')
            .select('is_flagged, flag_count')
            .limit(1)
            .execute()
        )
        logger.info("init_db: messages.is_flagged + flag_count sütunları doğrulandı ✅")
    except Exception as exc:
        logger.critical(
            "init_db: ❌ messages tablosunda 'is_flagged' veya 'flag_count' sütunu BULUNAMADI! "
            "Bu sütunlar olmadan moderasyon sistemi çalışmaz. "
            "Supabase SQL Editor'de şu SQL'i çalıştırın:\n"
            "  ALTER TABLE messages ADD COLUMN IF NOT EXISTS is_flagged boolean DEFAULT false;\n"
            "  ALTER TABLE messages ADD COLUMN IF NOT EXISTS flag_count integer DEFAULT 0;\n"
            f"Hata detayı: {exc}"
        )

    # ── moderation_reports tablosu ─────────────────────────────────────────────
    try:
        supabase.table('moderation_reports').select('id').limit(1).execute()
        logger.info("init_db: moderation_reports tablosu doğrulandı ✅")
    except Exception as exc:
        _ddl_reports = (
            "CREATE TABLE IF NOT EXISTS moderation_reports (\n"
            "  id          uuid DEFAULT gen_random_uuid() PRIMARY KEY,\n"
            "  message_id  text,\n"
            "  content     text NOT NULL,\n"
            "  sender      text NOT NULL,\n"
            "  reporter_ip text,\n"
            "  is_inappropriate bool DEFAULT false,\n"
            "  severity    text DEFAULT 'low',\n"
            "  status      text DEFAULT 'pending',\n"
            "  admin_note  text,\n"
            "  created_at  timestamptz DEFAULT now()\n"
            ");"
        )
        logger.critical(
            f"init_db: 'moderation_reports' tablosuna erişilemiyor. "
            f"Supabase SQL Editöründe şu DDL'yi çalıştırın:\n{_ddl_reports}\nHata: {exc}"
        )

    # ── mtb_os tables (Enterprise Digital Twin OS) ─────────────────────────────
    try:
        supabase.table('bike_parts_catalog').select('id').limit(1).execute()
        logger.info("init_db: bike_parts_catalog tablosu doğrulandı ✅")
    except Exception as exc:
        _ddl_catalog = (
            "CREATE TABLE IF NOT EXISTS bike_parts_catalog (\n"
            "  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,\n"
            "  exact_model text NOT NULL,\n"
            "  aliases jsonb DEFAULT '[]'::jsonb,\n"
            "  category text,\n"
            "  subcategory text,\n"
            "  intended_riding text,\n"
            "  wheel_compatibility text,\n"
            "  boost_spacing boolean,\n"
            "  axle_type text,\n"
            "  rotor_compatibility text,\n"
            "  bb_standard text,\n"
            "  headset_standard text,\n"
            "  drivetrain_speed integer,\n"
            "  suspension_travel integer,\n"
            "  weight_grams integer,\n"
            "  msrp numeric,\n"
            "  production_year_start integer,\n"
            "  production_year_end integer,\n"
            "  generation text,\n"
            "  revision text,\n"
            "  geometry_data jsonb DEFAULT '{}'::jsonb,\n"
            "  compatibility_metadata jsonb DEFAULT '{}'::jsonb,\n"
            "  created_at timestamptz DEFAULT now()\n"
            ");"
        )
        logger.warning(
            f"init_db: 'bike_parts_catalog' tablosuna erişilemiyor. Lütfen Supabase SQL Editor üzerinden oluşturun.\n{_ddl_catalog}"
        )

    try:
        supabase.table('part_failure_database').select('id').limit(1).execute()
        logger.info("init_db: part_failure_database tablosu doğrulandı ✅")
    except Exception as exc:
        _ddl_failure = (
            "CREATE TABLE IF NOT EXISTS part_failure_database (\n"
            "  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,\n"
            "  exact_model text NOT NULL,\n"
            "  known_failures text,\n"
            "  failure_frequency text,\n"
            "  severity text,\n"
            "  affected_years text,\n"
            "  riding_conditions text,\n"
            "  fix_suggestions text,\n"
            "  created_at timestamptz DEFAULT now()\n"
            ");"
        )
        logger.warning(
            f"init_db: 'part_failure_database' tablosuna erişilemiyor. Lütfen Supabase SQL Editor üzerinden oluşturun.\n{_ddl_failure}"
        )

    logger.info("init_db: Veritabanı başlatma tamamlandı ✅")
