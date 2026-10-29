# Progress operations (spec items C2-C3): the derived summary and /forgot.
# Used by hifz/progress.py and the Mini App's /progress routes.

from typing import List, Tuple

from hifz.refs import Ref
from modules import Quran


def surah_spans(ref: Ref) -> List[Tuple[int, int, int]]:
    """`ref` split into one (surah, start_ayah, end_ayah) triple per surah.

    `store.hifz.remove_range` is per-surah — an interval never crosses a surah
    boundary — while a reference happily does ("/forgot 67:30-68:2", and every
    juz). Splitting here keeps that arithmetic in one place.
    """
    spans = []
    for surah in range(ref.start_surah, ref.end_surah + 1):
        start = ref.start_ayah if surah == ref.start_surah else 1
        end = ref.end_ayah if surah == ref.end_surah else Quran.get_surah_length(surah)
        if start <= end:
            spans.append((surah, start, end))
    return spans


async def unmark(store, user_id: int, ref: Ref) -> bool:
    """Unmark everything `ref` covers. True if anything was actually memorized.

    The intervals are read once first, so a juz-wide `/forgot` costs one read plus
    a write per surah the user has actually touched — not 37 writes — and so the
    answer to "was any of this marked?" is known without a second count.
    `remove_range` returning [] is not that answer: it also means "the interval
    was erased whole".
    """
    intervals = await store.hifz.list_intervals(user_id)
    removed = False
    for surah, start, end in surah_spans(ref):
        if not any(
            row.surah == surah and row.start_ayah <= end and row.end_ayah >= start
            for row in intervals
        ):
            continue
        await store.hifz.remove_range(user_id, surah, start, end)
        removed = True
    return removed
