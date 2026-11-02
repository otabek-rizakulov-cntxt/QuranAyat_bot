"""GET /privacy — the policy URL Meta requires to publish the WhatsApp app."""

from fastapi.testclient import TestClient

import main
from app.routes.privacy import CONTACT_EMAIL, PRIVACY_PATH

client = TestClient(main.app)


def test_served_publicly_as_html():
    response = client.get(PRIVACY_PATH)
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    body = response.text
    assert "Privacy policy" in body and CONTACT_EMAIL in body
    assert "__EMAIL__" not in body and "__EFFECTIVE__" not in body


def test_names_what_we_store_and_how_to_leave():
    body = client.get(PRIVACY_PATH).text
    for phrase in ("WhatsApp", "Telegram", "STOP", "delete", "do not sell"):
        assert phrase in body, phrase
