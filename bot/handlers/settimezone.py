import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.user_timezone_manager import set_user_timezone, list_available_timezones
from bot.utils.error_reporter import report_error
from bot.utils.logger import setup_logger
from bot.utils.i18n import get_text

# Setup Logger
logger = setup_logger(__name__)

async def set_timezone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the /settimezone command.
    Allows the user to set their timezone dynamically.
    """
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"
    language = get_language(chat_id) or "en"

    try:
        # If no argument is provided, show available options
        if not context.args:
            timezone_list = list_available_timezones()
            available_timezones = "\n".join([f"`{tz}`" for tz in timezone_list])
            await update.message.reply_text(
                f"❗ {get_text('settimezone_no_argument', language)}\n\n{get_text('timezone_example', language)}\n\n{get_text('timezone_available', language)}:\n{available_timezones}",
                parse_mode="Markdown"
            )
            return

        timezone = context.args[0]

        # Check and set the user's timezone
        if set_user_timezone(chat_id, timezone):
            await update.message.reply_text(
                f"✅ {get_text('settimezone_success', language).format(timezone=timezone)}",
                parse_mode="Markdown"
            )
            logger.info(f"Timezone set for {user} ({chat_id}) → {timezone}")
        else:
            await update.message.reply_text(
                f"⚠️ {get_text('settimezone_invalid', language)}\n{get_text('settimezone_use_list', language)}",
                parse_mode="Markdown"
            )
            logger.warning(f"Invalid timezone input by {user}: {timezone}")

    except Exception as e:
        # Report error and log the issue
        await report_error(context.bot, chat_id, e, context_info="/settimezone command failure")
        logger.error(f"Error in /settimezone for user {user} ({chat_id}): {e}")
