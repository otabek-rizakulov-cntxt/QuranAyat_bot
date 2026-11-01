"""Telegram HTML → WhatsApp formatting, and splitting at WhatsApp's 4,096 chars."""

import html
import re

import pytest

import locales
from channels.whatsapp_format import MAX_TEXT, split, to_whatsapp
from locales import UI_LANGUAGES, welcome_text

LEFTOVER_TAG = re.compile(r"</?(b|strong|i|em|s|u|code|pre|a|blockquote|tg-spoiler)\b")


class TestTags:
    @pytest.mark.parametrize(
        "source, expected",
        [
            ("<b>bold</b>", "*bold*"),
            ("<strong>bold</strong>", "*bold*"),
            ("<i>it</i>", "_it_"),
            ("<em>it</em>", "_it_"),
            ("<s>gone</s>", "~gone~"),
            ("<code>/2 Al-Baqarah</code>", "`/2 Al-Baqarah`"),
            ("<pre>\nline 1\nline 2\n</pre>", "```line 1\nline 2```"),
            ("<u>under</u>", "under"),
            ("<tg-spoiler>hidden</tg-spoiler>", "hidden"),
            ("<span class='x'>plain</span>", "plain"),
            ("a<br>b<br/>c", "a\nb\nc"),
            ("<blockquote>one\ntwo</blockquote>", "> one\n> two"),
        ],
    )
    def test_each_tag(self, source, expected):
        assert to_whatsapp(source) == expected

    def test_links(self):
        assert to_whatsapp('<a href="https://q.com/2">Read</a>') == "Read (https://q.com/2)"
        assert to_whatsapp('<a href="https://q.com">https://q.com</a>') == "https://q.com"
        assert to_whatsapp('<a href="https://q.com"></a>') == "https://q.com"

    def test_nesting(self):
        assert to_whatsapp("<b><i>both</i></b>") == "*_both_*"
        assert to_whatsapp("<b>a <code>x</code> b</b>") == "*a `x` b*"

    def test_markers_hug_their_text(self):
        # WhatsApp ignores "* bold *": edge spaces move outside the marker
        assert to_whatsapp("say <b> hi </b>!") == "say  *hi* !"
        assert to_whatsapp("<b>\nhead\n</b>") == "\n*head*\n"

    def test_an_empty_run_gets_no_marker(self):
        assert to_whatsapp("a<b></b>b<i> </i>c") == "ab c"

    def test_entities_are_decoded(self):
        assert to_whatsapp("&lt;b&gt; &amp; &quot;q&quot; &#x27;s&#39;") == "<b> & \"q\" 's'"

    def test_malformed_html_keeps_its_words(self):
        assert to_whatsapp("a</b> b") == "a b"  # stray end tag
        assert to_whatsapp("<b>open") == "*open*"  # never closed

    def test_plain_text_is_untouched(self):
        assert to_whatsapp("2:255 — Ayat al-Kursi") == "2:255 — Ayat al-Kursi"

    def test_rtl_text(self):
        assert to_whatsapp("<b>سورة البقرة</b>\n\nاللَّهُ") == "*سورة البقرة*\n\nاللَّهُ"


class TestWhatTheBotSends:
    def test_a_verse_card(self):
        # bot.text.build_verse_text: a bold, escaped surah name over an escaped body
        name, body = "Al-Baqarah", "Allah — there is no deity <except> Him & ..."
        card = "<b>%s</b>\n\n%s" % (html.escape(name), html.escape(body))
        assert to_whatsapp(card) == "*Al-Baqarah*\n\n" + body

    def test_the_index(self):
        # domain.quran's /index line
        assert to_whatsapp("/2 <code>Al-Baqarah</code>/3 Al-Imran") == "/2 `Al-Baqarah`/3 Al-Imran"

    @pytest.mark.parametrize("lang", [lang.code for lang in UI_LANGUAGES])
    def test_every_welcome(self, lang):
        out = to_whatsapp(welcome_text(lang))
        assert not LEFTOVER_TAG.search(out)
        assert out.strip()

    def test_every_locale_string(self):
        checked = 0
        tables = locales._load_locales()
        for table in tables.values():
            for key, value in table.items():
                if isinstance(value, str) and "<" in value:
                    out = to_whatsapp(value)
                    assert not LEFTOVER_TAG.search(out), (key, out)
                    assert "{" not in value or out.count("{") == value.count("{"), key
                    checked += 1
        assert checked >= len(tables)  # every locale carries formatted strings


class TestSplit:
    def test_short_text_is_one_chunk(self):
        assert split("hello") == ["hello"]
        assert split("") == [""]
        assert split("x" * MAX_TEXT) == ["x" * MAX_TEXT]

    def test_prefers_paragraphs(self):
        text = "a" * 6 + "\n\n" + "b" * 6 + "\n" + "c" * 3
        assert split(text, limit=12) == ["a" * 6, "b" * 6 + "\n" + "c" * 3]

    def test_then_lines(self):
        assert split("aaaa\nbbbb cc", limit=8) == ["aaaa", "bbbb cc"]

    def test_then_words(self):
        assert split("one two three four", limit=9) == ["one two", "three", "four"]

    def test_hard_cut_only_for_a_giant_word(self):
        assert split("x" * 10, limit=4) == ["xxxx", "xxxx", "xx"]

    def test_real_sized_tafsir(self):
        paragraph = ("word " * 150).strip()
        text = "\n\n".join([paragraph] * 12)  # ~9,000 chars
        chunks = split(text)
        assert len(chunks) > 1
        assert all(len(c) <= MAX_TEXT for c in chunks)
        assert "".join(chunks).replace("\n", "").replace(" ", "") == text.replace("\n", "").replace(
            " ", ""
        )
