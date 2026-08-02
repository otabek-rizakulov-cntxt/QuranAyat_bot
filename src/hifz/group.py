# The group cluster (Phase 2, items 5-7): a supergroup study circle.
#
# The shape of it:
#   * The bot is added to a supergroup. A `my_chat_member` update tells us who
#     added it (`on_my_chat_member`), we create a `group_config` row keyed by the
#     chat, and post a message *in the group* with a deep link — because the bot
#     cannot DM an admin who has never started it.
#   * The admin taps the link, arriving in DM as `/start gs_<chat_id>`. We verify
#     they really are an admin of that chat with `getChatMember`, then run the
#     setup in DM: name a forum topic (created via `createForumTopic`, so we own
#     the thread id), choose the translation language and reciter.
#   * Members join the weekly board with a second deep link, `gb_<chat_id>`.
#
# Only `group_config` chats are served: `main.handle_update` ignores every group
# without a row here, which is how the Phase-1 blanket ban on `chat_id < 0`
# becomes selective (J1).
#
# `on_my_chat_member` and the deep-link entry are plain functions main.py calls —
# they are not commands, callbacks or wizards, because a chat-member change and a
# `/start` payload are neither. The setup *steps* do use the seam: `@wizard` for
# the typed topic name, `@callback` (prefix `gr:`) for the inline choices.

import html
from typing import Optional

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import telegram

from hifz import Ctx, callback, wizard
from lib.scheduler import send_handler
from lib.store.groups import CONFIG_ACTIVE, CONFIG_PAUSED, CONFIG_SETUP
from locales import t

WIZARD_KIND = "group_setup"

# Deep-link payloads. Telegram lowercases nothing in the /start argument, but a
# chat id is digits and a minus sign, so case never matters here.
SETUP_PREFIX = "gs_"        # admin configures the group
BOARD_PREFIX = "gb_"        # member joins the group board

_ADMIN_STATUSES = ("creator", "administrator")
_bot_username: Optional[str] = None


async def bot_username(bot) -> str:
  """The bot's @username, fetched once and cached — needed to build deep links."""
  global _bot_username
  if _bot_username is None:
    me = await bot.get_me()
    _bot_username = me.username
  return _bot_username


def _deep_link(username: str, payload: str) -> str:
  return "https://t.me/%s?start=%s" % (username, payload)


# --- J1 / J2: the bot is added to (or removed from) a group --------------------

async def on_my_chat_member(bot, store, update) -> None:
  """A `my_chat_member` update: the bot's own membership somewhere changed.

  Adding the bot to a supergroup creates its config and posts a setup link in the
  group. Removing it pauses the config rather than deleting it, so a re-add keeps
  the plan and the board history.
  """
  cm = update.my_chat_member
  chat = cm.chat
  if chat.type not in ("group", "supergroup"):
    return

  new_status = cm.new_chat_member.status
  added = new_status in ("member", "administrator")
  removed = new_status in ("left", "kicked")

  if removed:
    config = await store.groups.get_config(chat.id)
    if config is not None:
      await store.groups.update_config(chat.id, status=CONFIG_PAUSED)
    return

  if not added:
    return

  admin_id = cm.from_user.id
  await store.groups.ensure_config(chat.id, admin_user_id=admin_id)

  # The bot cannot DM an admin who has not started it, so the invitation lives in
  # the group as a deep link that opens a DM already carrying the chat id.
  username = await bot_username(bot)
  link = _deep_link(username, SETUP_PREFIX + str(chat.id))
  await bot.send_message(
      chat_id=chat.id,
      text=t("group_added", "en"),
      reply_markup=InlineKeyboardMarkup(
          [[InlineKeyboardButton(t("group_btn_setup", "en"), url=link)]]))


# --- The /start deep-link entry (called from main's /start handler) ------------

async def handle_start_payload(ctx: Ctx, payload: str) -> bool:
  """Route a `/start` deep-link argument. True if it was a group payload.

  `ctx.chat_id` is the DM the link opened; the chat id is *in* the payload.
  """
  if payload.startswith(SETUP_PREFIX):
    await _begin_setup(ctx, _chat_id(payload, SETUP_PREFIX))
    return True
  if payload.startswith(BOARD_PREFIX):
    await _join_board(ctx, _chat_id(payload, BOARD_PREFIX))
    return True
  return False


def _chat_id(payload: str, prefix: str) -> Optional[int]:
  try:
    return int(payload[len(prefix):])
  except (ValueError, TypeError):
    return None


async def _is_group_admin(ctx: Ctx, chat_id: int) -> bool:
  """Whether the caller is a creator/administrator of `chat_id`, asked live.

  Asked at the moment of action rather than trusted from the link, so a stale
  link cannot let a demoted admin reconfigure a group.
  """
  try:
    member = await ctx.bot.get_chat_member(chat_id, ctx.user_id)
  except telegram.error.TelegramError:
    return False
  return getattr(member, "status", None) in _ADMIN_STATUSES


# --- J2 / J3: the admin configures the group in DM -----------------------------

async def _begin_setup(ctx: Ctx, chat_id: Optional[int]) -> None:
  config = await ctx.store.groups.get_config(chat_id) if chat_id is not None else None
  if config is None:
    await ctx.reply(ctx.tr("group_setup_unknown"))
    return
  if not await _is_group_admin(ctx, chat_id):
    await ctx.reply(ctx.tr("group_setup_not_admin"))
    return
  # Record who is really configuring it (the adder may differ from the setter).
  await ctx.store.groups.update_config(chat_id, admin_user_id=ctx.user_id)
  ctx.wiz.start(ctx.user_id, WIZARD_KIND, step="topic", chat_id=chat_id)
  await ctx.reply(ctx.tr("group_topic_prompt"))


@wizard(WIZARD_KIND)
async def setup_step(ctx: Ctx, text: str) -> None:
  """The typed steps of setup: the topic name, the target, and the post time.

  Button steps (translation, pace, days, timezone) arrive as `gr:` callbacks;
  this handles only the free-text ones, routed by the draft's `step`.
  """
  draft = ctx.wiz.get(ctx.user_id)
  if draft is None:
    return
  step = draft.get("step")
  if step == "topic":
    await _step_topic(ctx, draft, text)
  elif step == "target":
    await _step_target(ctx, draft, text)
  elif step == "post_time":
    await _step_post_time(ctx, draft, text)


async def _step_topic(ctx: Ctx, draft, text: str) -> None:
  chat_id = draft["data"].get("chat_id")
  name = text.strip()[:128]
  if not name:
    await ctx.reply(ctx.tr("group_topic_prompt"))
    return
  thread_id = await _create_topic(ctx.bot, chat_id, name)
  await ctx.store.groups.update_config(chat_id, thread_id=thread_id)
  if thread_id is None:
    # J3 fallback: a plain supergroup has no topics, so the bot posts in the
    # main chat. Say so rather than let the admin wonder where posts will land.
    await ctx.reply(ctx.tr("group_topic_fallback"))
  else:
    await ctx.reply(ctx.tr("group_topic_created").format(name=html.escape(name)),
                    parse_mode="HTML")
  ctx.wiz.update(ctx.user_id, step="translation")
  await ctx.reply(ctx.tr("group_translation_prompt"), reply_markup=_lang_keyboard())


async def _step_target(ctx: Ctx, draft, text: str) -> None:
  from hifz.refs import parse_reference, KIND_RANGE, KIND_SURAH, KIND_JUZ
  ref = parse_reference(text)
  if ref is None:
    await ctx.reply(ctx.tr("group_target_invalid"))
    return
  ctx.wiz.update(ctx.user_id, step="pace",
                 target=[ref.kind, ref.start_surah, ref.start_ayah,
                         ref.end_surah, ref.end_ayah])
  await ctx.reply(ctx.tr("group_pace_prompt"), reply_markup=_pace_keyboard())


async def _step_post_time(ctx: Ctx, draft, text: str) -> None:
  from hifz.profile import parse_reminder_time
  post_time = parse_reminder_time(text)
  if post_time is None:
    await ctx.reply(ctx.tr("group_post_time_invalid"))
    return
  await _save_group_plan(ctx, draft["data"], post_time)


async def _save_group_plan(ctx: Ctx, data: dict, post_time) -> None:
  """Build the plan (same pure generator as the personal plan) and queue day one."""
  from datetime import date
  from hifz.refs import Ref
  from lib.plan_builder import build_plan, to_day_specs, advancing
  from lib.localtime import local_date, normalize_offset

  chat_id = data.get("chat_id")
  kind, s_s, s_a, e_s, e_a = data["target"]
  ref = Ref(kind, s_s, s_a, e_s, e_a)
  pace = int(data.get("pace") or 0)
  days = data.get("days") or list(range(1, 8))
  offset = normalize_offset(data.get("offset") or DEFAULT_OFFSET)

  # Retire any previous plan (one active per group, the same convention as users).
  old = await ctx.store.groups.get_active_plan(chat_id)
  if old is not None:
    await ctx.store.groups.set_plan_status(old.id, "complete")

  from datetime import datetime, timezone
  start = local_date(datetime.now(timezone.utc), offset)
  portions = build_plan(ref, pace, days, start)
  plan = await ctx.store.groups.create_plan(
      chat_id, kind, ref.start_surah, ref.start_ayah, ref.end_surah, ref.end_ayah,
      pace, days, to_day_specs(portions))

  await ctx.store.groups.update_config(
      chat_id, timezone=offset, post_time=post_time, days_of_week=days,
      status=CONFIG_ACTIVE)
  ctx.wiz.clear(ctx.user_id)

  await _enqueue_next_group(ctx.store, chat_id, plan)
  await _enqueue_next_board(ctx.store, chat_id)
  username = await bot_username(ctx.bot)
  board = _deep_link(username, BOARD_PREFIX + str(chat_id))
  await ctx.reply(ctx.tr("group_setup_done").format(
      board_link=board, days=len(advancing(portions)), total=len(portions)))


# --- J5: the daily group post through the Phase 1 scheduler ---------------------

SEND_KIND = "group_plan_day"


async def _enqueue_next_group(store, chat_id: int, plan, now=None):
  """Queue the next pending portion's post. None if none, or the plan is inactive.

  Mirrors `hifz.memorize._enqueue_next`: `enqueue` answers None on a key clash
  rather than raising, so re-arming the chain more often than needed is a no-op.
  """
  from datetime import datetime, timezone
  from lib.localtime import to_utc, next_due_utc, local_date, normalize_offset, parse_offset
  from lib.scheduler import enqueue
  from lib.store.groups import GPLAN_ACTIVE, GDAY_PENDING

  if plan is None or plan.status != GPLAN_ACTIVE:
    return None
  config = await store.groups.get_config(chat_id)
  if config is None or config.post_time is None or not config.timezone:
    return None
  offset = normalize_offset(config.timezone)

  pending = await store.groups.list_plan_days(plan.id, state=GDAY_PENDING)
  if not pending:
    return None
  day = pending[0]

  now = now or datetime.now(timezone.utc)
  from datetime import datetime as _dt
  due_at = to_utc(_dt.combine(day.scheduled_date, config.post_time), offset)
  if due_at <= now:
    due_at = next_due_utc(config.post_time, offset, now)

  return await enqueue(store, SEND_KIND, chat_id, due_at,
                       local_day=local_date(due_at, offset),
                       thread_id=config.thread_id,
                       payload={"group_plan_day_id": day.id, "group_plan_id": plan.id,
                                "chat_id": chat_id})


@send_handler(SEND_KIND)
async def push_group_day(ctx) -> None:
  """Deliver one group portion to the topic, then re-arm the chain.

  Returning marks the queued row 'sent'; raising marks it 'failed'. A paused
  group, a torn-down plan, or an already-delivered day all *return* — none is a
  failure to retry.
  """
  payload = ctx.payload or {}
  day_id = payload.get("group_plan_day_id")
  chat_id = payload.get("chat_id")
  if day_id is None or chat_id is None:
    raise ValueError("group_plan_day payload incomplete (send #%d)" % ctx.send.id)

  config = await ctx.store.groups.get_config(chat_id)
  plan = await ctx.store.groups.get_active_plan(chat_id)
  if config is None or config.status != CONFIG_ACTIVE or plan is None:
    return
  day = await ctx.store.groups.get_plan_day(int(day_id))
  if day is None:
    return
  claimed = await ctx.store.groups.claim_plan_day(day.id)
  if claimed is None:
    return                      # already delivered (restart between claim and mark)

  await _post_portion(ctx.bot, config, claimed)
  await _enqueue_next_group(ctx.store, chat_id, plan)


async def _post_portion(bot, config, day) -> None:
  """Post one portion to the group's topic: image, audio, translation, per flags."""
  from main import send_combined_audio, get_translation
  from lib.utils import File
  from lib.page_image import fetch_and_stitch

  flags = config.content_flags or {}
  thread = config.thread_id
  chat_id = config.chat_id
  file = File()
  base = dict(chat_id=chat_id)
  if thread is not None:
    base["message_thread_id"] = thread

  if flags.get("image", True):
    urls = [file.get_image_filename(day.surah, a)
            for a in range(day.start_ayah, day.end_ayah + 1)]
    try:
      image = await fetch_and_stitch(urls, name="portion.jpg")
      await bot.send_photo(photo=image, **base)
    except Exception as e:                       # a CDN hiccup must not sink audio+text
      print("HIFZ group: image post failed for %d: %s: %s"
            % (chat_id, type(e).__name__, e))

  if flags.get("translation", True):
    quran = await get_translation(config.translation_lang)
    text = quran.get_ayahs(day.surah, day.start_ayah, day.end_ayah)
    await bot.send_message(text=text[:4096], **base)

  if flags.get("audio", True):
    await send_combined_audio(bot, day.surah, day.start_ayah, day.end_ayah,
                              chat_id, config.reciter, message_thread_id=thread)


# --- J6: the group weekly board ------------------------------------------------

BOARD_KIND = "group_board"


async def group_board_entries(store, bot, chat_id: int, utc_now=None):
  """Ranked (user_id, name, sessions, streak) for this group's board, this week.

  Scoped to members who consented via the deep link *and* are still in the group:
  membership is re-checked with getChatMember at render time, so someone who left
  drops off the board without any explicit un-link. Sessions are counted in the
  group's own week window, ties broken by streak — the same rule as the personal
  board (H1).
  """
  from datetime import datetime, timezone
  from lib.leaderboard import week_window
  from lib.localtime import normalize_offset, DEFAULT_OFFSET

  config = await store.groups.get_config(chat_id)
  if config is None:
    return []
  offset = normalize_offset(config.timezone or DEFAULT_OFFSET)
  now = utc_now or datetime.now(timezone.utc)
  start, end = week_window(now, offset)

  entries = []
  for user_id in await store.groups.list_linked(chat_id):
    try:
      member = await bot.get_chat_member(chat_id, user_id)
      if getattr(member, "status", None) in ("left", "kicked", None):
        continue
    except telegram.error.TelegramError:
      continue                       # can't confirm membership -> leave them off
    sessions = await store.sessions.count_sessions(user_id, start, end)
    if sessions == 0:
      continue
    profile = await store.profiles.get_profile(user_id)
    name = getattr(profile, "display_name", None) or str(user_id)
    streak = getattr(profile, "current_streak", 0)
    entries.append((user_id, name, sessions, streak))

  entries.sort(key=lambda e: (-e[2], -e[3], e[0]))
  return entries


async def post_board(bot, store, chat_id: int, utc_now=None) -> None:
  """Render and post the weekly board into the group's topic."""
  config = await store.groups.get_config(chat_id)
  if config is None:
    return
  entries = await group_board_entries(store, bot, chat_id, utc_now)
  lines = [t("group_board_title", config.translation_lang)]
  if not entries:
    lines.append(t("group_board_empty", config.translation_lang))
  else:
    for rank, (_uid, name, sessions, _streak) in enumerate(entries[:10], start=1):
      lines.append(t("group_board_row", config.translation_lang).format(
          rank=rank, name=html.escape(name), sessions=sessions))
  base = dict(chat_id=chat_id, text="\n".join(lines))
  if config.thread_id is not None:
    base["message_thread_id"] = config.thread_id
  await bot.send_message(**base)


@send_handler(BOARD_KIND)
async def push_board(ctx) -> None:
  """Post the weekly board, then queue next week's."""
  chat_id = (ctx.payload or {}).get("chat_id")
  if chat_id is None:
    raise ValueError("group_board payload has no chat_id (send #%d)" % ctx.send.id)
  config = await ctx.store.groups.get_config(chat_id)
  if config is None or config.status != CONFIG_ACTIVE:
    return
  await post_board(ctx.bot, ctx.store, chat_id)
  await _enqueue_next_board(ctx.store, chat_id)


async def _enqueue_next_board(store, chat_id: int, now=None):
  """Queue the board for the end of the current group-local week at post time.

  Keyed by the week's Sunday so a restart cannot double-post it; `enqueue`
  answers None on a clash rather than raising.
  """
  from datetime import datetime, timezone, timedelta
  from lib.leaderboard import week_window
  from lib.localtime import to_utc, normalize_offset, DEFAULT_OFFSET
  from lib.scheduler import enqueue
  from lib.store.groups import CONFIG_ACTIVE as _ACTIVE
  from datetime import datetime as _dt, time as _time

  config = await store.groups.get_config(chat_id)
  if config is None or config.status != _ACTIVE:
    return None
  offset = normalize_offset(config.timezone or DEFAULT_OFFSET)
  post_time = config.post_time or _time(20, 0)
  now = now or datetime.now(timezone.utc)
  _start, end = week_window(now, offset)          # end = Sunday, local
  due_at = to_utc(_dt.combine(end, post_time), offset)
  if due_at <= now:                               # this week's slot has passed
    _start2, end2 = week_window(now + timedelta(days=7), offset)
    due_at = to_utc(_dt.combine(end2, post_time), offset)
    end = end2
  return await enqueue(store, BOARD_KIND, chat_id, due_at, local_day=end,
                       thread_id=config.thread_id, payload={"chat_id": chat_id})


async def _create_topic(bot, chat_id: int, name: str) -> Optional[int]:
  """createForumTopic, or None when the group is not a forum (J3 fallback b)."""
  try:
    topic = await bot.create_forum_topic(chat_id=chat_id, name=name)
    return topic.message_thread_id
  except telegram.error.TelegramError:
    return None


# A short spread of the group-flow languages actually translated (the policy:
# en/ru/uz/uz-Cyrl; everything else falls back to English). More can be typed
# later, but the picker only offers what is localized.
_GROUP_LANGS = (("en", "English"), ("ru", "Русский"),
                ("uz", "Oʻzbekcha"), ("uz-Cyrl", "Ўзбекча"))


def _lang_keyboard() -> InlineKeyboardMarkup:
  return InlineKeyboardMarkup(
      [[InlineKeyboardButton(label, callback_data="gr:tl:" + code)]
       for code, label in _GROUP_LANGS])


@callback("gr:")
async def on_group_tap(ctx: Ctx, cb_data: str) -> None:
  """Every `gr:` button. Parsed defensively; unknown shapes are acknowledged."""
  action, _, arg = cb_data[len("gr:"):].partition(":")
  draft = ctx.wiz.get(ctx.user_id)
  await ctx.answer()
  if draft is None:
    return
  if action == "tl":                                   # translation chosen
    await ctx.store.groups.update_config(
        draft["data"].get("chat_id"), translation_lang=arg or "en")
    ctx.wiz.update(ctx.user_id, step="target")
    await ctx.edit(ctx.tr("group_target_prompt"))
  elif action == "pace":                               # 0 = auto, else ayahs/day
    ctx.wiz.update(ctx.user_id, pace=int(arg) if arg.isdigit() else 0, step="days")
    await ctx.edit(ctx.tr("group_days_prompt"), reply_markup=_days_keyboard())
  elif action == "d":                                  # daily | weekdays
    days = list(range(1, 8)) if arg == "all" else [1, 2, 3, 4, 5]
    ctx.wiz.update(ctx.user_id, days=days, step="timezone")
    await ctx.edit(ctx.tr("group_timezone_prompt"), reply_markup=_offset_keyboard())
  elif action == "tz":                                 # utc offset chosen
    ctx.wiz.update(ctx.user_id, offset=arg or DEFAULT_OFFSET, step="post_time")
    await ctx.edit(ctx.tr("group_post_time_prompt"))


# --- J4: the group plan wizard (typed steps land in setup_step) ----------------

def _pace_keyboard() -> InlineKeyboardMarkup:
  row = [InlineKeyboardButton(t("group_btn_pace_auto", "en"), callback_data="gr:pace:0")]
  presets = [InlineKeyboardButton(str(n), callback_data="gr:pace:%d" % n)
             for n in (3, 5, 10)]
  return InlineKeyboardMarkup([row, presets])


def _days_keyboard() -> InlineKeyboardMarkup:
  return InlineKeyboardMarkup([[
      InlineKeyboardButton(t("group_btn_daily", "en"), callback_data="gr:d:all"),
      InlineKeyboardButton(t("group_btn_weekdays", "en"), callback_data="gr:d:wk")]])


def _offset_keyboard() -> InlineKeyboardMarkup:
  from lib.localtime import offset_options
  opts = offset_options()
  rows, row = [], []
  for off in opts:
    row.append(InlineKeyboardButton(off, callback_data="gr:tz:" + off))
    if len(row) == 4:
      rows.append(row); row = []
  if row:
    rows.append(row)
  return InlineKeyboardMarkup(rows)


# --- J6 (entry only): a member joins the board via deep link -------------------

async def _join_board(ctx: Ctx, chat_id: Optional[int]) -> None:
  config = await ctx.store.groups.get_config(chat_id) if chat_id is not None else None
  if config is None:
    await ctx.reply(ctx.tr("group_board_unknown"))
    return
  # Verify live membership: a link forwarded out of the group must not enroll a
  # non-member.
  try:
    member = await ctx.bot.get_chat_member(chat_id, ctx.user_id)
    is_member = getattr(member, "status", None) not in ("left", "kicked", None)
  except telegram.error.TelegramError:
    is_member = False
  if not is_member:
    await ctx.reply(ctx.tr("group_board_not_member"))
    return
  await ctx.store.groups.link_member(ctx.user_id, chat_id)
  await ctx.reply(ctx.tr("group_board_joined"))
