-- ==============================================================================
-- Bisiklet Yarışması (Bike Competition) Tablosu Kurulumu
-- Bu SQL kodunu Supabase SQL Editörü'nde çalıştırın.
-- ==============================================================================

CREATE TABLE IF NOT EXISTS public.bike_competitions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    username TEXT NOT NULL,
    week_id TEXT NOT NULL,
    category TEXT NOT NULL,
    bike_data JSONB DEFAULT '{}'::jsonb,
    user_ratings JSONB DEFAULT '[]'::jsonb,
    avg_rating DOUBLE PRECISION DEFAULT 0,
    final_rank INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Bir kullanıcı aynı haftada aynı kategoride birden fazla bisiklet yarıştıramazsın diye (Opsiyonel Güvenlik):
-- CREATE UNIQUE INDEX IF NOT EXISTS idx_bike_comp_user_week ON public.bike_competitions(username, week_id);

CREATE INDEX IF NOT EXISTS idx_bike_comp_week ON public.bike_competitions(week_id);
CREATE INDEX IF NOT EXISTS idx_bike_comp_category ON public.bike_competitions(category);

-- Trigger for updated_at
DROP TRIGGER IF EXISTS update_bike_competitions_updated_at ON public.bike_competitions;
CREATE TRIGGER update_bike_competitions_updated_at 
BEFORE UPDATE ON public.bike_competitions 
FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
