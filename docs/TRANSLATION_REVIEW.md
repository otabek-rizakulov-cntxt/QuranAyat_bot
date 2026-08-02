# Native-speaker review — hifz platform strings

**Status:** not started · **Scope:** 111 keys × 47 non-English UI locales
**Last updated:** 2026-08-02

---

## 0. Why this exists

`docs/HIFZ_PLATFORM.md` §8 flags this as open work: ~5,200 machine-translated
strings across 47 locales, in languages nobody on this project reads. This
document is the process for closing that gap — it does not close the gap
itself. Reviewing translation quality needs a native speaker per language;
that is staffing, not engineering, and nothing here should be read as having
done that review.

**Correction to the record.** `docs/HIFZ_PLATFORM.md` states "each translating
agent was asked to name the keys it was unsure of; that list is the starting
point for a native-speaker review." That list does not exist. Every
`i18n`/`feat(locale)` commit touching `src/locales/*.py` was checked (`git log
--all -- 'src/locales/*.py'`, `git log -1 --format=%B` on each) — the two
batch commits (`05086af`, `6d3b507`) describe translation *decisions*
(pluralization phrasing, Uzbek Latin/Cyrillic derivation, percent-sign
placement) but name no per-key uncertainty, and no other commit or file
records one either. Whatever prompted that sentence in the spec did not leave
a retrievable trace. **Treat this as a first-pass review of all 111 keys in
every locale, not a triage of a pre-flagged subset.**

## 1. What a reviewer needs

- `docs/HIFZ_STRINGS.md` — the frozen manifest: all 111 keys, their
  placeholders, and where each is shown in the product. Open it side by side
  with the locale file; it is the context a translator had when the string
  was written.
- `src/locales/<code>.py` — the target locale's string table.
- `src/locales/en.py` — the English original, for meaning comparison (search
  the `# --- Hifz platform ---` block).

Mechanical correctness — placeholder names matching English byte-for-byte, no
empty values, no HTML tags in hifz keys, `/start` advertising every command —
is already enforced by `scripts/check_locales.py` and does not need a human
to re-check it. A review is about what that script cannot see:

- **Meaning.** Does the string say what the English says, not just something
  plausible in the target language?
- **Register.** This is a religious memorization companion, not a chat app —
  tone should match the devotional phrasing of `en.py` (e.g.
  `plan_complete`'s "May Allah accept it from you"), not read as generic
  software copy.
- **Grammatical number.** `{n}` (streak days, ranks) arrives as a bare integer
  with no ICU/gettext plural support — just `str.format`. Slavic three-way
  agreement, Arabic's five plural forms, etc. cannot be resolved at runtime.
  Confirm the phrasing was built to stay correct at any value (the pattern
  `05086af` used for Russian: "Текущая серия, дней: {n}") rather than
  mirroring English's singular/plural split, which reads as broken at 2, 5,
  11, and similar values in the target language.
- **Script direction and rendering.** For `ar`, `ur`, `fa`, `ps`, `sd`, `dv`
  (all RTL): does a placeholder in the middle of a sentence (`{name}`,
  `{pct}`, `{time}`) still read correctly, particularly where it is adjacent
  to Latin-script content (dates, percentages)?
  - `translit`/transliterated readers are not a UI locale — no review needed.
  - Uzbek Latin/Cyrillic are a transliterated pair by design, not
    independent translations (see `05086af`) — reviewing one and confirming
    the other matches is enough; they are not two independent review targets.
- **Button length.** `btn_*` values should stay short enough not to wrap on
  a phone keyboard row — `day_mon` … `day_sun` sit side by side in one row.

## 2. Process

1. Pick a locale from the table below (any order — see note on
   prioritization).
2. Read every hifz key's value in `src/locales/<code>.py` against
   `docs/HIFZ_STRINGS.md`'s description of where and how it is used.
3. Record findings directly against that key — wrong meaning, awkward
   register, a plural that breaks at some value, an RTL rendering problem —
   as a comment or note wherever the team already tracks this kind of issue
   (a GitHub issue per locale is the natural fit if none exists yet; this
   file is not meant to hold prose per finding).
4. Fix in `src/locales/<code>.py` directly for small corrections; flag
   larger disagreements (e.g. "this whole section reads unnaturally") for a
   second opinion rather than one reviewer relitigating tone alone.
5. Update the row below: reviewer, date, status, and a link to wherever the
   findings were recorded (or "no issues found").
6. Re-run `python3 scripts/check_locales.py` if any value changed — it still
   only catches mechanics, not the things this review is for, but a typo'd
   placeholder during a fix is exactly the kind of thing it exists to catch.

**On prioritization.** There is no usage/analytics data behind any of the 47
locales to rank them by impact, so this table is ordered the way
`src/locales/languages.py` already orders `LANGUAGES` — Central Asia (the
bot's stated primary audience) first, then grouped by region. That is an
existing, deliberate ordering already in the codebase, reused here rather
than invented fresh; there is no other principled ranking available.

## 3. Locales

| Locale | Language | Status | Reviewer | Findings |
|---|---|---|---|---|
| ar | العربية (Arabic) | not started | | |
| ru | Русский (Russian) | not started | | |
| uz-Cyrl | Ўзбекча, Кирилл (Uzbek, Cyrillic) | not started | | |
| uz | Oʻzbekcha, Lotin (Uzbek, Latin) | not started | | |
| tr | Türkçe (Turkish) | not started | | |
| ur | اردو (Urdu) | not started | | |
| fa | فارسی (Persian) | not started | | |
| tg | Тоҷикӣ (Tajik) | not started | | |
| az | Azərbaycan (Azerbaijani) | not started | | |
| id | Bahasa Indonesia (Indonesian) | not started | | |
| ms | Bahasa Melayu (Malay) | not started | | |
| fr | Français (French) | not started | | |
| de | Deutsch (German) | not started | | |
| es | Español (Spanish) | not started | | |
| pt | Português (Portuguese) | not started | | |
| it | Italiano (Italian) | not started | | |
| nl | Nederlands (Dutch) | not started | | |
| bs | Bosanski (Bosnian) | not started | | |
| sq | Shqip (Albanian) | not started | | |
| bg | Български (Bulgarian) | not started | | |
| cs | Čeština (Czech) | not started | | |
| pl | Polski (Polish) | not started | | |
| ro | Română (Romanian) | not started | | |
| sv | Svenska (Swedish) | not started | | |
| no | Norsk (Norwegian) | not started | | |
| bn | বাংলা (Bengali) | not started | | |
| hi | हिन्दी (Hindi) | not started | | |
| ta | தமிழ் (Tamil) | not started | | |
| ml | മലയാളം (Malayalam) | not started | | |
| th | ไทย (Thai) | not started | | |
| zh | 中文 (Chinese) | not started | | |
| ja | 日本語 (Japanese) | not started | | |
| ko | 한국어 (Korean) | not started | | |
| ku | کوردی (Kurdish, Sorani) | not started | | |
| ha | Hausa (Hausa) | not started | | |
| so | Soomaali (Somali) | not started | | |
| sw | Kiswahili (Swahili) | not started | | |
| am | አማርኛ (Amharic) | not started | | |
| sd | سنڌي (Sindhi) | not started | | |
| ug | ئۇيغۇرچە (Uyghur) | not started | | |
| ps | پښتو (Pashto) | not started | | |
| dv | ދިވެހި (Divehi) | not started | | |
| si | සිංහල (Sinhala) | not started | | |
| my | မြန်မာ (Burmese) | not started | | |
| tt | Татарча (Tatar) | not started | | |
| ce | Нохчийн (Chechen) | not started | | |
| ber | Tamaziɣt (Berber) | not started | | |

(47 rows — generated from `locales.languages.LANGUAGES`, excluding `en` and
the `translation_only` transliteration entry. Re-derive with the same filter
if the language catalogue changes.)
