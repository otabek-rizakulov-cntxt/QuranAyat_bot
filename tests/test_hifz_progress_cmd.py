"""`/progress` and `/forgot` (C3), driven through the seam.

`tests/test_hifz_progress.py` pins the arithmetic in `lib/hifz_progress.py`; this
file pins the two commands built on it — above all the deliberate choice of
**units**: the surah is quoted in ayahs, the juz and the whole Qur'an in mushaf
pages, because that is how a hafiz measures each of them.
"""

from unittest.mock import AsyncMock

import pytest

import hifz
from hifz import Ctx
from hifz import progress as progress_feature
from hifz.refs import juz_ref
from lib.store import get_store
from modules import Quran

USER_ID = 900456
CHAT_ID = 900456


class _Settings:
    ui_lang = "en"
    translation_lang = "en"
    reciter = "Husary_128kbps"


@pytest.fixture(autouse=True)
def _isolate_registries():
    saved = (dict(hifz.COMMANDS), dict(hifz.CALLBACKS), dict(hifz.WIZARDS), hifz._loaded)
    yield
    hifz.COMMANDS.clear()
    hifz.COMMANDS.update(saved[0])
    hifz.CALLBACKS.clear()
    hifz.CALLBACKS.update(saved[1])
    hifz.WIZARDS.clear()
    hifz.WIZARDS.update(saved[2])
    hifz._loaded = saved[3]


class _Message:
    message_id = 55
    photo = None
    audio = None


class _CallbackQuery:
    def __init__(self):
        self.id = "cq-1"
        self.message = _Message()


async def _ctx(bot=None, argument="", tap=False) -> Ctx:
    from lib.utils import File
    bot = bot or AsyncMock()
    extra = {"callback_query": _CallbackQuery()} if tap else {"message": _Message()}
    return await Ctx.build(bot, {}, File(), CHAT_ID, USER_ID, _Settings(),
                           argument=argument, **extra)


def _sent(bot) -> str:
    return bot.send_message.await_args.kwargs["text"]


def _edited(bot) -> str:
    return bot.edit_message_text.await_args.kwargs["text"]


async def _mark(surah, start, end):
    await (await get_store()).hifz.add_interval(USER_ID, surah, start, end)


async def _intervals(surah=None):
    rows = await (await get_store()).hifz.list_intervals(USER_ID, surah)
    return [(r.surah, r.start_ayah, r.end_ayah) for r in rows]


async def _progress(bot=None, argument=""):
    bot = bot or AsyncMock()
    assert await hifz.dispatch_command(await _ctx(bot, argument), "progress") is True
    return _sent(bot)


# --- /progress -----------------------------------------------------------------

class TestProgressCommand:
    async def test_a_user_with_nothing_marked_gets_the_empty_copy(self):
        text = await _progress()
        assert "Nothing marked yet" in text
        assert "%" not in text

    async def test_the_headline_quotes_the_surah_in_ayahs(self):
        # C2's acceptance number, surfaced by C3: 8 of Al-Mulk's 30 ayahs is 27%.
        await _mark(67, 1, 8)
        text = await _progress()
        assert "Al-Mulk: 8/30 ayahs — 27%" in text

    async def test_the_juz_and_quran_lines_are_quoted_in_pages_not_ayahs(self):
        # The decision this module exists to carry: a juz is "twenty pages", never
        # "431 ayahs". By ayahs juz 29 would read 2%; by pages it reads 3%.
        from lib.hifz_progress import summarize
        await _mark(67, 1, 8)
        summary = summarize([(67, 1, 8)])
        assert summary.focus_juz.percent_text != summary.focus_juz_pages.percent_text
        text = await _progress()
        assert "Juz 29: %s%%" % summary.focus_juz_pages.percent_text in text
        assert "Juz 29: %s%%" % summary.focus_juz.percent_text not in text

    async def test_the_whole_quran_line_is_pages_too(self):
        # A whole juz 30 is 9% of the Qur'an by ayahs (its ayahs are short) and 4%
        # by pages. The page figure is the one a hafiz recognizes.
        from lib.hifz_progress import summarize
        ref = juz_ref(30)
        spans = progress_feature.surah_spans(ref)
        for surah, start, end in spans:
            await _mark(surah, start, end)
        summary = summarize(spans, focus_surah=None)
        assert summary.quran.percent_text == "9"
        assert summary.quran_pages.percent_text == "4"
        text = await _progress()
        assert "Whole Qur'an: 4%" in text
        assert "Whole Qur'an: 9%" not in text

    async def test_the_breakdown_lists_the_other_started_surahs(self):
        await _mark(67, 1, 8)
        await _mark(112, 1, 4)
        text = await _progress(argument="112")
        assert "%s: 4/4 ayahs — 100%%" % Quran.get_surah_name(112) in text  # the focus
        assert "Al-Mulk: 8/30 ayahs — 27%" in text       # the breakdown

    async def test_the_focus_juz_is_not_repeated_in_the_breakdown(self):
        # It was already shown in pages; a second, different percentage for the
        # same juz on the same screen reads as a bug.
        await _mark(67, 1, 8)
        text = await _progress()
        assert text.count("Juz 29:") == 1

    async def test_an_argument_points_the_headline_at_a_surah(self):
        await _mark(67, 1, 8)
        await _mark(2, 1, 5)
        text = await _progress(argument="67")
        assert text.splitlines()[2].startswith("Al-Mulk:")

    async def test_junk_after_the_command_falls_back_to_the_default_view(self):
        await _mark(67, 1, 8)
        text = await _progress(argument="not a reference")
        assert "Al-Mulk: 8/30 ayahs — 27%" in text


class TestProgressTaps:
    async def test_a_surah_button_refocuses_the_summary_in_place(self):
        await _mark(67, 1, 8)
        await _mark(112, 1, 4)
        bot = AsyncMock()
        assert await hifz.dispatch_callback(await _ctx(bot, tap=True),
                                            "hg:s:67") is True
        assert _edited(bot).splitlines()[2].startswith("Al-Mulk:")
        bot.answer_callback_query.assert_awaited()

    @pytest.mark.parametrize("junk", ["hg:", "hg:s:", "hg:s:zzz", "hg:s:0",
                                      "hg:s:115", "hg:s:67:extra", "hg:r"])
    async def test_stale_or_forged_data_redraws_instead_of_raising(self, junk):
        await _mark(67, 1, 8)
        bot = AsyncMock()
        assert await hifz.dispatch_callback(await _ctx(bot, tap=True), junk) is True
        assert "What you have memorized" in _edited(bot)
        bot.answer_callback_query.assert_awaited()

    def test_every_callback_shape_fits_telegrams_cap(self):
        for shape in (progress_feature.REFRESH_CB,
                      progress_feature.SURAH_PREFIX + "114"):
            assert shape.startswith(hifz.PREFIXES["progress"])
            assert len(shape.encode()) <= 64, shape


# --- /forgot -------------------------------------------------------------------

class TestForgot:
    async def test_it_splits_an_interval_in_two(self):
        # C3's done-when, verbatim.
        await _mark(67, 1, 10)
        bot = AsyncMock()
        assert await hifz.dispatch_command(await _ctx(bot, "67:5-6"), "forgot") is True
        assert await _intervals(67) == [(67, 1, 4), (67, 7, 10)]
        assert "Unmarked 67:5-6." in _sent(bot)

    async def test_the_confirmation_carries_the_updated_numbers(self):
        await _mark(67, 1, 10)
        bot = AsyncMock()
        await hifz.dispatch_command(await _ctx(bot, "67:5-6"), "forgot")
        assert "Al-Mulk: 8/30 ayahs — 27%" in _sent(bot)

    async def test_a_single_ayah_can_be_unmarked(self):
        await _mark(67, 1, 10)
        await hifz.dispatch_command(await _ctx(argument="67:5"), "forgot")
        assert await _intervals(67) == [(67, 1, 4), (67, 6, 10)]

    async def test_unmarking_an_end_shortens_rather_than_splits(self):
        await _mark(67, 1, 10)
        await hifz.dispatch_command(await _ctx(argument="67:8-10"), "forgot")
        assert await _intervals(67) == [(67, 1, 7)]

    async def test_unmarking_everything_leaves_nothing_behind(self):
        await _mark(67, 1, 10)
        bot = AsyncMock()
        await hifz.dispatch_command(await _ctx(bot, "67"), "forgot")
        assert await _intervals() == []
        assert "Unmarked 67:1-30." in _sent(bot)
        assert "Nothing marked yet" in _sent(bot)

    async def test_a_cross_surah_range_takes_one_call_per_surah(self):
        # `remove_range` is per-surah by construction; a reference is not.
        await _mark(67, 25, 30)
        await _mark(68, 1, 10)
        bot = AsyncMock()
        await hifz.dispatch_command(await _ctx(bot, "67:30-68:2"), "forgot")
        assert await _intervals() == [(67, 25, 29), (68, 3, 10)]
        assert "Unmarked 67:30-68:2." in _sent(bot)

    async def test_a_juz_reference_only_writes_where_something_was_marked(self):
        # Juz 30 spans 37 surahs; touching all of them for a user who has marked
        # one would be 37 writes to unmark six ayahs.
        await _mark(112, 1, 4)
        store = await get_store()
        calls = []
        original = store.hifz.remove_range

        async def counting(user_id, surah, start, end):
            calls.append(surah)
            return await original(user_id, surah, start, end)

        store.hifz.remove_range = counting
        try:
            await hifz.dispatch_command(await _ctx(argument="juz 30"), "forgot")
        finally:
            store.hifz.remove_range = original
        assert calls == [112]
        assert await _intervals() == []

    async def test_a_bare_command_explains_itself(self):
        bot = AsyncMock()
        await hifz.dispatch_command(await _ctx(bot, "   "), "forgot")
        assert _sent(bot) == "Send what to unmark, for example /forgot 67:5-6."

    @pytest.mark.parametrize("junk", ["banana", "67:99", "115", "juz 31", "0:0"])
    async def test_junk_input_is_refused_by_the_shared_string(self, junk):
        await _mark(67, 1, 10)
        bot = AsyncMock()
        await hifz.dispatch_command(await _ctx(bot, junk), "forgot")
        assert "isn't a reference I recognise" in _sent(bot)
        assert await _intervals(67) == [(67, 1, 10)]        # nothing touched

    async def test_forgetting_something_never_marked_says_so(self):
        await _mark(67, 1, 10)
        bot = AsyncMock()
        await hifz.dispatch_command(await _ctx(bot, "2:1-5"), "forgot")
        assert _sent(bot) == "You had not marked that as memorized."
        assert await _intervals() == [(67, 1, 10)]

    async def test_forgetting_a_range_next_to_a_marked_one_is_a_no_op(self):
        await _mark(67, 1, 10)
        bot = AsyncMock()
        await hifz.dispatch_command(await _ctx(bot, "67:11-12"), "forgot")
        assert _sent(bot) == "You had not marked that as memorized."
        assert await _intervals(67) == [(67, 1, 10)]


class TestSurahSpans:
    def test_a_within_surah_reference_is_one_span(self):
        from hifz.refs import parse_reference
        assert progress_feature.surah_spans(parse_reference("67:5-6")) == [(67, 5, 6)]

    def test_a_cross_surah_reference_is_split_at_the_boundary(self):
        from hifz.refs import parse_reference
        assert progress_feature.surah_spans(parse_reference("67:30-68:2")) == [
            (67, 30, 30), (68, 1, 2)]

    def test_a_juz_covers_every_surah_it_touches_whole(self):
        ref = juz_ref(30)
        spans = progress_feature.surah_spans(ref)
        assert spans[0][0] == ref.start_surah and spans[-1][0] == ref.end_surah
        assert spans[-1] == (114, 1, Quran.get_surah_length(114))
        assert sum(end - start + 1 for _, start, end in spans) == ref.count()
