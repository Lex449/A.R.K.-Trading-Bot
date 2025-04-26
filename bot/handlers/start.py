# bot/handlers/start.py

from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.logger import setup_logger
from bot.config.settings import get_settings
from bot.utils.error_reporter import report_error

# Setup structured logger
logger = setup_logger(__name__)

# Load configuration
config = get_settings()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler for /start command.
    Greets the user and explains basic usage.
    """
    user = update.effective_user.first_name or "Trader"
    chat_id = update.effective_chat.id
    lang = get_language(chat_id)

    logger.info(f"/start command triggered by {user} (Chat ID: {chat_id})")

    try:
        greeting = get_text("start", lang).format(user=user)
        help_text = get_text("help", lang)

        await context.bot.send_message(
            chat_id=chat_id,
            text=f"{greeting}\n\n{help_text}",
            parse_mode="Markdown"
        )

        logger.info(f"Start greeting and help sent to {user}")

    except Exception as e:
        await report_error(context.bot, chat_id, e, context_info="Start Command Error")
        logger.error(f"Error during start command: {e}")
