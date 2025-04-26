# bot/handlers/setlanguage.py

import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.i18n import get_text
from bot.utils.language import set_user_language
from bot.utils.error_reporter import report_error

# Setup Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler for /setlanguage command.
    Allows the user to change the preferred bot language.
    """
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "User"

    try:
        if not context.args:
            await update.message.reply_text("Please specify a language: `/setlanguage en` or `/setlanguage de`", parse_mode="Markdown")
            return

        choice = context.args[0].lower()
        success = set_user_language(chat_id, choice)

        if success:
            await update.message.reply_text(f"✅ Language successfully set to `{choice}`.", parse_mode="Markdown")
            logger.info(f"Language updated to {choice} for {user} (Chat ID: {chat_id})")
        else:
            await update.message.reply_text("❌ Invalid language option. Please use 'en' or 'de'.", parse_mode="Markdown")
            logger.warning(f"Invalid language choice by {user} (Chat ID: {chat_id})")

    except Exception as e:
        await report_error(context.bot, chat_id, e, context_info="Set Language Command Error")
        logger.error(f"Error in set_language command for {user}: {e}")
