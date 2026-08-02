"""The merge-on-insert / split-on-remove arithmetic (`lib.store.hifz`), C1.

`tests/test_store_contract.py` pins the *behaviour* both store legs must agree
on. This file goes after the *arithmetic*: it enumerates every relative position
two spans can be in, and then throws long random operation sequences at the store
and asserts the invariant that every percentage in the product depends on —

    for one (user, surah) the stored spans are disjoint, non-adjacent, ordered,
    and their union is exactly the set of ayahs the user has marked.

If that invariant ever breaks, `/progress` starts double-counting and there is
nothing in the data to reconcile it against, because the rows *are* the record.
The exhaustive and randomized tests are the point of the file; the named cases
below them exist so a failure says which shape broke rather than "seed 3".
"""

import random

import pytest

from lib.store import get_store
from lib.store.hifz import HifzInterval, _covers, _merge_span, _overlaps, _split_span, _touches

USER = 1
AL_MULK = 67          # 30 ayahs
YASIN = 36            # 83 ayahs


async def _hifz():
    return (await get_store()).hifz


def _spans(intervals):
    return [(i.surah, i.start_ayah, i.end_ayah) for i in intervals]


def _ayahs(intervals):
    """The set of (surah, ayah) the stored intervals cover."""
    covered = set()
    for interval in intervals:
        for ayah in range(interval.start_ayah, interval.end_ayah + 1):
            covered.add((interval.surah, ayah))
    return covered


def _assert_invariant(intervals):
    """Disjoint, non-adjacent, ordered — the one thing that must always hold.

    Non-adjacency is checked as strictly as disjointness on purpose: two rows
    that merely abut (1-4 and 5-8) are not *wrong* about which ayahs are known,
    but they mean the merge failed to fire, and a store that tolerates that will
    tolerate the overlap it is one operation away from.
    """
    keys = [(i.surah, i.start_ayah) for i in intervals]
    assert keys == sorted(keys), "intervals came back out of order: %r" % (_spans(intervals),)

    by_surah = {}
    for interval in intervals:
        assert interval.start_ayah <= interval.end_ayah, "inverted span %r" % (interval,)
        assert interval.start_ayah >= 1, "ayah numbers start at 1: %r" % (interval,)
        by_surah.setdefault(interval.surah, []).append(
            (interval.start_ayah, interval.end_ayah))

    for surah, spans in by_surah.items():
        spans.sort()
        for (_, first_end), (second_start, _) in zip(spans, spans[1:]):
            assert second_start > first_end + 1, (
                "surah %d holds overlapping or adjacent spans %r" % (surah, spans))


# --- The pure helpers ----------------------------------------------------------
#
# Both store legs share these, so proving them here proves the SQL leg's
# arithmetic too — only its WHERE clauses and row plumbing remain unproven, and
# the contract suite covers those against a real Postgres when one is available.

class TestHelpers:
    def test_touches_accepts_overlap_and_abutment_but_not_a_gap(self):
        assert _touches(1, 8, 5, 10)           # overlapping
        assert _touches(1, 8, 9, 10)           # abutting on the right
        assert _touches(9, 10, 1, 8)           # abutting on the left
        assert _touches(1, 8, 3, 4)            # contained
        assert not _touches(1, 8, 10, 12)      # one ayah of daylight
        assert not _touches(10, 12, 1, 8)

    def test_overlaps_is_touches_without_the_abutment(self):
        assert _overlaps(1, 8, 5, 10)
        assert _overlaps(1, 8, 8, 8)
        assert not _overlaps(1, 8, 9, 10)      # abutting is NOT overlapping
        assert not _overlaps(9, 10, 1, 8)

    def test_covers_is_true_only_for_full_containment(self):
        assert _covers(1, 10, 3, 5)
        assert _covers(1, 10, 1, 10)
        assert not _covers(1, 10, 1, 11)
        assert not _covers(3, 5, 1, 10)

    def test_merge_span_is_the_union_of_the_extremes(self):
        assert _merge_span([(1, 3), (7, 9)], 2, 8) == (1, 9)
        assert _merge_span([], 4, 6) == (4, 6)
        assert _merge_span([(1, 30)], 5, 6) == (1, 30)

    def test_split_span_yields_zero_one_or_two_pieces(self):
        assert _split_span(1, 10, 1, 10) == []                  # erased
        assert _split_span(1, 10, 1, 4) == [(5, 10)]            # head trimmed
        assert _split_span(1, 10, 7, 10) == [(1, 6)]            # tail trimmed
        assert _split_span(1, 10, 5, 6) == [(1, 4), (7, 10)]    # the /forgot hole
        assert _split_span(1, 10, 1, 30) == []                  # removal overhangs

    def test_split_span_pieces_never_leak_outside_the_original(self):
        for span_start, span_end in ((1, 10), (5, 5), (3, 8)):
            for start in range(1, 13):
                for end in range(start, 13):
                    for piece_start, piece_end in _split_span(span_start, span_end,
                                                              start, end):
                        assert span_start <= piece_start <= piece_end <= span_end
                        assert piece_end < start or piece_start > end


# --- Marking ------------------------------------------------------------------

class TestAddInterval:
    async def test_partial_overlap_yields_one_interval(self):
        """The spec's headline case: 67:1-8 then 67:5-10 is 67:1-10, never two rows."""
        hifz = await _hifz()
        await hifz.add_interval(USER, AL_MULK, 1, 8)
        merged = await hifz.add_interval(USER, AL_MULK, 5, 10)
        assert (merged.surah, merged.start_ayah, merged.end_ayah) == (AL_MULK, 1, 10)
        assert _spans(await hifz.list_intervals(USER)) == [(AL_MULK, 1, 10)]

    async def test_abutting_from_the_right_coalesces(self):
        hifz = await _hifz()
        await hifz.add_interval(USER, AL_MULK, 1, 4)
        await hifz.add_interval(USER, AL_MULK, 5, 8)
        assert _spans(await hifz.list_intervals(USER)) == [(AL_MULK, 1, 8)]

    async def test_abutting_from_the_left_coalesces(self):
        hifz = await _hifz()
        await hifz.add_interval(USER, AL_MULK, 5, 8)
        await hifz.add_interval(USER, AL_MULK, 1, 4)
        assert _spans(await hifz.list_intervals(USER)) == [(AL_MULK, 1, 8)]

    async def test_a_one_ayah_gap_is_bridged_but_a_two_ayah_gap_is_not(self):
        """The boundary the merge turns on, tested from both sides."""
        hifz = await _hifz()
        await hifz.add_interval(USER, AL_MULK, 1, 4)
        await hifz.add_interval(USER, AL_MULK, 5, 8)          # gap of 0 -> merges
        assert _spans(await hifz.list_intervals(USER)) == [(AL_MULK, 1, 8)]

        await hifz.add_interval(USER, YASIN, 1, 4)
        await hifz.add_interval(USER, YASIN, 6, 8)            # gap of 1 -> stays split
        assert _spans(await hifz.list_intervals(USER, surah=YASIN)) == [
            (YASIN, 1, 4), (YASIN, 6, 8)]

    async def test_the_bridging_ayah_joins_both_neighbours(self):
        hifz = await _hifz()
        await hifz.add_interval(USER, AL_MULK, 1, 4)
        await hifz.add_interval(USER, AL_MULK, 6, 8)
        await hifz.add_interval(USER, AL_MULK, 5, 5)
        assert _spans(await hifz.list_intervals(USER)) == [(AL_MULK, 1, 8)]

    async def test_containment_leaves_the_row_completely_untouched(self):
        """Re-marking known ayahs must not churn the id or the marked_at date."""
        hifz = await _hifz()
        original = await hifz.add_interval(USER, AL_MULK, 1, 10)
        again = await hifz.add_interval(USER, AL_MULK, 5, 6)
        assert (again.id, again.marked_at) == (original.id, original.marked_at)
        assert (again.start_ayah, again.end_ayah) == (1, 10)
        assert _spans(await hifz.list_intervals(USER)) == [(AL_MULK, 1, 10)]

    async def test_re_marking_the_exact_same_range_is_a_no_op(self):
        hifz = await _hifz()
        original = await hifz.add_interval(USER, AL_MULK, 1, 10)
        again = await hifz.add_interval(USER, AL_MULK, 1, 10)
        assert again.id == original.id
        assert _spans(await hifz.list_intervals(USER)) == [(AL_MULK, 1, 10)]

    async def test_a_bridge_absorbs_every_interval_it_reaches(self):
        hifz = await _hifz()
        for start, end in ((1, 3), (6, 8), (11, 13), (20, 22)):
            await hifz.add_interval(USER, AL_MULK, start, end)
        await hifz.add_interval(USER, AL_MULK, 2, 12)
        assert _spans(await hifz.list_intervals(USER)) == [(AL_MULK, 1, 13),
                                                           (AL_MULK, 20, 22)]

    async def test_the_returned_interval_always_covers_what_was_asked_for(self):
        """Callers show "you now know X" from the return value, so it must be true."""
        hifz = await _hifz()
        for start, end in ((5, 8), (1, 3), (10, 12), (2, 11), (20, 20)):
            marked = await hifz.add_interval(USER, AL_MULK, start, end)
            assert marked.start_ayah <= start and marked.end_ayah >= end

    async def test_reversed_endpoints_are_normalized_not_rejected(self):
        hifz = await _hifz()
        await hifz.add_interval(USER, AL_MULK, 8, 1)
        assert _spans(await hifz.list_intervals(USER)) == [(AL_MULK, 1, 8)]

    async def test_ayah_zero_is_rejected(self):
        """Nothing downstream can make sense of ayah 0, so it never gets stored."""
        hifz = await _hifz()
        with pytest.raises(ValueError):
            await hifz.add_interval(USER, AL_MULK, 0, 5)
        with pytest.raises(ValueError):
            await hifz.add_interval(USER, AL_MULK, -3, -1)
        assert await hifz.list_intervals(USER) == []

    async def test_a_mark_reaching_two_bad_rows_collapses_them(self):
        """The merge re-derives the union, so it repairs what it reaches.

        A pair of overlapping rows can only get into the table from outside the
        store (a hand-written fix, a migration), and marking a range that touches
        both collapses them: `_merge_span` takes the extremes of everything it
        found rather than trusting the rows to already be disjoint.

        This is repair, not self-healing — see the next test. It is why the write
        path, not a periodic cleanup, is the thing that has to be airtight.
        """
        store = await get_store()
        state = store.state
        for start, end in ((1, 10), (5, 15)):
            state.hifz_interval.append(
                HifzInterval(state.next_id(), USER, AL_MULK, start, end, None))
        await store.hifz.add_interval(USER, AL_MULK, 1, 20)
        intervals = await store.hifz.list_intervals(USER)
        assert _spans(intervals) == [(AL_MULK, 1, 20)]
        _assert_invariant(intervals)

    async def test_a_mark_out_of_reach_leaves_a_bad_row_pair_alone(self):
        """The limit of that repair, pinned so nobody mistakes it for a guarantee.

        `add_interval` only ever looks at rows its own range touches, which is what
        keeps it one indexed lookup instead of a scan of the surah. Overlapping
        rows outside that reach survive untouched — so an overlap that ever got
        written would persist, and the percentages built on it would stay wrong.
        The store's answer is to make the overlap unwritable in the first place
        (the merge here, the advisory lock in the Postgres leg), not to sweep up
        after it.
        """
        store = await get_store()
        state = store.state
        for start, end in ((1, 10), (5, 15)):
            state.hifz_interval.append(
                HifzInterval(state.next_id(), USER, AL_MULK, start, end, None))
        await store.hifz.add_interval(USER, AL_MULK, 12, 20)
        assert _spans(await store.hifz.list_intervals(USER)) == [(AL_MULK, 1, 10),
                                                                  (AL_MULK, 5, 20)]

    async def test_the_advisory_lock_key_is_unique_per_user_and_surah(self):
        """The bigint packed for `pg_advisory_xact_lock` must not collide.

        A collision would serialize two unrelated users (harmless but slow); a
        *missed* collision — two different (user, surah) pairs mapping to one key
        is the harmless direction, the dangerous one is the same pair mapping to
        two keys, which cannot happen here. Checked against a realistically large
        Telegram id because the pair is packed rather than hashed.
        """
        from lib.store.hifz import PostgresHifzStore
        key = PostgresHifzStore._lock_key
        pairs = [(user, surah)
                 for user in (1, 7_000_000_000, 7_000_000_001)
                 for surah in range(1, 115)]
        assert len({key(*pair) for pair in pairs}) == len(pairs)
        assert key(7_000_000_000, 114) < 2 ** 63 - 1


# --- Unmarking ----------------------------------------------------------------

class TestRemoveRange:
    async def test_forgot_the_middle_splits_in_two(self):
        """§7 acceptance: `/forgot 67:5-6` turns 67:1-10 into 67:1-4 and 67:7-10."""
        hifz = await _hifz()
        await hifz.add_interval(USER, AL_MULK, 1, 10)
        pieces = await hifz.remove_range(USER, AL_MULK, 5, 6)
        assert [(p.start_ayah, p.end_ayah) for p in pieces] == [(1, 4), (7, 10)]
        assert _spans(await hifz.list_intervals(USER)) == [(AL_MULK, 1, 4),
                                                           (AL_MULK, 7, 10)]

    async def test_the_split_halves_keep_the_original_marked_at(self):
        """Forgetting the middle of a page does not un-learn the edges.

        Both halves were memorized on the original date; stamping them "now" would
        make a `/forgot` look like fresh progress to anything reading marked_at.
        """
        hifz = await _hifz()
        original = await hifz.add_interval(USER, AL_MULK, 1, 10)
        pieces = await hifz.remove_range(USER, AL_MULK, 5, 6)
        assert [p.marked_at for p in pieces] == [original.marked_at,
                                                 original.marked_at]

    async def test_removing_a_single_ayah_from_the_middle(self):
        hifz = await _hifz()
        await hifz.add_interval(USER, AL_MULK, 1, 10)
        await hifz.remove_range(USER, AL_MULK, 5, 5)
        assert _spans(await hifz.list_intervals(USER)) == [(AL_MULK, 1, 4),
                                                           (AL_MULK, 6, 10)]

    async def test_removing_the_head_trims_and_removing_the_tail_trims(self):
        hifz = await _hifz()
        await hifz.add_interval(USER, AL_MULK, 5, 20)
        await hifz.remove_range(USER, AL_MULK, 1, 9)
        assert _spans(await hifz.list_intervals(USER)) == [(AL_MULK, 10, 20)]
        await hifz.remove_range(USER, AL_MULK, 18, 30)
        assert _spans(await hifz.list_intervals(USER)) == [(AL_MULK, 10, 17)]

    async def test_removing_the_whole_interval_deletes_it(self):
        hifz = await _hifz()
        await hifz.add_interval(USER, AL_MULK, 5, 10)
        assert await hifz.remove_range(USER, AL_MULK, 5, 10) == []
        assert await hifz.list_intervals(USER) == []

    async def test_removal_spanning_several_intervals_trims_the_ends_and_erases_the_rest(self):
        hifz = await _hifz()
        for start, end in ((1, 5), (8, 12), (15, 20), (25, 28)):
            await hifz.add_interval(USER, AL_MULK, start, end)
        await hifz.remove_range(USER, AL_MULK, 4, 18)
        assert _spans(await hifz.list_intervals(USER)) == [
            (AL_MULK, 1, 3), (AL_MULK, 19, 20), (AL_MULK, 25, 28)]

    async def test_removal_does_not_reach_an_abutting_neighbour(self):
        """The asymmetry between marking and unmarking, stated as a test.

        Marking 67:5-6 next to 67:7-10 absorbs it. Unmarking 67:5-6 must not.
        """
        hifz = await _hifz()
        await hifz.add_interval(USER, AL_MULK, 1, 4)
        await hifz.add_interval(USER, AL_MULK, 7, 10)
        await hifz.remove_range(USER, AL_MULK, 5, 6)
        assert _spans(await hifz.list_intervals(USER)) == [(AL_MULK, 1, 4),
                                                           (AL_MULK, 7, 10)]

    async def test_removing_an_unmarked_range_is_a_no_op(self):
        hifz = await _hifz()
        await hifz.add_interval(USER, AL_MULK, 1, 5)
        assert await hifz.remove_range(USER, AL_MULK, 10, 20) == []
        assert _spans(await hifz.list_intervals(USER)) == [(AL_MULK, 1, 5)]

    async def test_removing_from_an_empty_store_is_a_no_op(self):
        hifz = await _hifz()
        assert await hifz.remove_range(USER, AL_MULK, 1, 30) == []

    async def test_reversed_endpoints_are_normalized(self):
        hifz = await _hifz()
        await hifz.add_interval(USER, AL_MULK, 1, 10)
        await hifz.remove_range(USER, AL_MULK, 6, 5)
        assert _spans(await hifz.list_intervals(USER)) == [(AL_MULK, 1, 4),
                                                           (AL_MULK, 7, 10)]

    async def test_removal_is_confined_to_one_surah_and_one_user(self):
        hifz = await _hifz()
        await hifz.add_interval(USER, AL_MULK, 1, 10)
        await hifz.add_interval(USER, YASIN, 1, 10)
        await hifz.add_interval(USER + 1, AL_MULK, 1, 10)
        await hifz.remove_range(USER, AL_MULK, 1, 10)
        assert _spans(await hifz.list_intervals(USER)) == [(YASIN, 1, 10)]
        assert _spans(await hifz.list_intervals(USER + 1)) == [(AL_MULK, 1, 10)]

    async def test_ayah_zero_is_rejected(self):
        hifz = await _hifz()
        await hifz.add_interval(USER, AL_MULK, 1, 10)
        with pytest.raises(ValueError):
            await hifz.remove_range(USER, AL_MULK, 0, 5)
        assert _spans(await hifz.list_intervals(USER)) == [(AL_MULK, 1, 10)]


# --- Exhaustive: every relative position of two spans ---------------------------
#
# Six ayahs is enough for two spans to be disjoint-left, abutting, overlapping,
# containing, contained, identical, abutting-right and disjoint-right, plus every
# asymmetric variant — 441 ordered pairs, all of them checked against the only
# definition that is not itself the implementation: sets of ayahs.

_UNIVERSE = range(1, 7)
_ALL_SPANS = [(start, end) for start in _UNIVERSE for end in _UNIVERSE if start <= end]


class TestEveryRelativePosition:
    @pytest.mark.parametrize("first", _ALL_SPANS)
    async def test_two_marks_equal_the_union(self, first):
        hifz = await _hifz()
        for second in _ALL_SPANS:
            await hifz.remove_range(USER, AL_MULK, 1, 30)
            await hifz.add_interval(USER, AL_MULK, *first)
            await hifz.add_interval(USER, AL_MULK, *second)
            intervals = await hifz.list_intervals(USER)
            expected = {(AL_MULK, a) for a in range(first[0], first[1] + 1)}
            expected |= {(AL_MULK, a) for a in range(second[0], second[1] + 1)}
            assert _ayahs(intervals) == expected, "%r then %r" % (first, second)
            _assert_invariant(intervals)

    @pytest.mark.parametrize("marked", _ALL_SPANS)
    async def test_a_mark_then_a_removal_equals_the_difference(self, marked):
        hifz = await _hifz()
        for removed in _ALL_SPANS:
            await hifz.remove_range(USER, AL_MULK, 1, 30)
            await hifz.add_interval(USER, AL_MULK, *marked)
            await hifz.remove_range(USER, AL_MULK, *removed)
            intervals = await hifz.list_intervals(USER)
            expected = {(AL_MULK, a) for a in range(marked[0], marked[1] + 1)}
            expected -= {(AL_MULK, a) for a in range(removed[0], removed[1] + 1)}
            assert _ayahs(intervals) == expected, "%r minus %r" % (marked, removed)
            _assert_invariant(intervals)


# --- The property test ---------------------------------------------------------

@pytest.mark.parametrize("seed", [1, 2, 3, 5, 8, 13, 21, 34])
async def test_any_sequence_of_marks_and_removals_keeps_the_invariant(seed):
    """A long random walk of add/remove, checked against a set of ayahs.

    This is worth more than any number of hand-picked cases: the hand-picked ones
    only cover the shapes someone thought of, and the failure mode that would hurt
    (a `/progress` that drifts a percent at a time) comes from a shape nobody
    thought of. The model is a `set` of (surah, ayah) — the definition of "what
    the user knows" with no interval arithmetic in it at all, so the two can only
    agree if the arithmetic is right.

    Seeded, so a failure is reproducible from the parameter id alone. The spans
    are deliberately small relative to the surahs, because that is what produces
    the interesting mix of abutment, one-ayah gaps and multi-interval spans.
    """
    rng = random.Random(seed)
    hifz = await _hifz()
    known = set()

    for _ in range(200):
        surah = rng.choice((AL_MULK, YASIN))
        start = rng.randint(1, 24)
        end = min(start + rng.randint(0, 6), 30)
        touched = {(surah, a) for a in range(start, end + 1)}

        if rng.random() < 0.62:
            await hifz.add_interval(USER, surah, start, end)
            known |= touched
        else:
            await hifz.remove_range(USER, surah, start, end)
            known -= touched

        intervals = await hifz.list_intervals(USER)
        _assert_invariant(intervals)
        assert _ayahs(intervals) == known
        assert await hifz.count_ayahs(USER) == len(known)
        assert await hifz.count_ayahs(USER, surah=AL_MULK) == len(
            [a for s, a in known if s == AL_MULK])


@pytest.mark.parametrize("seed", [7, 42])
async def test_a_random_walk_never_leaks_across_users(seed):
    """Two users driven by the same loop stay completely independent.

    Cheap to get wrong (one missing `user_id` in a WHERE clause) and impossible to
    notice in production until someone's percentage jumps.
    """
    rng = random.Random(seed)
    hifz = await _hifz()
    known = {1: set(), 2: set()}

    for _ in range(150):
        user = rng.choice((1, 2))
        start = rng.randint(1, 25)
        end = min(start + rng.randint(0, 5), 30)
        touched = {(AL_MULK, a) for a in range(start, end + 1)}
        if rng.random() < 0.6:
            await hifz.add_interval(user, AL_MULK, start, end)
            known[user] |= touched
        else:
            await hifz.remove_range(user, AL_MULK, start, end)
            known[user] -= touched

    for user in (1, 2):
        intervals = await hifz.list_intervals(user)
        _assert_invariant(intervals)
        assert _ayahs(intervals) == known[user]


async def test_intervals_from_many_surahs_come_back_in_mushaf_order():
    """`list_intervals` orders by (surah, start_ayah) — what `/progress` renders."""
    hifz = await _hifz()
    for surah in (114, 1, 67, 36, 2):
        await hifz.add_interval(USER, surah, 3, 5)
        await hifz.add_interval(USER, surah, 1, 1)
    intervals = await hifz.list_intervals(USER)
    assert _spans(intervals) == [
        (1, 1, 1), (1, 3, 5),
        (2, 1, 1), (2, 3, 5),
        (36, 1, 1), (36, 3, 5),
        (67, 1, 1), (67, 3, 5),
        (114, 1, 1), (114, 3, 5),
    ]
    _assert_invariant(intervals)
