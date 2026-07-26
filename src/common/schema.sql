-- Durable per-user settings: UI language, translation language, reciter.
-- Applied idempotently at boot (CREATE TABLE IF NOT EXISTS) — no migration
-- framework at this scale (single table, three columns of actual data).
CREATE TABLE IF NOT EXISTS user_settings (
    telegram_user_id BIGINT PRIMARY KEY,
    ui_lang           TEXT NOT NULL DEFAULT 'en',
    translation_lang  TEXT NOT NULL DEFAULT 'en',
    reciter           TEXT NOT NULL DEFAULT 'Husary_128kbps',
    created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);
