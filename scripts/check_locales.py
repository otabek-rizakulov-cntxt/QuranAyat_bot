#!/usr/bin/env python3
# BismillahBot -- Explore the Holy Qur'an on Telegram
#
# Locale integrity check: every catalogued language must have a complete string
# table whose placeholders match English, and whose localized button labels map
# back to the right action. Run from the repo root:
#
#     python3 scripts/check_locales.py
#
# Exits non-zero on any problem, so it doubles as a CI gate.

import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

from locales import (  # noqa: E402
    ACTION_BUTTON_KEYS, DEFAULT_LANG, LANGUAGES, LOCALES,
    button_action, keyboard_rows, missing_keys, missing_locales, t,
)

PLACEHOLDER = re.compile(r"\{(\w+)\}")

# UI keys that must reach the user verbatim in every language.
REQUIRED_KEYS = sorted(LOCALES[DEFAULT_LANG])


def placeholders(text: str) -> set:
    return set(PLACEHOLDER.findall(text))


def main() -> int:
    problems = []

    absent = missing_locales()
    if absent:
        problems.append("languages with no locale table: " + ", ".join(absent))

    for lang in LANGUAGES:
        code = lang.code
        table = LOCALES.get(code)
        if table is None:
            continue

        gaps = missing_keys(code)
        if gaps:
            problems.append("%s: missing keys: %s" % (code, ", ".join(gaps)))

        for key in REQUIRED_KEYS:
            if key not in table:
                continue
            want = placeholders(LOCALES[DEFAULT_LANG][key])
            got = placeholders(table[key])
            if want != got:
                problems.append("%s: %r placeholders %s, expected %s"
                                % (code, key, sorted(got), sorted(want)))
            if not table[key].strip():
                problems.append("%s: %r is empty" % (code, key))

        # Every localized label must round-trip to the action that produced it.
        # A label colliding with another action's (or English's) label would
        # silently send the user somewhere else.
        for action, btn_key in ACTION_BUTTON_KEYS.items():
            label = t(btn_key, code)
            resolved = button_action(label, code)
            if resolved != action:
                problems.append("%s: button %r resolves to %r, expected %r"
                                % (code, label, resolved, action))

        labels = [label for row in keyboard_rows(code) for label in row]
        dupes = {x for x in labels if labels.count(x) > 1}
        if dupes:
            problems.append("%s: duplicate keyboard labels: %s"
                            % (code, ", ".join(sorted(dupes))))

        # HTML-parsed messages must not carry unbalanced tags: Telegram rejects
        # the whole send if they don't pair up.
        for key in ("welcome", "about"):
            if key in table and table[key].count("<b>") != table[key].count("</b>"):
                problems.append("%s: %r has unbalanced <b> tags" % (code, key))

    print("checked %d languages, %d keys each" % (len(LANGUAGES), len(REQUIRED_KEYS)))
    if problems:
        print("\n%d problem(s):" % len(problems))
        for p in problems:
            print("  -", p)
        return 1
    print("all locales complete and consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
