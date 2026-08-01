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
  """The one typed step: the forum-topic name."""
  draft = ctx.wiz.get(ctx.user_id)
  if draft is None or draft.get("step") != "topic":
    return
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
  await ctx.reply(ctx.tr("group_translation_prompt"),
                  reply_markup=_lang_keyboard())


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
  if action == "tl" and draft is not None:
    chat_id = draft["data"].get("chat_id")
    await ctx.store.groups.update_config(chat_id, translation_lang=arg or "en")
    await ctx.store.groups.update_config(chat_id, status=CONFIG_ACTIVE)
    ctx.wiz.clear(ctx.user_id)
    await ctx.answer()
    username = await bot_username(ctx.bot)
    board = _deep_link(username, BOARD_PREFIX + str(chat_id))
    await ctx.edit(ctx.tr("group_setup_done").format(board_link=board))
  else:
    await ctx.answer()


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
