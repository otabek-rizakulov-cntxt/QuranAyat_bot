"""Source-level guards for the service layer (docs/MINI_APP_PLAN.md P1.3).

`src/services/` is shared by the bot and the Mini App API, so it must not depend
on Telegram; `src/api/` is an HTTP adapter, so it must not hold SQL — storage
goes through `lib.store`, the same as the bot."""

import ast
import os
import re

import pytest

SRC = os.path.join(os.path.dirname(__file__), "..", "src")
_SQL = re.compile(r"\b(SELECT|INSERT\s+INTO|UPDATE\s+\w+\s+SET|DELETE\s+FROM)\b")


def _py_files(package):
    root = os.path.join(SRC, package)
    for dirpath, _, names in os.walk(root):
        for name in names:
            if name.endswith(".py"):
                yield os.path.join(dirpath, name)


def _imported_modules(path):
    with open(path, encoding="utf-8") as f:
        tree = ast.parse(f.read(), path)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name
        elif isinstance(node, ast.ImportFrom) and node.module:
            yield node.module


@pytest.mark.parametrize("path", sorted(_py_files("services")))
def test_services_never_import_telegram(path):
    bad = [m for m in _imported_modules(path) if m == "telegram" or m.startswith("telegram.")]
    assert not bad, "%s imports %s" % (os.path.relpath(path, SRC), bad)


@pytest.mark.parametrize("path", sorted(_py_files("api")))
def test_api_holds_no_sql(path):
    with open(path, encoding="utf-8") as f:
        source = f.read()
    assert not _SQL.search(source), "%s contains SQL" % os.path.relpath(path, SRC)
    assert "asyncpg" not in source


def test_guards_see_files():
    assert list(_py_files("services")) and list(_py_files("api"))
