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

-- Hifz identity: display name, leaderboard consent, when to push, and the two
-- denormalized streak counters (`session_log` remains the source of truth for
-- both; these exist so /streak and /profile are one cheap read).
--
-- `timezone` holds a fixed UTC offset as text, e.g. '+05:00' — not an IANA zone
-- name. That is deliberate: no tzdata dependency and no DST branches anywhere in
-- the streak or scheduler arithmetic. The column is TEXT rather than an interval
-- so an IANA name could be stored later without a migration.
CREATE TABLE IF NOT EXISTS user_profile (
    telegram_user_id   BIGINT PRIMARY KEY,
    display_name       TEXT,
    leaderboard_opt_in BOOLEAN NOT NULL DEFAULT false,
    timezone           TEXT,
    reminder_time      TIME,
    current_streak     INT NOT NULL DEFAULT 0,
    longest_streak     INT NOT NULL DEFAULT 0,
    created_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at         TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Only opted-in users are ever joined against, and they are the minority.
CREATE INDEX IF NOT EXISTS user_profile_leaderboard_idx
    ON user_profile (leaderboard_opt_in) WHERE leaderboard_opt_in;
-- The scheduler's per-tick scan: who has a reminder time at all.
CREATE INDEX IF NOT EXISTS user_profile_reminder_idx
    ON user_profile (reminder_time) WHERE reminder_time IS NOT NULL;

-- What the user knows by heart. Rows are merged on insert and split on removal,
-- so for a given (user_id, surah) they never overlap and never touch — every
-- percentage the bot reports is arithmetic over these, and an overlap would
-- double-count.
CREATE TABLE IF NOT EXISTS hifz_interval (
    id                BIGSERIAL PRIMARY KEY,
    user_id           BIGINT NOT NULL,
    surah             INT NOT NULL,
    start_ayah        INT NOT NULL,
    end_ayah          INT NOT NULL,
    marked_at         TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS hifz_interval_user_surah_idx
    ON hifz_interval (user_id, surah);

-- A memorization plan. One active plan per user is an application invariant
-- (see the plan lifecycle), not a constraint here: pausing and creating race in
-- a way a partial unique index would turn into a user-visible error.
CREATE TABLE IF NOT EXISTS plan (
    id                BIGSERIAL PRIMARY KEY,
    user_id           BIGINT NOT NULL,
    target_kind       TEXT NOT NULL,
    start_surah       INT NOT NULL,
    start_ayah        INT NOT NULL,
    end_surah         INT NOT NULL,
    end_ayah          INT NOT NULL,
    pace              INT NOT NULL DEFAULT 0,
    days_of_week      SMALLINT[] NOT NULL DEFAULT '{1,2,3,4,5,6,7}',
    status            TEXT NOT NULL DEFAULT 'active',
    created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS plan_user_status_idx ON plan (user_id, status);

-- The materialized daily portions, written in the same transaction as their
-- plan so the preview calendar the user approved is exactly what gets pushed.
CREATE TABLE IF NOT EXISTS plan_day (
    id                BIGSERIAL PRIMARY KEY,
    plan_id           BIGINT NOT NULL REFERENCES plan (id) ON DELETE CASCADE,
    scheduled_date    DATE NOT NULL,
    surah             INT NOT NULL,
    start_ayah        INT NOT NULL,
    end_ayah          INT NOT NULL,
    state             TEXT NOT NULL DEFAULT 'pending',
    created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS plan_day_plan_date_idx ON plan_day (plan_id, scheduled_date);

-- One row per completed session — a drill run through or a passed recall check.
-- `local_date` is the user's local day (from their fixed UTC offset) and is what
-- decides which day a session counts for.
CREATE TABLE IF NOT EXISTS session_log (
    id                BIGSERIAL PRIMARY KEY,
    user_id           BIGINT NOT NULL,
    local_date        DATE NOT NULL,
    kind              TEXT NOT NULL,
    surah             INT,
    start_ayah        INT,
    end_ayah          INT,
    occurred_at       TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Streak reads and the per-user half of the weekly board.
CREATE INDEX IF NOT EXISTS session_log_user_date_idx ON session_log (user_id, local_date);
-- The weekly aggregation scans a date window across every user.
CREATE INDEX IF NOT EXISTS session_log_date_idx ON session_log (local_date);
-- Idempotency: the same portion completed twice on the same local day logs once.
-- COALESCE because a session need not name a portion, and NULLs would otherwise
-- compare as distinct and defeat the whole point of the index.
CREATE UNIQUE INDEX IF NOT EXISTS session_log_dedupe_idx
    ON session_log (user_id, local_date, kind,
                    COALESCE(surah, 0), COALESCE(start_ayah, 0), COALESCE(end_ayah, 0));

-- The due-queue the in-process scheduler drains. `idempotency_key` is
-- conventionally (kind, target, local_date), which is what makes a restart, a
-- double boot or a retry unable to double-send.
CREATE TABLE IF NOT EXISTS scheduled_send (
    id                BIGSERIAL PRIMARY KEY,
    kind              TEXT NOT NULL,
    target_chat_id    BIGINT NOT NULL,
    thread_id         INT,
    due_at            TIMESTAMPTZ NOT NULL,
    payload           JSONB NOT NULL DEFAULT '{}'::jsonb,
    state             TEXT NOT NULL DEFAULT 'pending',
    idempotency_key   TEXT NOT NULL,
    claimed_at        TIMESTAMPTZ,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX IF NOT EXISTS scheduled_send_idempotency_key_idx
    ON scheduled_send (idempotency_key);
-- The claim query: pending rows already due, oldest first.
CREATE INDEX IF NOT EXISTS scheduled_send_state_due_idx ON scheduled_send (state, due_at);
