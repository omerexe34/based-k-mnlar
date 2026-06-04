CREATE TABLE IF NOT EXISTS public.giveaways (
    id               BIGSERIAL PRIMARY KEY,
    title            TEXT NOT NULL,
    prize            TEXT NOT NULL,
    description      TEXT DEFAULT '',
    image_url        TEXT,
    end_date         DATE NOT NULL,
    status           TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'completed', 'cancelled')),
    participants     JSONB NOT NULL DEFAULT '[]'::jsonb,
    winner_count     INT NOT NULL DEFAULT 1,
    winners          JSONB NOT NULL DEFAULT '[]'::jsonb,
    winner_username  TEXT,
    winner_instagram TEXT,
    finalized_at     TIMESTAMPTZ,
    created_by       TEXT NOT NULL,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_giveaways_status ON public.giveaways (status);
CREATE INDEX IF NOT EXISTS idx_giveaways_end_date ON public.giveaways (end_date);

ALTER TABLE public.giveaways ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Herkes okuyabilir" ON public.giveaways FOR SELECT USING (true);
CREATE POLICY "Service role yazabilir" ON public.giveaways FOR ALL TO service_role USING (true) WITH CHECK (true);

