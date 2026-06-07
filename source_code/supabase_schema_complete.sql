-- ==============================================================================
-- FreeriderTR Supabase Production SQL Schema Migration (COMPLETE & UNIFIED)
-- Bu dosya uygulamadaki TÜM tabloları ve eksik kolonları (is_banned dahil)
-- kusursuz bir şekilde kurmak veya onarmak için tasarlanmıştır.
-- ==============================================================================

-- ==============================================================================
-- 1. USERS (Kullanıcılar) & BANNED USERS
-- ==============================================================================
CREATE TABLE IF NOT EXISTS public.users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    username TEXT UNIQUE NOT NULL
);

-- Var olan 'users' tablosuna eksik kolonları ekle
ALTER TABLE public.users ADD COLUMN IF NOT EXISTS password_hash TEXT;
ALTER TABLE public.users ADD COLUMN IF NOT EXISTS name TEXT;
ALTER TABLE public.users ADD COLUMN IF NOT EXISTS bio TEXT;
ALTER TABLE public.users ADD COLUMN IF NOT EXISTS avatar TEXT;
ALTER TABLE public.users ADD COLUMN IF NOT EXISTS city TEXT;
ALTER TABLE public.users ADD COLUMN IF NOT EXISTS instagram TEXT;
ALTER TABLE public.users ADD COLUMN IF NOT EXISTS youtube TEXT;
ALTER TABLE public.users ADD COLUMN IF NOT EXISTS role TEXT DEFAULT 'User';
ALTER TABLE public.users ADD COLUMN IF NOT EXISTS stats JSONB DEFAULT '{}'::jsonb;
ALTER TABLE public.users ADD COLUMN IF NOT EXISTS is_banned BOOLEAN DEFAULT false; -- KÖK BAN SİSTEMİ
ALTER TABLE public.users ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT now();
ALTER TABLE public.users ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ DEFAULT now();

CREATE INDEX IF NOT EXISTS idx_users_username ON public.users(username);

-- Banned Users (Admin Ban Logları)
CREATE TABLE IF NOT EXISTS public.banned_users (
    username TEXT PRIMARY KEY, -- Hedeflenen temel veri
    reason TEXT,
    banned_by TEXT,
    banned_at TIMESTAMPTZ DEFAULT now()
);

-- Eski sistemde 'banned' adında bir tablo varsa ve kullanılmıyorsa, verileri aktar
DO $$
BEGIN
    IF EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename  = 'banned') THEN
        -- Eğer banned tablosunda banned_by veya ts gibi kolonlar yoksa hata vermemesi için
        -- sadece username'i kopyalıyoruz.
        INSERT INTO public.banned_users (username, banned_by, reason)
        SELECT username, 'system', 'Eski sistemden aktarıldı'
        FROM public.banned
        ON CONFLICT (username) DO NOTHING;
    END IF;
END
$$;

-- Tüm banned_users tablosundaki kullanıcıların ana 'users' tablosundaki durumunu True yap
UPDATE public.users SET is_banned = true WHERE username IN (SELECT username FROM public.banned_users);


-- ==============================================================================
-- 2. MARKERS (Harita Noktaları)
-- ==============================================================================
CREATE TABLE IF NOT EXISTS public.markers (
    id TEXT PRIMARY KEY
);

-- Var olan 'markers' tablosuna eksik kolonları ekle
ALTER TABLE public.markers ADD COLUMN IF NOT EXISTS username TEXT;
ALTER TABLE public.markers ADD COLUMN IF NOT EXISTS "addedBy" TEXT; -- Kodda addedBy olarak geçiyor
ALTER TABLE public.markers ADD COLUMN IF NOT EXISTS title TEXT;
ALTER TABLE public.markers ADD COLUMN IF NOT EXISTS name TEXT; -- Kodda name olarak geçiyor
ALTER TABLE public.markers ADD COLUMN IF NOT EXISTS "desc" TEXT;
ALTER TABLE public.markers ADD COLUMN IF NOT EXISTS category TEXT; 
ALTER TABLE public.markers ADD COLUMN IF NOT EXISTS lat DOUBLE PRECISION;
ALTER TABLE public.markers ADD COLUMN IF NOT EXISTS lng DOUBLE PRECISION;
ALTER TABLE public.markers ADD COLUMN IF NOT EXISTS image TEXT;
ALTER TABLE public.markers ADD COLUMN IF NOT EXISTS difficulty TEXT;
ALTER TABLE public.markers ADD COLUMN IF NOT EXISTS extra_note TEXT;
ALTER TABLE public.markers ADD COLUMN IF NOT EXISTS is_dangerous BOOLEAN DEFAULT false;
ALTER TABLE public.markers ADD COLUMN IF NOT EXISTS danger_reports INTEGER DEFAULT 0;
ALTER TABLE public.markers ADD COLUMN IF NOT EXISTS ratings JSONB DEFAULT '[]'::jsonb;
ALTER TABLE public.markers ADD COLUMN IF NOT EXISTS avg_rating DOUBLE PRECISION DEFAULT 0;
ALTER TABLE public.markers ADD COLUMN IF NOT EXISTS likes JSONB DEFAULT '[]'::jsonb;
ALTER TABLE public.markers ADD COLUMN IF NOT EXISTS dislikes JSONB DEFAULT '[]'::jsonb;
ALTER TABLE public.markers ADD COLUMN IF NOT EXISTS is_hidden BOOLEAN DEFAULT false;
ALTER TABLE public.markers ADD COLUMN IF NOT EXISTS report_count INTEGER DEFAULT 0;
ALTER TABLE public.markers ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT now();
ALTER TABLE public.markers ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ DEFAULT now();

-- Önceki sistemden kalan "icon_type" verilerini "category" sütununa kopyala
DO $$
BEGIN
    IF EXISTS (SELECT column_name FROM information_schema.columns WHERE table_name='markers' AND column_name='icon_type') THEN
        EXECUTE 'UPDATE public.markers SET category = icon_type WHERE category IS NULL AND icon_type IS NOT NULL';
    END IF;
END
$$;

CREATE INDEX IF NOT EXISTS idx_markers_lat_lng ON public.markers(lat, lng);
CREATE INDEX IF NOT EXISTS idx_markers_category ON public.markers(category);


-- ==============================================================================
-- 3. MESSAGES (Global Chat)
-- ==============================================================================
CREATE TABLE IF NOT EXISTS public.messages (
    id TEXT PRIMARY KEY
);

ALTER TABLE public.messages ADD COLUMN IF NOT EXISTS sender TEXT;
ALTER TABLE public.messages ADD COLUMN IF NOT EXISTS "user" TEXT; -- Kodda user olarak da kullanılıyor
ALTER TABLE public.messages ADD COLUMN IF NOT EXISTS text TEXT;
ALTER TABLE public.messages ADD COLUMN IF NOT EXISTS image TEXT;
ALTER TABLE public.messages ADD COLUMN IF NOT EXISTS voice TEXT;
ALTER TABLE public.messages ADD COLUMN IF NOT EXISTS reply_to TEXT;
ALTER TABLE public.messages ADD COLUMN IF NOT EXISTS ts BIGINT;
ALTER TABLE public.messages ADD COLUMN IF NOT EXISTS likes JSONB DEFAULT '[]'::jsonb;
ALTER TABLE public.messages ADD COLUMN IF NOT EXISTS is_flagged BOOLEAN DEFAULT false;
ALTER TABLE public.messages ADD COLUMN IF NOT EXISTS flag_count INTEGER DEFAULT 0;
ALTER TABLE public.messages ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT now();

CREATE INDEX IF NOT EXISTS idx_messages_ts ON public.messages(ts DESC);


-- ==============================================================================
-- 4. DMS (Özel Mesajlar)
-- ==============================================================================
CREATE TABLE IF NOT EXISTS public.dms (
    id TEXT PRIMARY KEY
);

ALTER TABLE public.dms ADD COLUMN IF NOT EXISTS sender TEXT;
ALTER TABLE public.dms ADD COLUMN IF NOT EXISTS receiver TEXT;
ALTER TABLE public.dms ADD COLUMN IF NOT EXISTS participants JSONB DEFAULT '[]'::jsonb;
ALTER TABLE public.dms ADD COLUMN IF NOT EXISTS text TEXT;
ALTER TABLE public.dms ADD COLUMN IF NOT EXISTS image TEXT;
ALTER TABLE public.dms ADD COLUMN IF NOT EXISTS voice TEXT;
ALTER TABLE public.dms ADD COLUMN IF NOT EXISTS ts BIGINT;
ALTER TABLE public.dms ADD COLUMN IF NOT EXISTS is_read BOOLEAN DEFAULT false;
ALTER TABLE public.dms ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT now();

CREATE INDEX IF NOT EXISTS idx_dms_sender_receiver ON public.dms(sender, receiver);
CREATE INDEX IF NOT EXISTS idx_dms_ts ON public.dms(ts DESC);


-- ==============================================================================
-- 5. EVENTS (Buluşmalar & Etkinlikler)
-- ==============================================================================
CREATE TABLE IF NOT EXISTS public.events (
    id TEXT PRIMARY KEY
);

ALTER TABLE public.events ADD COLUMN IF NOT EXISTS owner TEXT;
ALTER TABLE public.events ADD COLUMN IF NOT EXISTS creator TEXT; -- Kodda creator olarak da geçiyor
ALTER TABLE public.events ADD COLUMN IF NOT EXISTS title TEXT;
ALTER TABLE public.events ADD COLUMN IF NOT EXISTS description TEXT;
ALTER TABLE public.events ADD COLUMN IF NOT EXISTS date TEXT;
ALTER TABLE public.events ADD COLUMN IF NOT EXISTS time TEXT;
ALTER TABLE public.events ADD COLUMN IF NOT EXISTS lat DOUBLE PRECISION;
ALTER TABLE public.events ADD COLUMN IF NOT EXISTS lng DOUBLE PRECISION;
ALTER TABLE public.events ADD COLUMN IF NOT EXISTS participants JSONB DEFAULT '[]'::jsonb;
ALTER TABLE public.events ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT now();


-- ==============================================================================
-- 6. STORIES & REELS (Hikayeler)
-- ==============================================================================
CREATE TABLE IF NOT EXISTS public.stories (
    id TEXT PRIMARY KEY
);
ALTER TABLE public.stories ADD COLUMN IF NOT EXISTS "user" TEXT;
ALTER TABLE public.stories ADD COLUMN IF NOT EXISTS image TEXT;
ALTER TABLE public.stories ADD COLUMN IF NOT EXISTS video TEXT;
ALTER TABLE public.stories ADD COLUMN IF NOT EXISTS text TEXT;
ALTER TABLE public.stories ADD COLUMN IF NOT EXISTS expires_at BIGINT;
ALTER TABLE public.stories ADD COLUMN IF NOT EXISTS views JSONB DEFAULT '[]'::jsonb;
ALTER TABLE public.stories ADD COLUMN IF NOT EXISTS likes JSONB DEFAULT '[]'::jsonb;
ALTER TABLE public.stories ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT now();
CREATE INDEX IF NOT EXISTS idx_stories_expires_at ON public.stories(expires_at);

-- Reels
CREATE TABLE IF NOT EXISTS public.reels (
    id TEXT PRIMARY KEY
);
ALTER TABLE public.reels ADD COLUMN IF NOT EXISTS "user" TEXT;
ALTER TABLE public.reels ADD COLUMN IF NOT EXISTS video TEXT;
ALTER TABLE public.reels ADD COLUMN IF NOT EXISTS text TEXT;
ALTER TABLE public.reels ADD COLUMN IF NOT EXISTS likes JSONB DEFAULT '[]'::jsonb;
ALTER TABLE public.reels ADD COLUMN IF NOT EXISTS comment_count INTEGER DEFAULT 0;
ALTER TABLE public.reels ADD COLUMN IF NOT EXISTS views INTEGER DEFAULT 0;
ALTER TABLE public.reels ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT now();

CREATE TABLE IF NOT EXISTS public.comments (
    id TEXT PRIMARY KEY
);
ALTER TABLE public.comments ADD COLUMN IF NOT EXISTS "user" TEXT;
ALTER TABLE public.comments ADD COLUMN IF NOT EXISTS reel_id TEXT;
ALTER TABLE public.comments ADD COLUMN IF NOT EXISTS text TEXT;
ALTER TABLE public.comments ADD COLUMN IF NOT EXISTS ts BIGINT;
ALTER TABLE public.comments ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT now();


-- ==============================================================================
-- 7. MARKET (İlanlar / Garaj)
-- ==============================================================================
CREATE TABLE IF NOT EXISTS public.market (
    id TEXT PRIMARY KEY
);
ALTER TABLE public.market ADD COLUMN IF NOT EXISTS owner TEXT;
ALTER TABLE public.market ADD COLUMN IF NOT EXISTS title TEXT;
ALTER TABLE public.market ADD COLUMN IF NOT EXISTS description TEXT;
ALTER TABLE public.market ADD COLUMN IF NOT EXISTS price TEXT;
ALTER TABLE public.market ADD COLUMN IF NOT EXISTS image TEXT;
ALTER TABLE public.market ADD COLUMN IF NOT EXISTS category TEXT;
ALTER TABLE public.market ADD COLUMN IF NOT EXISTS views INTEGER DEFAULT 0;
ALTER TABLE public.market ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT now();


-- ==============================================================================
-- 8. SETTINGS & APP STATE (Genel Ayarlar)
-- ==============================================================================
CREATE TABLE IF NOT EXISTS public.settings (
    id TEXT PRIMARY KEY
);
ALTER TABLE public.settings ADD COLUMN IF NOT EXISTS value TEXT;
ALTER TABLE public.settings ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ DEFAULT now();


-- ==============================================================================
-- 9. ADMIN LOGS
-- ==============================================================================
CREATE TABLE IF NOT EXISTS public.admin_logs (
    id TEXT PRIMARY KEY
);
ALTER TABLE public.admin_logs ADD COLUMN IF NOT EXISTS admin TEXT;
ALTER TABLE public.admin_logs ADD COLUMN IF NOT EXISTS action TEXT;
ALTER TABLE public.admin_logs ADD COLUMN IF NOT EXISTS target TEXT;
ALTER TABLE public.admin_logs ADD COLUMN IF NOT EXISTS detail TEXT;
ALTER TABLE public.admin_logs ADD COLUMN IF NOT EXISTS ts BIGINT;


-- ==============================================================================
-- 10. MODERATION REPORTS
-- ==============================================================================
CREATE TABLE IF NOT EXISTS public.moderation_reports (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY
);
ALTER TABLE public.moderation_reports ADD COLUMN IF NOT EXISTS message_id TEXT;
ALTER TABLE public.moderation_reports ADD COLUMN IF NOT EXISTS content TEXT;
ALTER TABLE public.moderation_reports ADD COLUMN IF NOT EXISTS sender TEXT;
ALTER TABLE public.moderation_reports ADD COLUMN IF NOT EXISTS reporter_ip TEXT;
ALTER TABLE public.moderation_reports ADD COLUMN IF NOT EXISTS is_inappropriate BOOLEAN DEFAULT false;
ALTER TABLE public.moderation_reports ADD COLUMN IF NOT EXISTS severity TEXT DEFAULT 'low';
ALTER TABLE public.moderation_reports ADD COLUMN IF NOT EXISTS status TEXT DEFAULT 'pending';
ALTER TABLE public.moderation_reports ADD COLUMN IF NOT EXISTS admin_note TEXT;
ALTER TABLE public.moderation_reports ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT now();


-- ==============================================================================
-- DATABASE TRIGGER OPTIMIZATIONS (updated_at)
-- ==============================================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

DROP TRIGGER IF EXISTS update_users_updated_at ON public.users;
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON public.users FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

DROP TRIGGER IF EXISTS update_markers_updated_at ON public.markers;
CREATE TRIGGER update_markers_updated_at BEFORE UPDATE ON public.markers FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
