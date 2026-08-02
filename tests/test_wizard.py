"""Multi-step draft state (`lib.wizard`).

`/memorize` collects four answers across several turns and `/profile` collects a
name and a timezone, none of which the pre-existing `set_awaiting_input` flag can
hold — it is a bare string with no payload slot. This module is the draft that
replaces it for those flows, and the properties that matter are that a draft
accumulates, that exactly one is ever in flight, and that there is always a way
out.

Driven against the in-process MemoryStore that conftest pins via an empty
REDIS_HOST_URL, so nothing here touches a network.
"""

import pytest

from lib.utils import File
from lib.wizard import CANCEL_COMMANDS, DRAFT_TTL, Wizard

USER = 810001


@pytest.fixture
def wiz() -> Wizard:
    return Wizard()


class TestLifecycle:
    def test_no_draft_by_default(self, wiz):
        assert wiz.get(USER) is None
        assert wiz.kind(USER) is None
        assert wiz.step(USER) is None
        assert wiz.data(USER) == {}
        assert wiz.is_active(USER) is False

    def test_start_creates_a_draft(self, wiz):
        wiz.start(USER, "memorize", step="target")
        assert wiz.is_active(USER) is True
        assert wiz.kind(USER) == "memorize"
        assert wiz.step(USER) == "target"
        assert wiz.data(USER) == {}

    def test_start_can_seed_data(self, wiz):
        wiz.start(USER, "memorize", step="pace", surah=67)
        assert wiz.data(USER) == {"surah": 67}

    def test_clear_ends_it(self, wiz):
        wiz.start(USER, "memorize")
        wiz.clear(USER)
        assert wiz.is_active(USER) is False

    def test_clear_is_idempotent(self, wiz):
        wiz.clear(USER)
        wiz.clear(USER)
        assert wiz.get(USER) is None

    def test_step_defaults_to_empty_string(self, wiz):
        wiz.start(USER, "profile_name")
        assert wiz.step(USER) == ""


class TestAccumulation:
    """The whole point of the draft: four answers held together while the user thinks."""

    def test_update_merges_without_losing_earlier_answers(self, wiz):
        wiz.start(USER, "memorize", step="target")
        wiz.update(USER, step="pace", target_kind="surah", surah=67)
        wiz.update(USER, step="days", pace=5)
        wiz.update(USER, step="confirm", days=[1, 2, 3, 4, 5])
        draft = wiz.get(USER)
        assert draft["step"] == "confirm"
        assert draft["data"] == {"target_kind": "surah", "surah": 67, "pace": 5,
                                 "days": [1, 2, 3, 4, 5]}

    def test_update_can_overwrite_an_answer(self, wiz):
        wiz.start(USER, "memorize", surah=67)
        wiz.update(USER, surah=36)
        assert wiz.data(USER)["surah"] == 36

    def test_update_without_step_keeps_the_step(self, wiz):
        wiz.start(USER, "memorize", step="pace")
        wiz.update(USER, pace=3)
        assert wiz.step(USER) == "pace"

    def test_update_on_an_expired_draft_returns_none(self, wiz):
        # A draft can expire between two taps; every caller must handle it.
        assert wiz.update(USER, pace=3) is None

    def test_set_step_on_an_expired_draft_returns_none(self, wiz):
        assert wiz.set_step(USER, "confirm") is None

    def test_set_step_keeps_data(self, wiz):
        wiz.start(USER, "memorize", surah=67)
        wiz.set_step(USER, "days")
        assert wiz.step(USER) == "days"
        assert wiz.data(USER) == {"surah": 67}

    def test_data_returns_a_copy(self, wiz):
        wiz.start(USER, "memorize", surah=67)
        snapshot = wiz.data(USER)
        snapshot["surah"] = 999
        assert wiz.data(USER)["surah"] == 67

    def test_survives_nested_and_non_string_values(self, wiz):
        wiz.start(USER, "memorize")
        wiz.update(USER, days=[1, 3, 5], preview=[{"d": "2026-08-01", "ref": "67:1-5"}])
        draft = wiz.get(USER)
        assert draft["data"]["days"] == [1, 3, 5]
        assert draft["data"]["preview"][0]["ref"] == "67:1-5"


class TestOneDraftPerUser:
    def test_starting_a_second_wizard_replaces_the_first(self, wiz):
        wiz.start(USER, "memorize", step="pace", surah=67)
        wiz.start(USER, "profile_name")
        assert wiz.kind(USER) == "profile_name"
        assert wiz.data(USER) == {}      # the old answers are gone, not merged

    def test_users_do_not_share_drafts(self, wiz):
        wiz.start(USER, "memorize", surah=67)
        wiz.start(USER + 1, "profile_name")
        assert wiz.kind(USER) == "memorize"
        assert wiz.kind(USER + 1) == "profile_name"
        wiz.clear(USER + 1)
        assert wiz.kind(USER) == "memorize"


class TestCancel:
    @pytest.mark.parametrize("text", list(CANCEL_COMMANDS))
    def test_recognises_the_cancel_words(self, text):
        assert Wizard.is_cancel(text) is True

    @pytest.mark.parametrize("text", ["/CANCEL", "  /cancel  ", "Cancel",
                                      "/cancel@BismillahBot"])
    def test_cancel_is_case_space_and_botname_tolerant(self, text):
        # "/help@BotName" is already tolerated by the command parser; match it
        assert Wizard.is_cancel(text) is True

    @pytest.mark.parametrize("text", ["67:1-8", "", "cancellation", "/memorize", None])
    def test_ordinary_input_is_not_cancel(self, text):
        assert Wizard.is_cancel(text) is False

    def test_cancel_reports_whether_there_was_anything_to_cancel(self, wiz):
        assert wiz.cancel(USER) is False
        wiz.start(USER, "memorize")
        assert wiz.cancel(USER) is True
        assert wiz.is_active(USER) is False


class TestCorruptState:
    def test_a_non_json_value_is_treated_as_absent(self, wiz):
        wiz.redis.set(wiz._key(USER), "not json at all")
        assert wiz.get(USER) is None
        assert wiz.is_active(USER) is False

    def test_a_json_value_of_the_wrong_shape_is_dropped(self, wiz):
        wiz.redis.set(wiz._key(USER), '["a", "list"]')
        assert wiz.get(USER) is None

    def test_a_draft_without_a_kind_is_dropped(self, wiz):
        wiz.redis.set(wiz._key(USER), '{"step": "pace"}')
        assert wiz.get(USER) is None

    def test_a_corrupt_draft_does_not_trap_the_user(self, wiz):
        wiz.redis.set(wiz._key(USER), "garbage")
        wiz.get(USER)                      # reading it clears it
        wiz.start(USER, "memorize")        # and a fresh wizard still starts
        assert wiz.kind(USER) == "memorize"


class TestCoexistsWithTheReciterFlow:
    """`set_awaiting_input` is deliberately NOT migrated — it is the right shape
    for a 120 s single-turn flag, and rewriting it would only add risk."""

    def test_the_legacy_awaiting_flag_still_works(self):
        f = File()
        f.set_awaiting_input(700111, "reciter_search")
        assert f.pop_awaiting_input(700111) == "reciter_search"

    def test_a_draft_and_an_awaiting_flag_do_not_collide(self, wiz):
        f = File()
        f.set_awaiting_input(USER, "reciter_search")
        wiz.start(USER, "memorize", surah=67)
        assert f.pop_awaiting_input(USER) == "reciter_search"
        assert wiz.kind(USER) == "memorize"      # untouched by the pop

    def test_they_use_different_keys(self, wiz):
        f = File()
        assert wiz._key(USER) != f._awaiting_key(USER)


def test_ttl_is_long_enough_to_think_and_short_enough_to_forget():
    # 30 minutes: survives putting the phone down, cannot ambush the user tomorrow
    assert 10 * 60 <= DRAFT_TTL <= 60 * 60


def test_draft_is_written_with_that_ttl(wiz):
    captured = {}

    class RecordingRedis:
        def set(self, key, value, ex=None):
            captured["ex"] = ex

        def get(self, key):
            return None

        def delete(self, key):
            pass

    Wizard(redis=RecordingRedis()).start(USER, "memorize")
    assert captured["ex"] == DRAFT_TTL
