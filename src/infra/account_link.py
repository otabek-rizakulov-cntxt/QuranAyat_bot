"""Codes that link a Telegram account and a WhatsApp number (MULTI_PLATFORM_PLAN Phase 6).

`link` on one app shows a six-digit code; `link <code>` on the other joins the
two. The code lives ten minutes and is single-use, and each account gets a few
wrong guesses per window — a million codes over ten minutes is not guessable at
five tries.
"""

import secrets
from typing import Optional

from infra.redis_client import RedisSingleton

CODE_TTL = 10 * 60
MAX_TRIES = 5


def _code_key(code: str) -> str:
    return "acctlink:code:" + code


def _tries_key(user_id: int) -> str:
    return "acctlink:tries:%d" % user_id


def issue(user_id: int) -> str:
    """A fresh six-digit code naming `user_id`."""
    redis = RedisSingleton().connection
    while True:
        code = "%06d" % secrets.randbelow(10**6)
        if redis.set(_code_key(code), str(user_id), ex=CODE_TTL, nx=True):
            return code


def too_many_tries(user_id: int) -> bool:
    raw = RedisSingleton().connection.get(_tries_key(user_id))
    return raw is not None and int(raw) >= MAX_TRIES


def redeem(code: str, user_id: int) -> Optional[int]:
    """The account a valid code names (and burn it), or None. Wrong codes count
    against `user_id`'s tries."""
    redis = RedisSingleton().connection
    code = (code or "").strip()
    owner = redis.get(_code_key(code)) if code.isdigit() and len(code) == 6 else None
    if owner is None:
        tries = int(redis.get(_tries_key(user_id)) or 0) + 1
        redis.set(_tries_key(user_id), str(tries), ex=CODE_TTL)
        return None
    redis.delete(_code_key(code))
    return int(owner)
