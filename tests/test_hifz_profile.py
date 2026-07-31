"""`/profile`, the leaderboard opt-in and the timezone / reminder capture (B1-B3).

Everything is driven through the seam (`hifz.dispatch_command`,
`dispatch_callback`, `dispatch_wizard`) with an `AsyncMock` bot, the way
`tests/test_hifz_seam.py` does — these tests exercise the handlers exactly as
`main.py` reaches them, so a registration mistake fails here rather than in
production.
"""

from datetime import date, datetime, time, timezone
from unittest.mock import AsyncMock

import pytest

import hifz
from hifz import Ctx
from hifz import profile as profile_feature
from lib.store import get_store

USER_ID = 900123
CHAT_ID = 900123


class _Settings:
    ui_lang = "en"
    translation_lang = "en"
    reciter = "Husary_128kbps"


@pytest.fixture(autouse=True)
def _isolate_registries():
    """Snapshot and restore the process-wide handler registries (see the seam's
    own tests: a leaked registration would follow every later test)."""
    saved = (dict(hifz.COMMANDS), dict(hifz.CALLBACKS), dict(hifz.WIZARDS), hifz._loaded)
    yield
    hifz.COMMANDS.clear()
    hifz.COMMANDS.update(saved[0])
    hifz.CALLBACKS.clear()
    hifz.CALLBACKS.update(saved[1])
    hifz.WIZARDS.clear()
    hifz.WIZARDS.update(saved[2])
    hifz._loaded = saved[3]


class _User:
    def __init__(self, username=None):
        self.id = USER_ID
        self.username = username


class _Message:
    def __init__(self, username=None):
        self.message_id = 77
        self.photo = None
        self.audio = None
        self.from_user = _User(username)


class _CallbackQuery:
    def __init__(self, username=None):
        self.id = "cq-1"
        self.message = _Message(username)
        self.from_user = _User(username)


async def _ctx(bot=None, username=None, argument="", tap=False) -> Ctx:
    from lib.utils import File
    bot = bot or AsyncMock()
    extra = ({"callback_query": _CallbackQuery(username)} if tap
             else {"message": _Message(username)})
    return await Ctx.build(bot, {}, File(), CHAT_ID, USER_ID, _Settings(),
                           argument=argument, **extra)


def _sent(bot) -> str:
    """The text of the last message the bot sent."""
    return bot.send_message.await_args.kwargs["text"]


def _edited(bot) -> str:
    """The text of the last in-place edit."""
    return bot.edit_message_text.await_args.kwargs["text"]


def _toast(bot) -> str:
    return bot.answer_callback_query.await_args.kwargs.get("text", "")


def _buttons(markup):
    return [b for row in markup.inline_keyboard for b in row]


def _callback_data(markup):
    return [b.callback_data for b in _buttons(markup)]


async def _profile_row():
    return await (await get_store()).profiles.get_profile(USER_ID)


# --- B1: the card --------------------------------------------------------------

class TestProfileCard:
    async def test_renders_for_a_user_who_has_used_nothing_else(self):
        # B1's done-when: every field has an unset state, so a first-contact user
        # gets a screen rather than a KeyError.
        bot = AsyncMock()
        assert await hifz.dispatch_command(await _ctx(bot), "profile") is True
        text = _sent(bot)
        assert "Your profile" in text
        assert "Name: not set" in text
        assert "Leaderboard: you are hidden" in text       # default off (B2)
        assert "Time zone: not set" in text
        assert "Daily reminder: off" in text
        assert "Plan: none yet" in text

    async def test_offers_a_button_for_every_field(self):
        bot = AsyncMock()
        await hifz.dispatch_command(await _ctx(bot), "profile")
        data = _callback_data(bot.send_message.await_args.kwargs["reply_markup"])
        assert data == [profile_feature.NAME_CB, profile_feature.BOARD_ON_CB,
                        profile_feature.TIMEZONE_CB, profile_feature.REMINDER_CB]

    async def test_the_profile_row_is_created_on_first_view(self):
        assert await _profile_row() is None
        await hifz.dispatch_command(await _ctx(), "profile")
        row = await _profile_row()
        assert row is not None and row.leaderboard_opt_in is False

    async def test_a_populated_profile_reads_back(self):
        store = await get_store()
        await store.profiles.set_display_name(USER_ID, "Abu Bakr")
        await store.profiles.set_leaderboard_opt_in(USER_ID, True)
        await store.profiles.set_timezone(USER_ID, "+05:00")
        await store.profiles.set_reminder_time(USER_ID, time(7, 30))
        bot = AsyncMock()
        await hifz.dispatch_command(await _ctx(bot), "profile")
        text = _sent(bot)
        assert "Name: Abu Bakr" in text
        assert "Leaderboard: you are listed" in text
        assert "UTC+05:00" in text
        assert "07:30" in text
        assert _callback_data(bot.send_message.await_args.kwargs["reply_markup"])[1] \
            == profile_feature.BOARD_OFF_CB

    async def test_an_active_plan_is_named_with_its_progress(self):
        from lib.store.plans import PlanDaySpec
        store = await get_store()
        days = [PlanDaySpec(date(2026, 8, 1), 67, 1, 5),
                PlanDaySpec(date(2026, 8, 2), 67, 6, 10)]
        plan = await store.plans.create_plan(USER_ID, "surah", 67, 1, 67, 30, 5,
                                             [1, 2, 3, 4, 5], days)
        first = (await store.plans.list_plan_days(plan.id))[0]
        await store.plans.claim_plan_day(first.id)
        await store.plans.complete_plan_day(first.id)
        bot = AsyncMock()
        await hifz.dispatch_command(await _ctx(bot), "profile")
        assert "Al-Mulk" in _sent(bot)
        assert "day 2 of 2" in _sent(bot)

    async def test_a_command_escapes_a_pending_wizard(self):
        ctx = await _ctx()
        ctx.wiz.start(USER_ID, profile_feature.WIZARD_NAME)
        await hifz.dispatch_command(ctx, "profile")
        assert ctx.wiz.is_active(USER_ID) is False


# --- B2: the leaderboard opt-in ------------------------------------------------

class TestLeaderboardOptIn:
    async def test_opt_in_adopts_the_telegram_username(self):
        bot = AsyncMock()
        ctx = await _ctx(bot, username="abubakr", tap=True)
        assert await hifz.dispatch_callback(ctx, profile_feature.BOARD_ON_CB) is True
        row = await _profile_row()
        assert row.display_name == "abubakr"
        assert row.leaderboard_opt_in is True
        assert _toast(bot) == "You are on the leaderboard now."
        assert "Name: abubakr" in _edited(bot)

    async def test_a_leading_at_sign_is_not_stored_twice(self):
        ctx = await _ctx(username="@abubakr", tap=True)
        await hifz.dispatch_callback(ctx, profile_feature.BOARD_ON_CB)
        assert (await _profile_row()).display_name == "abubakr"

    async def test_an_existing_name_is_not_overwritten_by_the_username(self):
        await (await get_store()).profiles.set_display_name(USER_ID, "Umm Salamah")
        ctx = await _ctx(username="someone_else", tap=True)
        await hifz.dispatch_callback(ctx, profile_feature.BOARD_ON_CB)
        row = await _profile_row()
        assert row.display_name == "Umm Salamah"
        assert row.leaderboard_opt_in is True

    async def test_a_user_with_no_username_is_asked_for_a_name(self):
        # B2's done-when, first half. Plenty of accounts have no @username, and
        # nobody is put on a public board under a blank label.
        bot = AsyncMock()
        ctx = await _ctx(bot, username=None, tap=True)
        await hifz.dispatch_callback(ctx, profile_feature.BOARD_ON_CB)
        assert "Send the name" in _edited(bot)
        assert ctx.wiz.kind(USER_ID) == profile_feature.WIZARD_NAME
        assert (await _profile_row()).leaderboard_opt_in is False   # not yet

    async def test_the_typed_name_completes_the_opt_in(self):
        ctx = await _ctx(username=None, tap=True)
        await hifz.dispatch_callback(ctx, profile_feature.BOARD_ON_CB)

        bot = AsyncMock()
        typed = await _ctx(bot)
        assert await hifz.dispatch_wizard(typed, "Bilal ibn Rabah") is True
        row = await _profile_row()
        assert row.display_name == "Bilal ibn Rabah"
        assert row.leaderboard_opt_in is True
        assert "You will appear as Bilal ibn Rabah." in _sent(bot)
        assert "You are on the leaderboard now." in _sent(bot)
        assert typed.wiz.is_active(USER_ID) is False

    @pytest.mark.parametrize("typed", ["x", "", "   ", "y" * 33])
    async def test_a_name_outside_2_32_characters_is_refused(self, typed):
        bot = AsyncMock()
        ctx = await _ctx(bot)
        ctx.wiz.start(USER_ID, profile_feature.WIZARD_NAME, join=True)
        await hifz.dispatch_wizard(ctx, typed)
        assert _sent(bot) == "Use between 2 and 32 characters."
        assert ctx.wiz.is_active(USER_ID) is True       # a retry, not a dead end
        assert await _profile_row() is None

    async def test_the_boundaries_themselves_are_accepted(self):
        for typed in ("ab", "z" * 32):
            ctx = await _ctx()
            ctx.wiz.start(USER_ID, profile_feature.WIZARD_NAME, join=False)
            await hifz.dispatch_wizard(ctx, typed)
            assert (await _profile_row()).display_name == typed

    async def test_whitespace_is_collapsed_not_rejected(self):
        ctx = await _ctx()
        ctx.wiz.start(USER_ID, profile_feature.WIZARD_NAME, join=False)
        await hifz.dispatch_wizard(ctx, "  Abu   Bakr \n")
        assert (await _profile_row()).display_name == "Abu Bakr"

    async def test_a_name_containing_html_is_escaped_on_screen(self):
        # Rule 4: user text in an HTML message goes through html.escape, exactly
        # as main.build_verse_text escapes corpus text. Unbalanced markup would
        # make Telegram reject the whole message.
        bot = AsyncMock()
        ctx = await _ctx(bot)
        ctx.wiz.start(USER_ID, profile_feature.WIZARD_NAME, join=False)
        await hifz.dispatch_wizard(ctx, "<b>Ali</b> & co")
        assert (await _profile_row()).display_name == "<b>Ali</b> & co"   # stored raw
        text = _sent(bot)
        assert "&lt;b&gt;Ali&lt;/b&gt; &amp; co" in text
        assert "<b>Ali</b>" not in text

    async def test_opt_out_removes_the_user_from_every_board_query(self):
        # B2's done-when, second half: absent from the *query*, not hidden by the
        # renderer (lib/leaderboard.py refuses to filter at render time).
        from lib.leaderboard import weekly_board
        from lib.streaks import record_session
        store = await get_store()
        ctx = await _ctx(username="abubakr", tap=True)
        await hifz.dispatch_callback(ctx, profile_feature.BOARD_ON_CB)
        now = datetime(2026, 8, 5, 12, 0, tzinfo=timezone.utc)
        await record_session(USER_ID, "drill", utc_now=now)
        board = await weekly_board(USER_ID, utc_now=now)
        assert [e.user_id for e in board.entries] == [USER_ID]

        bot = AsyncMock()
        out = await _ctx(bot, tap=True)
        await hifz.dispatch_callback(out, profile_feature.BOARD_OFF_CB)
        assert (await _profile_row()).leaderboard_opt_in is False
        assert _toast(bot) == "You have been removed from the leaderboard."

        start, end = board.week_start, board.week_end
        assert await store.sessions.weekly_leaderboard(start, end) == []
        after = await weekly_board(USER_ID, utc_now=now)
        assert after.entries == () and after.me is None

    async def test_the_board_modules_spelled_out_opt_in_button_works(self):
        # `hifz/leaderboard.py` hard-codes "hp:board:on" rather than importing it,
        # so that a broken profile module cannot take the board down with it. That
        # only holds if this module actually answers that exact shape.
        from hifz import leaderboard as board_feature
        assert board_feature.CB_JOIN == profile_feature.BOARD_ON_CB
        ctx = await _ctx(username="abubakr", tap=True)
        await hifz.dispatch_callback(ctx, board_feature.CB_JOIN)
        assert (await _profile_row()).leaderboard_opt_in is True

    async def test_the_short_legacy_shapes_are_still_answered(self):
        # Keyboards are never expired by Telegram; a card sent before the shapes
        # were spelled out must keep working.
        await hifz.dispatch_callback(await _ctx(username="abubakr", tap=True), "hp:b:1")
        assert (await _profile_row()).leaderboard_opt_in is True
        await hifz.dispatch_callback(await _ctx(tap=True), "hp:b:0")
        assert (await _profile_row()).leaderboard_opt_in is False

    async def test_opting_out_keeps_the_name_for_a_later_opt_in(self):
        ctx = await _ctx(username="abubakr", tap=True)
        await hifz.dispatch_callback(ctx, profile_feature.BOARD_ON_CB)
        await hifz.dispatch_callback(await _ctx(tap=True), profile_feature.BOARD_OFF_CB)
        assert (await _profile_row()).display_name == "abubakr"
        await hifz.dispatch_callback(await _ctx(tap=True), profile_feature.BOARD_ON_CB)
        assert (await _profile_row()).leaderboard_opt_in is True


# --- B3: timezone and reminder time --------------------------------------------

class TestTimezone:
    async def test_the_picker_offers_every_offset(self):
        from lib.localtime import OFFSET_CHOICES
        bot = AsyncMock()
        ctx = await _ctx(bot, tap=True)
        await hifz.dispatch_callback(ctx, profile_feature.TIMEZONE_CB)
        assert "Pick your UTC offset" in _edited(bot)
        markup = bot.edit_message_text.await_args.kwargs["reply_markup"]
        labels = [b.text for b in _buttons(markup)]
        for offset in OFFSET_CHOICES:
            assert offset in labels
        assert len(OFFSET_CHOICES) == 34

    async def test_picking_an_offset_stores_it_normalized(self):
        bot = AsyncMock()
        ctx = await _ctx(bot, tap=True)
        await hifz.dispatch_callback(ctx, "hp:tz:+05:00")
        assert (await _profile_row()).timezone == "+05:00"
        assert _toast(bot) == "Time zone set to UTC+05:00."
        assert "Time zone: UTC+05:00" in _edited(bot)

    async def test_changing_the_timezone_shifts_the_next_push(self):
        # B3's done-when. The scheduler queues each day's push from the profile as
        # it stands (lib.scheduler.schedule_daily), so the stored offset is the
        # only thing that has to move.
        from lib.scheduler import schedule_daily
        store = await get_store()
        now = datetime(2026, 8, 5, 0, 0, tzinfo=timezone.utc)
        await hifz.dispatch_callback(await _ctx(tap=True), "hp:tz:+00:00")
        ctx = await _ctx(bot=AsyncMock())
        ctx.wiz.start(USER_ID, profile_feature.WIZARD_REMINDER)
        await hifz.dispatch_wizard(ctx, "07:30")

        at_utc = profile_feature.next_push_utc(await _profile_row(), now)
        assert at_utc == datetime(2026, 8, 5, 7, 30, tzinfo=timezone.utc)

        await hifz.dispatch_callback(await _ctx(tap=True), "hp:tz:+05:00")
        at_plus5 = profile_feature.next_push_utc(await _profile_row(), now)
        assert at_plus5 == datetime(2026, 8, 5, 2, 30, tzinfo=timezone.utc)
        assert at_utc - at_plus5 == abs(at_utc - at_plus5)      # it moved earlier

        # and the queued push follows the stored offset, not a copy of it
        row = await schedule_daily(store, "plan_day", CHAT_ID, time(7, 30),
                                   (await _profile_row()).timezone, now=now)
        assert row.due_at == at_plus5

    async def test_a_forged_or_stale_offset_is_ignored_not_stored(self):
        for junk in ("hp:tz:", "hp:tz:Europe/Tashkent", "hp:tz:+99:00", "hp:tz:x"):
            ctx = await _ctx(tap=True)
            await hifz.dispatch_callback(ctx, junk)
            assert (await _profile_row()).timezone is None

    def test_the_offset_helpers_are_reusable_by_another_wizard(self):
        # B3 is captured once during first plan setup (workstream D) and changed
        # from here; both call sites must behave identically, so the prefix is a
        # parameter rather than a second implementation.
        markup = profile_feature.offset_keyboard("en", prefix="hm:tz:", columns=6)
        data = _callback_data(markup)
        assert data[0] == "hm:tz:-12:00" and data[-1] == "hm:tz:+14:00"
        assert profile_feature.offset_from_callback("hm:tz:+05:30",
                                                    prefix="hm:tz:") == "+05:30"
        assert profile_feature.offset_from_callback("hp:tz:+05:30",
                                                    prefix="hm:tz:") is None


class TestReminderTime:
    async def test_the_prompt_offers_turning_reminders_off(self):
        bot = AsyncMock()
        ctx = await _ctx(bot, tap=True)
        await hifz.dispatch_callback(ctx, profile_feature.REMINDER_CB)
        assert "24-hour" in _edited(bot)
        assert ctx.wiz.kind(USER_ID) == profile_feature.WIZARD_REMINDER
        assert profile_feature.REMINDER_OFF_CB in _callback_data(
            bot.edit_message_text.await_args.kwargs["reply_markup"])

    @pytest.mark.parametrize("typed,expected", [
        ("07:30", time(7, 30)), ("7:30", time(7, 30)), ("0730", time(7, 30)),
        ("7", time(7, 0)), ("19:05", time(19, 5)), ("23:59", time(23, 59)),
    ])
    async def test_a_typed_time_is_stored(self, typed, expected):
        bot = AsyncMock()
        ctx = await _ctx(bot)
        ctx.wiz.start(USER_ID, profile_feature.WIZARD_REMINDER)
        await hifz.dispatch_wizard(ctx, typed)
        assert (await _profile_row()).reminder_time == expected
        assert ctx.wiz.is_active(USER_ID) is False

    @pytest.mark.parametrize("typed", ["tomorrow", "25:00", "07:60", "-1", "7:3:0"])
    async def test_an_unparseable_time_re_prompts(self, typed):
        bot = AsyncMock()
        ctx = await _ctx(bot)
        ctx.wiz.start(USER_ID, profile_feature.WIZARD_REMINDER)
        await hifz.dispatch_wizard(ctx, typed)
        assert _sent(bot) == "Send a time in 24-hour form, e.g. 07:30."
        assert ctx.wiz.is_active(USER_ID) is True

    async def test_reminders_can_be_turned_off(self):
        store = await get_store()
        await store.profiles.set_reminder_time(USER_ID, time(7, 30))
        bot = AsyncMock()
        await hifz.dispatch_callback(await _ctx(bot, tap=True),
                                     profile_feature.REMINDER_OFF_CB)
        assert (await _profile_row()).reminder_time is None
        assert _toast(bot) == "Daily reminders are off."
        assert profile_feature.next_push_utc(await _profile_row()) is None

    def test_the_reminder_helpers_are_reusable_by_another_wizard(self):
        markup = profile_feature.reminder_keyboard("en", off_data="hm:rem:off",
                                                   cancel_data="hm:x")
        assert _callback_data(markup) == ["hm:rem:off", "hm:x"]
        assert profile_feature.parse_reminder_time("07:30") == time(7, 30)
        assert profile_feature.parse_reminder_time("nope") is None
        assert profile_feature.format_reminder_time(time(7, 5)) == "07:05"


# --- Defensive parsing and the 64-byte cap -------------------------------------

class TestCallbackDataDiscipline:
    def test_every_shape_fits_telegrams_cap(self):
        shapes = [profile_feature.PROFILE_CB, profile_feature.NAME_CB,
                  profile_feature.BOARD_ON_CB, profile_feature.BOARD_OFF_CB,
                  profile_feature.TIMEZONE_CB, profile_feature.REMINDER_CB,
                  profile_feature.REMINDER_OFF_CB,
                  profile_feature.OFFSET_PREFIX + "-12:00"]
        for shape in shapes:
            assert shape.startswith(hifz.PREFIXES["profile"])
            assert len(shape.encode()) <= 64, shape

    async def test_unrecognized_data_redraws_the_card_instead_of_failing(self):
        # A keyboard is never expired by Telegram: a tap can arrive years later,
        # from a build whose callback shapes are gone.
        bot = AsyncMock()
        for junk in ("hp:", "hp:zzz", "hp:b:", "hp:b:2", "hp:r:xx", "hp:n:extra"):
            bot.reset_mock()
            assert await hifz.dispatch_callback(await _ctx(bot, tap=True), junk) is True
            bot.answer_callback_query.assert_awaited()      # no spinner left behind
            assert "Your profile" in _edited(bot)

    async def test_the_back_button_leaves_a_wizard_and_shows_the_card(self):
        bot = AsyncMock()
        ctx = await _ctx(bot, tap=True)
        ctx.wiz.start(USER_ID, profile_feature.WIZARD_NAME, join=True)
        await hifz.dispatch_callback(ctx, profile_feature.PROFILE_CB)
        assert ctx.wiz.is_active(USER_ID) is False
        assert "Your profile" in _edited(bot)
        assert (await _profile_row()).leaderboard_opt_in is False
