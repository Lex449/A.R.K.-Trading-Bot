"""
A.R.K. Set Timezone Handler – Global Scaling Feature.
Allows users to customize their timezone individually.
"""

from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.user_timezone_manager import set_user_timezone, list_available_timezones
from bot.utils.error_reporter import report_error
from bot.utils.logger import setup_logger

# Setup Logger
logger = setup_logger(__name__)

async def set_timezone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"

    try:
        if not context.args:
            await update.message.reply_text(
                "❗ Please provide a timezone.\n\nExample: `/settimezone Europe/Berlin`\n\nUse `/listtimezones` to see all options.",
                parse_mode="Markdown"
            )
            return

        timezone = context.args[0]

        if set_user_timezone(chat_id, timezone):
            await update.message.reply_text(f"✅ Timezone set to `{timezone}` successfully!", parse_mode="Markdown")
            logger.info(f"Timezone set for {user} ({chat_id}) → {timezone}")
        else:
            await update.message.reply_text(
                "⚠️ Invalid timezone.\nUse `/listtimezones` to see all available options.",
                parse_mode="Markdown"
            )
            logger.warning(f"Invalid timezone input by {user}: {timezone}")

    except Exception as e:
        await report_error(context.bot, chat_id, e, context_info="/settimezone command failure")
        logger.error(f"Error in /settimezone: {e}")
