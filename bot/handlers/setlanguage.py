"""
A.R.K. Language Setter – Ultra Premium Build.
Allows users to dynamically change their language preference.
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.language import get_language, set_user_language
from bot.utils.i18n import get_text
from bot.utils.logger import setup_logger
from bot.utils.error_reporter import report_error

# Setup structured logger
logger = setup_logger(__name__)

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles /setlanguage command.
    Allows the user to change their preferred language dynamically.
    """
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"

    try:
        if not context.args:
            await update.message.reply_text(
                "🌐 Please specify a language: `/setlanguage en` or `/setlanguage de`",
                parse_mode="Markdown"
            )
            logger.warning(f"/setlanguage called without argument by {user}")
            return

        choice = context.args[0].lower()

        if choice in ("de", "deutsch"):
            lang = "de"
        elif choice in ("en", "english"):
            lang = "en"
        else:
            await update.message.reply_text(
                "❌ Unknown language. Available: `en`, `de`.",
                parse_mode="Markdown"
            )
            logger.warning(f"/setlanguage invalid choice '{choice}' by {user}")
            return

        # Save language in user context
        context.user_data["lang"] = lang
        set_user_language(chat_id, lang)  # Optional DB/save feature for future scaling

        confirmation = get_text("set_language_success", lang)

        await update.message.reply_text(
            f"✅ {confirmation}",
            parse_mode="Markdown"
        )

        logger.info(f"Language set to {lang} by {user} (Chat ID: {chat_id})")

    except Exception as e:
        logger.error(f"Error during /setlanguage by {user}: {e}")
        await report_error(context.bot, chat_id, e, context_info="/setlanguage command")
