"""Uzbek Latin <-> Cyrillic transliteration for text we write ourselves (tajweed lessons).

`to_cyrillic` is the reverse of the Cyrillic->Latin converter that derives the bundled
Latin translation (scripts/bundle_translations.py), and `to_latin` mirrors that one so a
round trip can be tested. Input is the standard Latin orthography: oʻ / gʻ with U+02BB
(the ASCII ' and ‘ are accepted too), ʼ (U+02BC) for the tutuq belgisi.

The ambiguous cases follow the usual rules: "e" is э at the start of a word and е
elsewhere; "ye" at the start of a word or after a vowel is е; "yo / yu / ya" are ё / ю / я;
"sh / ch" are ш / ч (write sʼh to keep s and h apart, as in Isʼhoq). Words where these
rules give the wrong letter go in EXCEPTIONS.
"""

import re

_LAT_TO_CYR = {
    "a": "а", "b": "б", "d": "д", "e": "е", "f": "ф", "g": "г", "h": "ҳ", "i": "и",
    "j": "ж", "k": "к", "l": "л", "m": "м", "n": "н", "o": "о", "p": "п", "q": "қ",
    "r": "р", "s": "с", "t": "т", "u": "у", "v": "в", "x": "х", "y": "й", "z": "з",
}  # fmt: skip
_DIGRAPHS = {"oʻ": "ў", "gʻ": "ғ", "sh": "ш", "ch": "ч", "yo": "ё", "yu": "ю", "ya": "я"}
_VOWELS = set("aeiouʻ")  # ʻ: after oʻ the previous sound is a vowel
_APOSTROPHES = str.maketrans({"'": "ʻ", "‘": "ʻ", "’": "ʼ"})

# Whole words the rules above get wrong, Latin (lowercase) -> Cyrillic.
EXCEPTIONS = {
    "sentabr": "сентябрь",
    "oktabr": "октябрь",
}

_CYR_TO_LAT = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "ё": "yo", "ж": "j", "з": "z",
    "и": "i", "й": "y", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o", "п": "p",
    "р": "r", "с": "s", "т": "t", "у": "u", "ф": "f", "х": "x", "ц": "ts", "ч": "ch",
    "ш": "sh", "ъ": "ʼ", "ь": "", "э": "e", "ю": "yu", "я": "ya", "ў": "oʻ", "қ": "q",
    "ғ": "gʻ", "ҳ": "h",
}  # fmt: skip
_CYR_VOWELS = set("аоуэиўеёюя")

_WORD = re.compile(r"[A-Za-zʻʼ'‘’]+")


def _case(src: str, out: str) -> str:
    if src.isupper() and len(src) > 1:
        return out.upper()
    if src[:1].isupper():
        return out[:1].upper() + out[1:]
    return out


def _word_to_cyr(word: str) -> str:
    low = word.lower().translate(_APOSTROPHES)
    if low in EXCEPTIONS:
        return _case(word, EXCEPTIONS[low])
    out, i = [], 0
    while i < len(low):
        pair = low[i : i + 2]
        prev = low[i - 1] if i else ""
        if pair == "ye" and (i == 0 or prev in _VOWELS):
            out.append("е")
            i += 2
        elif pair == "yo" and low[i + 2 : i + 3] == "ʻ":
            out.append("й")  # y + oʻ (yoʻl -> йўл), not yo + ʻ
            i += 1
        elif pair in _DIGRAPHS:
            out.append(_DIGRAPHS[pair])
            i += 2
        elif low[i] == "e" and i == 0:
            out.append("э")
            i += 1
        elif low[i] == "ʼ":
            out.append("ъ")
            i += 1
        else:
            out.append(_LAT_TO_CYR.get(low[i], low[i]))
            i += 1
    return _case(word, "".join(out))


# HTML tags, entities, /commands and {placeholders} stay as they are
_MARKUP = re.compile(r"(<[^>]*>|&[#\w]+;|/[A-Za-z_]+|\{\w*\})")


def to_cyrillic(text: str) -> str:
    """Uzbek Latin -> Cyrillic, word by word; HTML markup and non-words pass through."""
    parts = _MARKUP.split(text)
    return "".join(
        part if i % 2 else _WORD.sub(lambda m: _word_to_cyr(m.group(0)), part)
        for i, part in enumerate(parts)
    )


def to_latin(text: str) -> str:
    """Uzbek Cyrillic -> Latin (the same rules as scripts/bundle_translations.py)."""
    out = []
    for i, ch in enumerate(text):
        low = ch.lower()
        if low == "е":
            prev = text[i - 1].lower() if i else ""
            mapped = "ye" if (prev not in _CYR_TO_LAT or prev in _CYR_VOWELS) else "e"
        else:
            mapped = _CYR_TO_LAT.get(low)
        if mapped is None:
            out.append(ch)
            continue
        if ch != low and mapped:
            # in an all-caps word a digraph is all caps too (ЎҚИШ -> OʻQISH)
            nxt = text[i + 1] if i + 1 < len(text) else ""
            prv = text[i - 1] if i else ""
            caps = nxt.isupper() or (not nxt.isalpha() and prv.isupper())
            mapped = mapped.upper() if caps else mapped[0].upper() + mapped[1:]
        out.append(mapped)
    return "".join(out)
