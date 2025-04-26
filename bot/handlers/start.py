# bot/handlers/start.py

from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.error_reporter import report_error
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler for /start command.
    Greets the user and provides initial bot instructions.
    """
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"
    lang = get_language(chat_id) or "en"

    try:
        greeting = get_text("start_greeting", lang).format(user=user)
        help_hint = get_text("start_help_hint", lang)

        await update.message.reply_text(
            f"{greeting}\n\n{help_hint}",
            parse_mode="Markdown"
        )

        logger.info(f"Start command triggered by {user} (Chat ID: {chat_id})")

    except Exception as e:
        await report_error(context.bot, chat_id, e, context_info="Start Command Error")
        logger.error(f"Error in /start command: {e}")
