"""Import-direction rules between the top-level packages (docs/REFACTOR_PLAN.md §4).

Dependencies point one way:

    app, main  →  bot, api, hifz  →  services  →  infra, lib, modules  →  domain, config, locales

Nothing imports `main`. Only the presentation layer (app, bot, api, hifz, main)
and infra, which wraps the Telegram client, may import Telegram or FastAPI.

Today's code breaks a few of these rules. They are listed in KNOWN with the
refactor step that removes each one, and the list is a ratchet:

  * a violation that isn't listed fails `test_no_new_violations`;
  * a listed violation that no longer exists fails `test_known_violations_still_exist`,
    so the entry has to be deleted in the same PR that fixes it.

When the refactor renames packages (app/, bot/, domain/, infra/), update ALLOWED
in the same PR.
"""

import ast
import os

SRC = os.path.join(os.path.dirname(__file__), "..", "src")

PACKAGES = {
    "main", "app", "bot", "api", "hifz",
    "services",
    "infra", "lib", "modules",
    "domain", "config", "locales",
}  # fmt: skip

_BASE = {"domain", "config", "locales"}
_LOWER = _BASE | {"infra", "lib", "modules"}

# Which project packages each package may import (itself included).
ALLOWED = {
    "config": {"config"},
    "locales": {"locales"},
    "domain": {"domain", "config", "locales"},
    "modules": _BASE | {"modules"},
    "lib": _LOWER,
    "infra": _LOWER,
    "services": _LOWER | {"services"},
    # The bot's feature modules (hifz, until it becomes bot/features) and the bot
    # core sit side by side in the presentation layer.
    "bot": _LOWER | {"services", "bot", "hifz"},
    "hifz": _LOWER | {"services", "bot", "hifz"},
    "api": _LOWER | {"services", "api"},
    "app": PACKAGES - {"main"},
    "main": PACKAGES - {"main"},
}

FRAMEWORKS = {"telegram", "fastapi"}
# Packages below the presentation layer: no Telegram, no FastAPI.
FRAMEWORK_FREE = {"config", "locales", "domain", "modules", "lib", "services"}

# (file relative to src/, imported module) -> the refactor step that removes it.
KNOWN = {
    ("modules/bot.py", "telegram"): "4.3 bot client moves to infra/telegram.py",
    ("lib/miniapp.py", "telegram"): "5.3 app_row moves to bot/keyboards/",
    ("lib/scheduler.py", "telegram"): "5.2 scheduler moves to infra/",
    ("lib/plan_builder.py", "hifz.refs"): "5.1 refs moves to domain/",
    ("lib/hifz_progress.py", "hifz.refs"): "5.1 refs moves to domain/",
    ("services/check.py", "hifz.refs"): "5.1 refs moves to domain/",
    ("services/plans.py", "hifz.refs"): "5.1 refs moves to domain/",
    ("services/profile.py", "hifz.refs"): "5.1 refs moves to domain/",
    ("services/progress.py", "hifz.refs"): "5.1 refs moves to domain/",
    ("api/common.py", "hifz.refs"): "5.1 refs moves to domain/",
    ("api/plans.py", "hifz.refs"): "5.1 refs moves to domain/",
}


def _sources():
    for dirpath, _, names in os.walk(SRC):
        for name in names:
            if name.endswith(".py"):
                path = os.path.join(dirpath, name)
                rel = os.path.relpath(path, SRC).replace(os.sep, "/")
                package = rel.split("/")[0].removesuffix(".py")
                if package in ALLOWED:
                    yield rel, package, path


def _absolute_imports(path):
    """Every absolute import in the file — including ones inside functions,
    which is where a cycle-dodging import usually hides."""
    with open(path, encoding="utf-8") as f:
        tree = ast.parse(f.read(), path)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            yield node.module


def _violations():
    found = set()
    for rel, package, path in _sources():
        for module in _absolute_imports(path):
            top = module.split(".")[0]
            if top in PACKAGES and top not in ALLOWED[package]:
                found.add((rel, module))
            elif top in FRAMEWORKS and package in FRAMEWORK_FREE:
                found.add((rel, top))
    return found


def test_no_new_violations():
    new = sorted(_violations() - set(KNOWN))
    assert not new, "imports against the layering rules (see this file's header):\n" + "\n".join(
        "  %s imports %s" % v for v in new
    )


def test_known_violations_still_exist():
    fixed = sorted(set(KNOWN) - _violations())
    assert not fixed, "fixed — delete these from KNOWN:\n" + "\n".join(
        "  %s -> %s" % v for v in fixed
    )


def test_the_scan_sees_every_package():
    # Packages appear as the refactor creates them; every one that exists must
    # have rules, and nothing unruled may hide under src/.
    on_disk = {
        name.removesuffix(".py")
        for name in os.listdir(SRC)
        if (name.endswith(".py") or os.path.isdir(os.path.join(SRC, name)))
        and not name.startswith(("_", "."))
        and name not in ("common",)
    }
    assert on_disk <= set(ALLOWED), sorted(on_disk - set(ALLOWED))
    seen = {package for _, package, _ in _sources()}
    assert seen == on_disk
