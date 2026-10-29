# The reciter catalog (src/common/performers.json): order, kinds and the
# per-kind warnings. Shared by the bot's /reciter picker (main.py) and the Mini
# App's GET /catalog/reciters.

from lib.utils import File


# A curated shortlist of well-known reciters (subfolder keys into performers.json).
# These lead the catalog, so the first page of the picker is the ten names most
# people are looking for and the pager walks through everything else.
_RECITER_SHORTLIST = (
    "Husary_128kbps",
    "Alafasy_128kbps",
    "Abdurrahmaan_As-Sudais_192kbps",
    "Abdul_Basit_Murattal_192kbps",
    "Minshawy_Murattal_128kbps",
    "Saood_ash-Shuraym_128kbps",
    "MaherAlMuaiqly128kbps",
    "Yasser_Ad-Dussary_128kbps",
    "Hudhaify_128kbps",
    "Ghamadi_40kbps",
)


# The catalog holds three genuinely different kinds of recording, and conflating them
# is a correctness problem, not a cosmetic one: a riwayah is a *different reading of
# the text* (so the audio stops matching the Arabic on screen), and a "translation"
# entry is not recitation at all but someone reading the translated meaning aloud.
# The picker therefore groups by kind and says so on the tab. Recitation leads.
RECITER_KINDS = ("recitation", "riwayah", "translation")
DEFAULT_RECITER_KIND = RECITER_KINDS[0]

# What to warn about when the chosen entry is not ordinary Arabic recitation. A
# riwayah *is* recitation — just a different reading of the text from the one shown
# on screen — so the two cases cannot share a message.
_KIND_WARNING_KEYS = {
    "riwayah": "riwayah_warning",
    "translation": "translation_audio_warning",
}


def reciter_catalog() -> list:
    """Every reciter in src/common/performers.json, shortlist first then the rest in
    catalog order — the order the picker pages through."""
    performers = File._load_performers()
    by_subfolder = {p["subfolder"]: p for p in performers}
    # a shortlist entry the catalog no longer has is skipped, not fatal
    ordered = [by_subfolder[s] for s in _RECITER_SHORTLIST if s in by_subfolder]
    shortlisted = set(_RECITER_SHORTLIST)
    ordered.extend(p for p in performers if p["subfolder"] not in shortlisted)
    return ordered


def reciter_kind(subfolder: str) -> str:
    """Which group `subfolder` belongs to, defaulting to plain recitation for an
    entry with no `kind` (or a stale saved preference no longer in the catalog)."""
    match = next((p for p in File._load_performers() if p["subfolder"] == subfolder), None)
    if match is None:
        return DEFAULT_RECITER_KIND
    return match.get("kind", DEFAULT_RECITER_KIND)


def reciter_group(kind: str) -> list:
    """The catalog entries of one kind, in the catalog's own order."""
    return [p for p in reciter_catalog() if p.get("kind", DEFAULT_RECITER_KIND) == kind]
