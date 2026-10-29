# Testing & CI

## Running the tests locally

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
pytest                        # from the repo root
pytest --cov=src --cov-report=term-missing   # with coverage
```

Run from the **repo root**: `conftest.py` puts `src/` on the import path and pins the
process CWD there (the corpus files — `quran-data.xml`, `Al_Jalalain_Eng.txt`, the
`translations/` dir — resolve relative to CWD, exactly as in production under
`uvicorn main:app --app-dir src`).

Tests need **no network and no Redis**: `conftest.py` sets `REDIS_HOST_URL=""`, which
makes `config/redis.py` fall back to its in-memory store, and outbound Telegram calls
are replaced by an `AsyncMock`.

## What's covered

| File | Area |
|------|------|
| `tests/test_parsing.py` | `parse_ayah` / `parse_ayah_range` — separators, ranges, reversed/`–` dashes, invalid input |
| `tests/test_quran.py` | bounds (`exists`), navigation wraparound, random-in-bounds, and corpus integrity (6236 ayahs, tafsir) |
| `tests/test_translations.py` | `TranslationRegistry` lazy load, caching, missing-language fallback |
| `tests/test_locales.py` | i18n integrity for all 48 languages (mirrors `scripts/check_locales.py`) + `t` / `normalize_lang` / `button_action` |
| `tests/test_utils.py` | media-URL construction and the state store (user state, language, file-id cache) |
| `tests/test_webhook.py` | FastAPI `/` health + token-gated `/webhook/{token}` routing |
| `tests/test_handle_update.py` | end-to-end update dispatch: commands, buttons, navigation, inline queries, language callback |

## CI — Blue-Green pipeline

`.github/workflows/blue-green-ci.yml`:

```
test ─► build ─► preflight ─► deploy-green ─► smoke-green ─► promote
                                   └───────────────── rollback (on any deploy failure)
```

- **test / build** run on every push and PR (the always-on gate): pytest across
  Python 3.10–3.12, the locale check, and a Docker image build.
- **deploy → promote** run only on `main`, and only once `KOYEB_API_TOKEN` is set —
  otherwise they're skipped and the pipeline stays green. New revisions go to the
  **inactive** colour, are health-checked (`/` must return `{"status":"ok"}`), then
  traffic cuts over and the old colour is released. A failure anywhere in the deploy
  chain triggers **rollback**, leaving the previously-live colour serving.

See the header comment in the workflow file for the exact secret/variable setup.
