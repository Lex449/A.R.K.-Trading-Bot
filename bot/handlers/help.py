# bot/handlers/help.py

from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.logger import setup_logger
from bot.utils.error_reporter import report_error

# Setup structured logger
logger = setup_logger(__name__)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler for /help command.
    Sends the available command list to the user.
    """
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"
    lang = get_language(chat_id)

    logger.info(f"/help command requested by {user} (Chat ID: {chat_id})")

    try:
        help_text = get_text("help", lang)

        await context.bot.send_message(
            chat_id=chat_id,
            text=help_text,
            parse_mode="Markdown"
        )

        logger.info(f"Help information sent to {user}")

    except Exception as e:
        await report_error(context.bot, chat_id, e, context_info="Help Command Error")
        logger.error(f"Error during help command: {e}")
