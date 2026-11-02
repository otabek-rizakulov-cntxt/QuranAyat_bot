"""GET /privacy — the privacy policy Meta requires before a WhatsApp app is published.

Public and static, served by the bot itself so the URL lives on the same domain
as the webhook. Written from what the code actually stores (src/common/schema.sql
and the Redis keys under src/infra/); update it whenever that changes.
"""

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

PRIVACY_PATH = "/privacy"
CONTACT_EMAIL = "abdurrohman.devv@gmail.com"
EFFECTIVE = "2 November 2026"

router = APIRouter()

_PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>BismillahBot — Privacy policy</title>
<style>
  :root { color-scheme: light dark; }
  body { font: 16px/1.6 system-ui, -apple-system, Segoe UI, sans-serif; margin: 0;
         background: #F7F3EA; color: #1c2420; }
  main { max-width: 720px; margin: 0 auto; padding: 32px 20px 64px; }
  h1 { font-size: 1.7rem; margin: 0 0 4px; }
  h2 { font-size: 1.15rem; margin: 28px 0 8px; }
  .muted { color: #5E675F; }
  a { color: #0E6B55; }
  @media (prefers-color-scheme: dark) {
    body { background: #0F1513; color: #e6ece8; }
    .muted { color: #949E97; }
    a { color: #3CC29A; }
  }
</style>
</head>
<body>
<main>
<h1>Privacy policy</h1>
<p class="muted">BismillahBot — Qur'an reader and memorization (hifz) assistant on Telegram
and WhatsApp, and its Mini App. Effective __EFFECTIVE__.</p>

<p>BismillahBot is operated by Abdurrohman Dev ("we"). This page explains what the bot
stores about you, why, who processes it, and how to have it removed. We do not show ads,
we do not sell or share your data for marketing, and we do not use it to train AI models.</p>

<h2>What we store</h2>
<ul>
  <li><b>Your account identifier</b>: your Telegram user id, or on WhatsApp your phone
    number (WhatsApp ID) together with an internal id we assign to it.</li>
  <li><b>Your settings</b>: interface language, translation language and reciter.</li>
  <li><b>Your reading position</b>: the last surah, ayah and view you opened, so the bot
    can continue where you stopped.</li>
  <li><b>Memorization data</b>, only if you use those features: your plan, which portions
    you completed, the ayat you marked as memorized, recall-check results, streaks, and
    the time zone and reminder time you chose.</li>
  <li><b>Profile and leaderboard</b>: an optional display name, and whether you chose to
    appear on the weekly leaderboard (off unless you turn it on).</li>
  <li><b>Daily messages</b>: whether you subscribed to the verse of the day or reminders,
    at what time, and on WhatsApp when you opted in or out and when you last wrote to the
    bot (WhatsApp only allows free replies within 24 hours of your last message).</li>
  <li><b>Groups</b>, only for Telegram study groups: the group's id, its settings and
    plan, and which members chose to link themselves to its weekly board.</li>
  <li><b>Short-lived technical data</b>, kept from minutes to two days: the menu you were
    last shown, an unfinished setup step, cached media ids, one-time sign-in links, and
    WhatsApp message ids used to avoid answering the same message twice.</li>
</ul>
<p>We do not store the text of your messages beyond processing them to reply, and we
do not collect contacts, location or media you send.</p>

<h2>Why</h2>
<p>Only to provide the service you ask for: answering your requests, remembering your
settings and progress, and sending the scheduled messages you subscribed to.</p>

<h2>Who processes it</h2>
<ul>
  <li><b>Telegram</b> and <b>Meta (WhatsApp)</b> deliver messages between you and the bot,
    under their own privacy policies.</li>
  <li><b>Koyeb</b> hosts the bot; our database (Postgres) and cache (Redis) providers store
    the data above. Qur'an text, images and recitations come from public sources and
    involve none of your data.</li>
</ul>

<h2>How long</h2>
<p>Account data stays until you ask us to delete it. Technical data expires on its own as
described above. Server logs, which can contain your account id, are kept by our hosting
provider for a limited period.</p>

<h2>Your choices</h2>
<ul>
  <li>Send <b>STOP</b> on WhatsApp at any time to stop daily messages; you can also turn
    them off with <b>/daily</b> (Telegram) or <b>daily</b> (WhatsApp).</li>
  <li>Leave the leaderboard or change your name in <b>/profile</b>.</li>
  <li>Send <b>unlink</b> to disconnect a linked Telegram account and WhatsApp number.</li>
  <li>To see or delete your data, email
    <a href="mailto:__EMAIL__">__EMAIL__</a> from, or naming, the account concerned. We delete
    it within 30 days.</li>
</ul>

<h2>Children</h2>
<p>The service is meant for general audiences and is not directed at children under 13.
If you believe a child has used it, contact us and we will delete the data.</p>

<h2>Changes and contact</h2>
<p>We will update this page when what we store changes, and change the date above.
Questions: <a href="mailto:__EMAIL__">__EMAIL__</a>.</p>
</main>
</body>
</html>
""".replace("__EFFECTIVE__", EFFECTIVE).replace("__EMAIL__", CONTACT_EMAIL)


@router.get(PRIVACY_PATH, response_class=HTMLResponse)
async def privacy() -> HTMLResponse:
    return HTMLResponse(_PAGE, headers={"Cache-Control": "public, max-age=3600"})
