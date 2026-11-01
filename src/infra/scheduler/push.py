"""Delivering a scheduled push on any platform (docs/MULTI_PLATFORM_PLAN.md P2.6).

WhatsApp charges for, and polices, what a business sends unprompted. A push
therefore goes one of three ways there:

  * the user wrote within the last 24 hours (the service window): the free
    session message, exactly what Telegram gets;
  * the window is closed: the pre-approved template, which is billed — the
    log line below is the record to estimate that cost from;
  * the user never opted in, or said STOP since: nothing at all.

Telegram has no window, no template and no consent rule, so it always gets the
session message. A send handler describes both forms and lets this decide:

    outcome = await deliver_push(
        ctx, session=lambda channel: deliver_quran(channel, ...),
        template=Template("daily_ayah", "en", [reference, text], ["vc:tr:2:255"]),
    )
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Awaitable, Callable, List, Optional

from channels import TELEGRAM, WHATSAPP
from channels.whatsapp import WhatsAppChannel, WindowClosed

logger = logging.getLogger(__name__)

# Ten minutes short of 24 hours: a session message sent at 23:59 could arrive
# after the window closes and be refused.
SERVICE_WINDOW = timedelta(hours=24) - timedelta(minutes=10)

SESSION = "session"
TEMPLATE = "template"
DROPPED = "dropped"

_whatsapp_client = None


def set_whatsapp_client(client) -> None:
    """Hand the scheduler the Graph client (app startup, when WhatsApp is on)."""
    global _whatsapp_client
    _whatsapp_client = client


@dataclass(frozen=True)
class Template:
    """An approved WhatsApp template and what fills it."""

    name: str
    lang: str
    params: List[str] = field(default_factory=list)
    payloads: List[str] = field(default_factory=list)  # quick-reply buttons, in order


Session = Callable[[object], Awaitable[None]]


def _log(ctx, outcome: str, category: Optional[str] = None, template: Optional[str] = None):
    logger.info(
        "push platform=%s kind=%s user=%d outcome=%s category=%s template=%s",
        ctx.platform,
        ctx.kind,
        ctx.chat_id,
        outcome,
        category or "-",
        template or "-",
    )


async def deliver_push(
    ctx,
    *,
    session: Session,
    template: Optional[Template] = None,
    needs_consent: bool = True,
    category: str = "marketing",
) -> str:
    """Send a scheduled push the way its platform allows; returns the outcome."""
    if ctx.platform == TELEGRAM:
        await session(ctx.channel)
        _log(ctx, SESSION, "free")
        return SESSION
    if ctx.platform != WHATSAPP:
        raise ValueError("no push delivery for platform %r" % ctx.platform)

    if _whatsapp_client is None:
        _log(ctx, DROPPED, "whatsapp-off")
        return DROPPED
    row = await ctx.store.identity.get_by_user(ctx.chat_id, WHATSAPP)
    if row is None:
        _log(ctx, DROPPED, "no-identity")
        return DROPPED
    if needs_consent and not row.consented:
        _log(ctx, DROPPED, "no-consent")
        return DROPPED

    channel = WhatsAppChannel(_whatsapp_client, row.external_id, ctx.chat_id)
    now = ctx.now or datetime.now(timezone.utc)
    if row.last_inbound_at is not None and now - row.last_inbound_at < SERVICE_WINDOW:
        try:
            await session(channel)
            _log(ctx, SESSION, "service")
            return SESSION
        except WindowClosed:
            pass  # our clock and Meta's disagree; the template is still allowed
    if template is None:
        _log(ctx, DROPPED, "window-closed")
        return DROPPED
    await channel.send_template(template.name, template.lang, template.params, template.payloads)
    _log(ctx, TEMPLATE, category, template.name)
    return TEMPLATE
