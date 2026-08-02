# Multi-step conversation state ("wizards"): the draft a user is part-way through.
#
# The bot already had exactly one multi-step interaction — the reciter search —
# and it is served by `File.set_awaiting_input` / `File.pop_awaiting_input`: a
# bare string under `awaiting:<chat_id>` with a 120 s TTL and nowhere to put a
# payload. That is enough for "the next message is a reciter name" and nothing
# more. `/memorize` needs four answers (target, pace, days, reminder time) held
# together while the user thinks, and `/profile` needs a name and a timezone.
#
# So this module adds a *draft*: a small JSON blob keyed by user, carrying a
# `kind` (which wizard), a `step` (where in it) and a free-form `data` dict.
# `set_awaiting_input` / `pop_awaiting_input` are untouched and keep working —
# the reciter flow is not migrated, because a 120 s single-turn flag is the right
# shape for it and rewriting it would only add risk.
#
# Storage: `RedisSingleton().connection`, the same store the navigation state
# uses. **With REDIS_HOST_URL unset the backing store is the in-process
# `MemoryStore` (see config/redis.py), so a draft does not survive a restart and
# is not shared between processes.** That is acceptable here: a draft lives for
# 30 minutes, the deployment is a single worker, and losing one means the user
# re-runs `/memorize` — no durable state is involved, since nothing is written to
# Postgres until the wizard is confirmed.

import ujson as json
from typing import Any, Dict, Optional

from config import RedisSingleton

__all__ = ["Wizard", "DRAFT_TTL", "CANCEL_COMMANDS"]

# Long enough to survive a user putting the phone down mid-wizard, short enough
# that a forgotten draft cannot ambush them tomorrow with "type a display name".
DRAFT_TTL = 30 * 60

# Typing any of these ends the wizard instead of answering its question. `/start`
# is not here because it is a command, and commands are dispatched *before* the
# wizard slot in `handle_update` — every command escapes a pending wizard.
CANCEL_COMMANDS = ("/cancel", "cancel")


class Wizard:
    """Per-user draft state for a multi-step flow.

    A draft is `{"kind": str, "step": str, "data": dict}`. `kind` names the
    wizard (and is what `hifz.dispatch_wizard` routes on), `step` is that
    wizard's own business, and `data` accumulates the answers.
    """

    redis_namespace = ""

    def __init__(self, redis=None):
        self.redis = redis if redis is not None else RedisSingleton().connection

    def _key(self, user_id: int) -> str:
        return self.redis_namespace + "wizard:" + str(user_id)

    # --- reads ---------------------------------------------------------------

    def get(self, user_id: int) -> Optional[Dict[str, Any]]:
        """The user's draft, or None when no wizard is in progress."""
        raw = self.redis.get(self._key(user_id))
        if raw is None:
            return None
        try:
            draft = json.loads(raw)
        except ValueError:                  # corrupt/legacy value: treat as absent
            self.clear(user_id)
            return None
        if not isinstance(draft, dict) or "kind" not in draft:
            self.clear(user_id)
            return None
        draft.setdefault("step", "")
        draft.setdefault("data", {})
        return draft

    def kind(self, user_id: int) -> Optional[str]:
        """Which wizard the user is in, or None."""
        draft = self.get(user_id)
        return draft["kind"] if draft else None

    def step(self, user_id: int) -> Optional[str]:
        draft = self.get(user_id)
        return draft["step"] if draft else None

    def data(self, user_id: int) -> Dict[str, Any]:
        """The accumulated answers, or {} when no wizard is in progress."""
        draft = self.get(user_id)
        return dict(draft["data"]) if draft else {}

    def is_active(self, user_id: int) -> bool:
        return self.get(user_id) is not None

    # --- writes --------------------------------------------------------------

    def start(self, user_id: int, kind: str, step: str = "",
              **data: Any) -> Dict[str, Any]:
        """Begin (or restart) a wizard, discarding any draft already in flight.

        One draft per user by design: two half-finished wizards at once has no
        sane free-text routing, and the second one is always the one the user
        meant.
        """
        draft = {"kind": kind, "step": step, "data": dict(data)}
        self.save(user_id, draft)
        return draft

    def save(self, user_id: int, draft: Dict[str, Any]) -> Dict[str, Any]:
        """Persist a whole draft, refreshing the TTL."""
        self.redis.set(self._key(user_id), json.dumps(draft), ex=DRAFT_TTL)
        return draft

    def set_step(self, user_id: int, step: str) -> Optional[Dict[str, Any]]:
        """Move to `step`, keeping the accumulated data. None if nothing is in
        flight (the draft expired, or the user tapped a stale button)."""
        draft = self.get(user_id)
        if draft is None:
            return None
        draft["step"] = step
        return self.save(user_id, draft)

    def update(self, user_id: int, step: Optional[str] = None,
               **fields: Any) -> Optional[Dict[str, Any]]:
        """Merge `fields` into the draft's data (and optionally move to `step`).

        Returns the updated draft, or None if no wizard is in flight — every
        caller must handle that, because a draft can expire between two taps.
        """
        draft = self.get(user_id)
        if draft is None:
            return None
        draft["data"].update(fields)
        if step is not None:
            draft["step"] = step
        return self.save(user_id, draft)

    def clear(self, user_id: int) -> None:
        """End the wizard. Idempotent."""
        self.redis.delete(self._key(user_id))

    # --- the /cancel path ----------------------------------------------------

    @staticmethod
    def is_cancel(text: str) -> bool:
        """Whether this free-text message means "get me out of here"."""
        return (text or "").strip().lower().split("@", 1)[0] in CANCEL_COMMANDS

    def cancel(self, user_id: int) -> bool:
        """Clear the draft; True if there actually was one to cancel."""
        active = self.is_active(user_id)
        self.clear(user_id)
        return active
