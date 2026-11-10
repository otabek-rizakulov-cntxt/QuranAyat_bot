"""Spaced-repetition cards for the tajweed course (docs/TAJWEED_PLAN.md P4).

The deck is built from the lessons, and a card is in a user's deck once any lesson
that teaches it is done (✅ Oʻqidim). Four kinds:

    L:<letter>        a letter (its forms) -> its name and articulation group
    H:<sign>          a haraka or sign (shadda, tanwin, ...) -> its name and reading
    R:<rule> / RR:<rule>  rule name -> a marked example ayah, and the reverse
    W:<s>:<a>:<n>     word n of an ayah -> hear it (the user's reciter)

Only standard names and groupings are stated here, nothing that needs a scholar's
wording; examples come from the annotated text. Scheduling lives in services.tajweed.
"""

from typing import Dict, FrozenSet, List, NamedTuple, Optional, Tuple

from domain import tajweed, tajweed_lessons, tajweed_practice


class Card(NamedTuple):
    id: str
    kind: str  # letter | sign | rule | rule_back | word
    front: str  # HTML-safe text (Arabic or Uzbek Latin), may hold <u><b>
    back: str  # Uzbek Latin, may hold <u><b> / Arabic
    ayah: Optional[Tuple[int, int]]  # an ayah to play on the back
    lessons: FrozenSet[str]  # any of these done -> the card is unlocked


# --- letters --------------------------------------------------------------------

_THROAT, _TONGUE, _LIPS = "ءهعحغخ", "قكجشيضلنرطدتصزسظذث", "فوبم"
GROUPS = {
    "throat": "Tomoq (halq) harfi",
    "tongue": "Til (lison) harfi",
    "lips": "Lab (shafatayn) harfi",
    "jawf": "Ogʻiz boʻshligʻi (javf): mad harfi",
}
_NON_JOINING = set("اأإآدذرزوؤ")


def _group(letter: str) -> str:
    if letter == "ا":
        return "jawf"
    if letter in _THROAT:
        return "throat"
    if letter in _LIPS:
        return "lips"
    return "tongue"


def _forms(letter: str) -> str:
    """The letter alone and joined: isolated, initial, medial, final."""
    if letter in _NON_JOINING:
        return "%s  ـ%s" % (letter, letter)
    return "%s  %sـ  ـ%sـ  ـ%s" % (letter, letter, letter, letter)


def _letter_names() -> Dict[str, str]:
    """Each letter's name as the book's lesson titles give it (Alif, Ro, Za, ...)."""
    names = {}
    for x in tajweed_lessons.audio_lessons():
        if 2 <= x.n <= 29:
            names[tajweed_practice.LETTERS[x.n - 2]] = x.title.replace(" harfi", "")
    return names


# --- signs (harakat and spelling) -----------------------------------------------------

SIGNS: Dict[str, Tuple[str, str]] = {  # id -> (front, back)
    "harakat": ("بَ  بِ  بُ", "Fatha, kasra, zamma: ba, bi, bu"),
    "sukun": ("اَبْ", "Sukun: harf harakatsiz oʻqiladi — ab"),
    "madd": ("بَا  بِي  بُو", "Madli harflar: ovoz choʻziladi — baa, bii, buu"),
    "shadda": ("رَبَّ", "Tashdid: harf ikki marta — rab-ba"),
    "tanwin": ("بًا  بٍ  بٌ", "Tanvin: oxiriga «n» qoʻshiladi — ban, bin, bun"),
    "shadda_tanwin": ("رَبًّا", "Tashdid va tanvin birga — rab-ban"),
    "hamza": ("أَ  إِ  أُ  ء", "Hamza: tomoqdan qisqa toʻxtash bilan — a, i, u"),
    "ta_marbuta": ("ـة", "Ta marbuta: davom ettirilsa «t», toʻxtalsa «h»"),
    "dagger_alif": ("ٱلرَّحْمَٰنِ", "Yozilmagan alif (ٰ): yozilmasa ham choʻziladi — rahmaan"),
    "small_ya": ("بِهِۦ", "Kichik yo (ۦ): «i» choʻziladi — bihii"),
    "small_waw": ("لَهُۥ", "Kichik vov (ۥ): «u» choʻziladi — lahuu"),
    "alif_maqsura": ("عَلَى", "Alifi maqsura (ى): «a» kabi choʻziladi — alaa"),
    "waw_alif": ("ٱلصَّلَوٰةَ", "Vovi alifiya: vov «a» kabi oʻqiladi — as-salaata"),
}
# Which lessons teach each sign (Muallimi soniy numbers, or rules-track ids).
_SIGN_LESSONS: Dict[str, Tuple] = {
    "harakat": (2, "harakatlar"),
    "sukun": (3, "harakatlar"),
    "madd": (30,),
    "shadda": (31, "tashdid"),
    "tanwin": (32, "tanvin"),
    "shadda_tanwin": (33,),
    "hamza": (34,),
    "ta_marbuta": (35,),
    "dagger_alif": (36,),
    "small_ya": (37,),
    "small_waw": (38,),
    "alif_maqsura": (39,),
    "waw_alif": (40,),
}
# Rules-track lessons that teach a group of letters.
_GROUP_LESSONS = {"throat": "maxraj-bogiz", "tongue": "maxraj-til", "lips": "maxraj-lab"}
WORDS_PER_LESSON = 3


def _ms(n: int) -> str:
    return "ms-%03d" % n


def _lesson_ids(spec) -> FrozenSet[str]:
    return frozenset(_ms(x) if isinstance(x, int) else x for x in spec)


_deck: Optional[Dict[str, Card]] = None


def deck() -> Dict[str, Card]:
    """Every card, by id, in teaching order."""
    global _deck
    if _deck is not None:
        return _deck
    cards: Dict[str, Card] = {}
    names = _letter_names()

    for i, letter in enumerate(tajweed_practice.LETTERS):
        group = _group(letter)
        lessons = {_ms(i + 2)}
        if group in _GROUP_LESSONS:
            lessons.add(_GROUP_LESSONS[group])
        back = "<b>%s</b>\n%s" % (names.get(letter, letter), GROUPS[group])
        cards["L:" + letter] = Card(
            "L:" + letter, "letter", _forms(letter), back, None, frozenset(lessons)
        )

    for sign, (front, back) in SIGNS.items():
        cards["H:" + sign] = Card(
            "H:" + sign, "sign", front, back, None, _lesson_ids(_SIGN_LESSONS[sign])
        )

    by_rule: Dict[str, set] = {}
    for x in tajweed_lessons.audio_lessons():
        for r in tajweed_practice.AUDIO_RULES.get(x.n, ()):
            by_rule.setdefault(r, set()).add(x.id)
    for x in tajweed_lessons.lessons():
        for r in x.rules:
            by_rule.setdefault(r, set()).add(x.id)
    for rule in tajweed.RULES:
        if rule not in by_rule or not tajweed.examples(rule, 1):
            continue
        s, a = tajweed.examples(rule, 1)[0]
        marked = tajweed.marked_html(s, a, [rule])
        name = tajweed.RULES[rule].name_uz
        lessons = frozenset(by_rule[rule])
        cards["R:" + rule] = Card(
            "R:" + rule, "rule", name, "%s\n(%d:%d)" % (marked, s, a), (s, a), lessons
        )
        cards["RR:" + rule] = Card(
            "RR:" + rule, "rule_back", "%s\n(%d:%d)" % (marked, s, a), name, (s, a), lessons
        )

    for lesson_id in [x.id for x in tajweed_lessons.audio_lessons()] + [
        x.id for x in tajweed_lessons.lessons()
    ]:
        for d in tajweed_practice.drill(lesson_id, 1, WORDS_PER_LESSON):
            position = tajweed.text(d.surah, d.ayah).split(" ").index(d.word)
            card_id = "W:%d:%d:%d" % (d.surah, d.ayah, position)
            if card_id in cards:  # the same word drawn for two lessons: keep the first
                continue
            cards[card_id] = Card(
                card_id,
                "word",
                d.word,
                "(%d:%d)" % (d.surah, d.ayah),
                (d.surah, d.ayah),
                frozenset({lesson_id}),
            )
    _deck = cards
    return cards


def card(card_id: str) -> Optional[Card]:
    return deck().get(card_id)


def unlocked(done: set) -> List[Card]:
    """The cards a user with these lessons done may study, in teaching order."""
    return [c for c in deck().values() if c.lessons & done]


def reset_for_tests() -> None:
    global _deck
    _deck = None
