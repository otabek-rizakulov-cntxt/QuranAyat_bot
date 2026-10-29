"""config.settings — typed configuration read from the environment."""

import pytest

from config import get_settings


@pytest.mark.parametrize("value, expected", [("1", True), ("true", True), (" Yes ", True),
                                             ("", False), ("0", False), (None, False)])  # fmt: skip
def test_the_memory_store_flag(monkeypatch, value, expected):
    if value is None:
        monkeypatch.delenv("ALLOW_MEMORY_STORE", raising=False)
    else:
        monkeypatch.setenv("ALLOW_MEMORY_STORE", value)
    assert get_settings().allow_memory_store is expected


def test_cors_origins_are_split_and_trimmed(monkeypatch):
    monkeypatch.setenv("MINIAPP_ORIGINS", " https://a.example , ,https://b.example")
    assert get_settings().miniapp_origins == ("https://a.example", "https://b.example")


def test_page_images_fall_back_to_the_photo_set(monkeypatch):
    monkeypatch.setenv("PHOTO_BASE_URL", "https://cdn/photos")
    monkeypatch.delenv("PAGE_IMAGE_BASE_URL", raising=False)
    assert get_settings().page_image_base_url == "https://cdn/photos"
    monkeypatch.setenv("PAGE_IMAGE_BASE_URL", "https://cdn/pages")
    assert get_settings().page_image_base_url == "https://cdn/pages"


def test_the_webhook_base_prefers_the_explicit_url(monkeypatch):
    monkeypatch.setenv("WEBHOOK_URL", "https://bot.example/")
    monkeypatch.setenv("RAILWAY_PUBLIC_DOMAIN", "railway.example")
    assert get_settings().webhook_base_url == "https://bot.example"


def test_the_webhook_base_falls_back_to_railway(monkeypatch):
    monkeypatch.setenv("WEBHOOK_URL", "")
    monkeypatch.setenv("RAILWAY_PUBLIC_DOMAIN", "railway.example/")
    assert get_settings().webhook_base_url == "https://railway.example"


def test_no_public_url_is_none(monkeypatch):
    monkeypatch.setenv("WEBHOOK_URL", "")
    monkeypatch.delenv("RAILWAY_PUBLIC_DOMAIN", raising=False)
    assert get_settings().webhook_base_url is None


def test_settings_are_live_and_read_only(monkeypatch):
    monkeypatch.setenv("MINIAPP_URL", "https://one.example")
    assert get_settings().miniapp_url == "https://one.example"
    monkeypatch.setenv("MINIAPP_URL", "https://two.example")
    assert get_settings().miniapp_url == "https://two.example"
    with pytest.raises(AttributeError):
        get_settings().miniapp_url = "x"
