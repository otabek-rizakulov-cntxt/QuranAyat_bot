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
    ACTION_BUTTON_KEYS, BOT_COMMANDS, DEFAULT_LANG, LANGUAGES, LOCALES,
    UI_LANGUAGES, button_action, keyboard_rows, missing_keys, missing_locales,
    t, welcome_text,
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

    # Only interface languages need a string table; translation-only entries (the
    # transliteration) are a reading of the Qur'an, not a language the UI exists in.
    for lang in UI_LANGUAGES:
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
        for key in ("welcome_intro", "welcome_inline", "about"):
            if key in table and table[key].count("<b>") != table[key].count("</b>"):
                problems.append("%s: %r has unbalanced <b> tags" % (code, key))

        # /start must advertise every registered command, in every language.
        # The list is generated, so a gap here means a locale hard-coded its own.
        message = welcome_text(code)
        absent_commands = [c for c, _ in BOT_COMMANDS if "/%s " % c not in message]
        if absent_commands:
            problems.append("%s: /start omits: %s"
                            % (code, ", ".join("/" + c for c in absent_commands)))

    # Every bundled translation must actually exist on disk, including the
    # translation-only ones that have no string table to check.
    for lang in LANGUAGES:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                            "translations", lang.code + ".txt")
        if not os.path.exists(path):
            problems.append("%s: translations/%s.txt is missing" % (lang.code, lang.code))

    print("checked %d interface languages (%d keys each) and %d bundled translations"
          % (len(UI_LANGUAGES), len(REQUIRED_KEYS), len(LANGUAGES)))
    if problems:
        print("\n%d problem(s):" % len(problems))
        for p in problems:
            print("  -", p)
        return 1
    print("all locales complete and consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
