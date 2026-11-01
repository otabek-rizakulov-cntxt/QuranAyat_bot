"""WhatsApp stays off unless it is fully configured (MULTI_PLATFORM_PLAN P2.0)."""

import pytest

from config.settings import get_settings

FULL = {
    "WHATSAPP_ENABLED": "1",
    "WHATSAPP_PHONE_NUMBER_ID": "1234567890",
    "WHATSAPP_ACCESS_TOKEN": "token",
    "WHATSAPP_APP_SECRET": "secret",
    "WHATSAPP_VERIFY_TOKEN": "verify",
}


@pytest.fixture
def env(monkeypatch):
    for name in FULL:
        monkeypatch.delenv(name, raising=False)

    def apply(**values):
        for name, value in values.items():
            monkeypatch.setenv(name, value)

    return apply


def test_off_by_default(env):
    assert get_settings().whatsapp_ready is False


def test_on_when_fully_configured(env):
    env(**FULL)
    assert get_settings().whatsapp_ready is True


@pytest.mark.parametrize("missing", sorted(FULL))
def test_any_missing_value_keeps_it_off(env, missing):
    env(**{k: v for k, v in FULL.items() if k != missing})
    assert get_settings().whatsapp_ready is False


def test_the_flag_must_be_truthy(env):
    env(**{**FULL, "WHATSAPP_ENABLED": "no"})
    assert get_settings().whatsapp_ready is False
