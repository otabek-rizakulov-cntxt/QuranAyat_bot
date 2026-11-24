from domain import tajweed, tajweed_lessons, tajweed_reader


def test_every_rule_links_to_a_rules_track_lesson():
    ids = {x.id for x in tajweed_lessons.lessons("uz")}
    for rule in tajweed_reader.ORDER:
        assert tajweed_reader.rule_lesson(rule) in ids, rule


def test_rules_doc_has_a_name_and_hint_in_every_language():
    for lang in tajweed_reader.HINT_LANGS:
        doc = tajweed_reader.rules_doc(lang)
        assert [r["id"] for r in doc] == list(tajweed_reader.ORDER)
        assert all(r["name"] and r["hint"] for r in doc), lang


def test_cyrillic_hints_keep_the_arabic_letters():
    cyrl = {r["id"]: r for r in tajweed_reader.rules_doc("uz-Cyrl")}
    assert "ي ن م و" in cyrl["idghaam_ghunnah"]["hint"]
    assert "Ғунна" in cyrl["ghunnah"]["name"] or "Ғ" in cyrl["ghunnah"]["name"]


def test_other_languages_use_english():
    assert tajweed_reader.rules_doc("de") == tajweed_reader.rules_doc("en")


def test_surah_doc_matches_the_annotations():
    doc = tajweed_reader.surah_doc(1)
    assert len(doc) == 7
    body, spans = doc[0]
    assert body == tajweed.text(1, 1)
    for i, a, b in spans:
        assert 0 <= a < b <= len(body)
        assert (tajweed_reader.ORDER[i], a, b) in tajweed.spans(1, 1)
    assert len(tajweed_reader.surah_doc(2)) == 286


def test_the_bismillah_is_lifted_off_ayah_one():
    assert tajweed_reader.surah_doc(2)[0][0] == "الٓمٓ"
    for surah in (95, 97, 113):
        body, spans = tajweed_reader.surah_doc(surah)[0]
        assert not body.startswith(("بِسْمِ", "بِّسْمِ")), surah
        assert all(0 <= a < b <= len(body) for _, a, b in spans)
    assert tajweed_reader.surah_doc(1)[0][0].startswith("بِسْمِ")
    assert tajweed_reader.surah_doc(9)[0][0] == tajweed.text(9, 1)
