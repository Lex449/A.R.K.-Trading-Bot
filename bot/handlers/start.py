import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.language import get_language
from bot.utils.i18n import get_text

# Setup logger for start handler
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Greets the user and provides an introduction to the bot.
    """
    user = update.effective_user.first_name or "Trader"
    lang = get_language(update)

    greeting = get_text("start", lang).format(user=user)
    help_text = get_text("help", lang)

    try:
        await update.message.reply_text(f"{greeting}\n\n{help_text}", parse_mode="Markdown")
        logger.info(f"✅ Start command handled successfully for {user}")
    except Exception as e:
        logger.error(f"❌ Error in start command: {e}")
