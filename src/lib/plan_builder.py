# The plan generator: a target plus a pace plus a set of weekdays, turned into
# the exact list of daily portions the user will be pushed.
#
# Two properties are load-bearing and everything here is shaped around them.
#
# **It is pure.** No store, no clock, no I/O — a target, a pace, a weekday set
# and a start date in, a list of portions out. The wizard (D1) renders the
# preview calendar from the return value and then writes that same list through
# `store.plans.create_plan`, so "the preview matches what is later pushed, day
# for day" is not a discipline anyone has to maintain: it is the same function
# call. It also means a stored plan's drill kinds can be re-derived at any time
# by calling `build_plan` again with the plan's own columns, which is how the
# scheduler knows a given `plan_day` row is a consolidation day even though the
# table has no column for it.
#
# **Every portion lives inside one surah.** `PlanDaySpec` — and the `plan_day`
# table under it — is (surah, start_ayah, end_ayah), single-surah by
# construction, and D3 sends a portion as one stitched recitation. Rather than
# split a cross-surah portion into two rows on one date (two drills, two audios,
# one confusing day), the generator simply never emits one: an advancing day
# stops at the end of its surah, and a consolidation over a page that straddles
# a surah boundary is clamped to the surah the page ended in. Cross-surah
# *targets* — a juz, or a `range` written "67:1-68:5" — work fine; it is the
# daily portions that stay within a surah. So no schema change is needed.
#
# The drill unit widens as ground is covered: range -> mushaf page -> whole
# surah. That progression is the generator's job, not the user's, so it appears
# here as extra days interleaved into the calendar (see `_consolidations`).

from dataclasses import dataclass
from datetime import date, timedelta
from typing import List, Optional, Sequence, Tuple

from hifz.refs import KIND_RANGE, Ref
from modules import Quran

__all__ = [
    "AUTO_PACE", "DRILL_RANGE", "DRILL_PAGE", "DRILL_SURAH",
    "CONSOLIDATION_DRILLS", "AUTO_PACE_PAGE_FRACTION",
    "Portion", "auto_pace", "build_plan",
    "to_day_specs", "advancing", "next_scheduled_date",
]

# `plan.pace = 0` is the wizard's "let the bot decide" — see `auto_pace`.
AUTO_PACE = 0

# What a day drills. `DRILL_RANGE` advances into new ground; the other two are
# consolidation days that re-drill ground already covered.
DRILL_RANGE = "range"    # the day's new portion
DRILL_PAGE = "page"      # the mushaf page just finished
DRILL_SURAH = "surah"    # the surah just finished

CONSOLIDATION_DRILLS = (DRILL_PAGE, DRILL_SURAH)

# Auto pace aims at a fifth of a mushaf page a day — about three lines of the
# standard 15-line Madani mushaf. See `auto_pace` for why the unit is the page.
AUTO_PACE_PAGE_FRACTION = 0.2

_Pos = Tuple[int, int]


@dataclass(frozen=True)
class Portion:
    """One day of a plan: exactly a `PlanDaySpec`, plus the two things the
    `plan_day` table has no column for.

    `drill` says whether the day advances into new ground (`DRILL_RANGE`) or
    consolidates ground already covered (`DRILL_PAGE`, `DRILL_SURAH`), and
    `unit` carries the page or surah number that consolidation is over — which
    is what lets the preview calendar label "Page 562" differently from
    "67:11-12" instead of showing the user two indistinguishable rows.
    """

    scheduled_date: date
    surah: int
    start_ayah: int
    end_ayah: int
    drill: str = DRILL_RANGE
    unit: Optional[int] = None

    @property
    def is_consolidation(self) -> bool:
        """Whether this day re-drills covered ground rather than advancing."""
        return self.drill in CONSOLIDATION_DRILLS

    @property
    def ayahs(self) -> int:
        """How many ayahs the day covers."""
        return self.end_ayah - self.start_ayah + 1

    def as_ref(self) -> Ref:
        """The day's span as a `Ref`, for `format_ref` and the drill senders.

        Always `KIND_RANGE`, even on a consolidation day: a page drill is
        clamped to the target and to its surah, so calling the result a "page"
        ref would claim a span it may not actually be. The page number lives in
        `unit`, where it cannot be mistaken for the span itself.
        """
        return Ref(KIND_RANGE, self.surah, self.start_ayah,
                   self.surah, self.end_ayah)


def next_scheduled_date(start: date, days_of_week: Sequence[int]) -> date:
    """The first date on or after `start` that falls on an included weekday.

    `days_of_week` is 1=Mon … 7=Sun, matching `plan.days_of_week` and
    `date.isoweekday()`. A plan set up on a Saturday for weekdays therefore
    begins on the Monday, not on a day the user said they were unavailable.
    """
    allowed = _validated_days(days_of_week)
    day = start
    for _ in range(7):
        if day.isoweekday() in allowed:
            return day
        day += timedelta(days=1)
    raise ValueError("unreachable: every weekday checked")  # pragma: no cover


def auto_pace(target: Ref) -> int:
    """Ayahs per day for `pace = AUTO_PACE`, from the target's own density.

    Ayah *count* is a terrible unit for pacing hifz: an ayah of al-Baqarah can
    be fifty times the length of an ayah of an-Naba'. The mushaf page is the
    unit huffaz actually use ("a page a day", "half a page a day") precisely
    because a page is a fixed amount of text however the ayahs fall on it.

    So the heuristic works in pages and converts back: measure the target's
    density (ayahs per mushaf page it spans), take `AUTO_PACE_PAGE_FRACTION` of
    it — a fifth of a page, roughly three lines — and round half up. The result
    is at least one ayah and never more than the whole target.

    It lands where a teacher would: al-Mulk 2/day (15 days), Ya-Sin 3/day,
    juz 30 5/day, al-Baqarah 1/day, and a four-ayah surah 1/day.
    """
    total = target.count()
    if total <= 0:
        return 1
    pages = Quran.page_of(*target.end) - Quran.page_of(*target.start) + 1
    density = total / max(1, pages)
    pace = int(density * AUTO_PACE_PAGE_FRACTION + 0.5)
    return max(1, min(pace, total))


def build_plan(target: Ref, pace: int, days_of_week: Sequence[int],
               start_date: date) -> List[Portion]:
    """Materialize `target` into the daily portions of a plan.

    `pace` is ayahs per advancing day, or `AUTO_PACE` (0) to let `auto_pace`
    pick one. `days_of_week` is 1=Mon … 7=Sun; the plan starts on the first
    included day on or after `start_date` and uses only included days
    thereafter. Nothing is ever split mid-ayah — every portion is a whole
    number of whole ayahs — and the last advancing day ends exactly on
    `target.end`, short rather than overshooting.

    Consolidation days are interleaved (see `_consolidations`), so the returned
    list is longer than the number of advancing days. It is ordered by date,
    one portion per date, and is the exact preview calendar: pass it through
    `to_day_specs` to store it.
    """
    allowed = _validated_days(days_of_week)
    total = target.count()
    if total <= 0:
        raise ValueError("empty target: %r" % (target,))

    step = auto_pace(target) if pace is None or pace <= 0 else int(pace)
    step = max(1, min(step, total))

    portions: List[Portion] = []
    day = next_scheduled_date(start_date, allowed)
    cursor: _Pos = target.start

    while True:
        surah, first = cursor
        # Stop at whichever comes first: the pace, the end of the surah, the
        # end of the target. The surah bound is what keeps a portion — and so a
        # `plan_day` row — inside one surah.
        last = min(first + step - 1, Quran.get_surah_length(surah))
        if surah == target.end_surah:
            last = min(last, target.end_ayah)
        portions.append(Portion(day, surah, first, last))
        day = _advance(day, allowed)

        for start, end, drill, unit in _consolidations(target, surah, first, last):
            portions.append(Portion(day, surah, start, end, drill, unit))
            day = _advance(day, allowed)

        # Tested here rather than in the `while`, because `get_next_ayah` wraps
        # 114:6 round to 1:1 — a juz-30 target would otherwise never terminate.
        if (surah, last) >= target.end:
            return portions
        cursor = Quran.get_next_ayah(surah, last)


def _consolidations(target: Ref, surah: int, first: int, last: int):
    """The consolidation days that follow an advancing portion, widening.

    The ladder is range -> mushaf page -> whole surah, and a rung is only
    climbed when the day just drilled *finished* that unit: a page drill lands
    on the day whose portion ends on the last ayah of a mushaf page, a surah
    drill on the day whose portion ends on the last ayah of a surah. Both fire
    on the same day when a surah and a page end together.

    Each span is clamped to the target (and the page also to `surah`, so a page
    straddling a surah boundary still yields a single-surah row). A rung is
    skipped when clamping leaves it no wider than the rung below — otherwise a
    four-ayah surah done in one day would be followed by a day re-drilling the
    identical four ayahs, and a plan starting mid-page would get a page day
    that is just yesterday again.

    Yields `(start_ayah, end_ayah, drill, unit)`, all within `surah`.
    """
    lower = first                      # widest rung emitted so far
    floor = target.start_ayah if target.start_surah == surah else 1

    page = Quran.page_of(surah, last)
    page_span = Quran.page_range(page)
    if page_span is not None and (page_span[2], page_span[3]) == (surah, last):
        start = max(page_span[1] if page_span[0] == surah else 1, floor)
        if start < lower:
            yield start, last, DRILL_PAGE, page
            lower = start

    if last == Quran.get_surah_length(surah) and floor < lower:
        yield floor, last, DRILL_SURAH, surah


def to_day_specs(portions: Sequence[Portion]) -> list:
    """`Portion`s as `PlanDaySpec`s, ready for `store.plans.create_plan`.

    The store type is imported here rather than at module scope so that
    importing the generator stays free of the repository layer (and of
    asyncpg): the preview path needs the arithmetic, not a database.
    """
    from lib.store.plans import PlanDaySpec
    return [PlanDaySpec(p.scheduled_date, p.surah, p.start_ayah, p.end_ayah)
            for p in portions]


def advancing(portions: Sequence[Portion]) -> List[Portion]:
    """Only the days that cover new ground — the plan's actual progress."""
    return [p for p in portions if not p.is_consolidation]


def _validated_days(days_of_week: Sequence[int]) -> frozenset:
    """`days_of_week` as a validated 1..7 set. Raises on empty or out of range.

    A plan with no available day cannot be materialized at all, so this is a
    programming error rather than something to paper over with a default.
    """
    days = frozenset(int(d) for d in (days_of_week or ()))
    if not days:
        raise ValueError("days_of_week is empty")
    if not days <= frozenset(range(1, 8)):
        raise ValueError("days_of_week must be 1=Mon..7=Sun: %r" % (days_of_week,))
    return days


def _advance(day: date, allowed: frozenset) -> date:
    """The next scheduled date strictly after `day`."""
    return next_scheduled_date(day + timedelta(days=1), allowed)
