"""Reading the caller's durable settings at the start of an update."""

from locales import normalize_lang
from services.user_settings import UserSettings


async def resolve_settings(user_settings: UserSettings, chat_id, user_id, lang_hint=None):
    """Return the caller's durable settings (ui_lang, translation_lang, reciter),
    detecting a UI language from the client's `lang_hint` on first contact.

    `chat_id` may be None for inline-query callers (no chat exists yet); in that
    case the legacy-Redis migration step inside UserSettings is simply skipped.
    """
    default_ui_lang = normalize_lang(lang_hint)
    return await user_settings.get(user_id, chat_id, default_ui_lang=default_ui_lang)
