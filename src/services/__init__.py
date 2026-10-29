# The operations behind every feature, shared by the two surfaces that expose
# them (docs/MINI_APP_PLAN.md §3, Phase 1):
#
#   bot handlers (src/hifz/*, src/main.py)  ─┐
#                                            ├─► services/* ─► lib/* ─► infra/store
#   Mini App API (src/api/*)                ─┘
#
# A service takes plain values and a store and returns plain values. It never
# imports `telegram`, never formats a chat message and never touches HTTP — that
# is what lets the bot and the app run the same rule instead of two copies of it.
# (tests/test_service_layer.py enforces the import rule.)
