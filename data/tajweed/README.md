# Tajweed data

Used by the tajweed section (`docs/TAJWEED_PLAN.md`). Both source files are verbatim copies; do
not edit them; the annotations index the text by Unicode code point.

| File | What | Source and licence |
|---|---|---|
| `quran-uthmani.txt` | Uthmani Qur'an text, `surah\|ayah\|text`, Hafs | [Tanzil.net](http://tanzil.net), the copy the annotations were built on (via cpfair/quran-tajweed, downloaded 2017-04-06). Tanzil terms: verbatim use with the source indicated; its notice is kept at the end of the file. |
| `tajweed.json` | Per ayah, `{surah, ayah, annotations: [{rule, start, end}]}`; `start`/`end` are code-point offsets into that ayah's text | [cpfair/quran-tajweed](https://github.com/cpfair/quran-tajweed), `output/tajweed.hafs.uthmani-pause-sajdah.json`, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| `examples.json` | Best example ayahs per rule, generated | `scripts/tajweed/build.py` from the two files above |
| `lessons.uz.json` | The lessons (Uzbek Latin) | Written for this project; reviewed by the owner before publication |

This text deliberately differs from `data/translations/ar.txt` (another spelling convention, see
the plan §2); the rest of the bot keeps using `ar.txt`.
