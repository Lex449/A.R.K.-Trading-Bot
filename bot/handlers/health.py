"""
A.R.K. Health Check – Ultra Bilingual Version
Ensures the bot runs as flawlessly as a Koenigsegg Jesko Absolut.
"""

from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.language import get_language
from bot.utils.i18n import get_text

async def health_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Responds to the /health command.
    Bilingual, stable, minimalistic.
    """
    chat_id = update.effective_chat.id
    lang = get_language(chat_id) or "en"

    try:
        await update.message.reply_text(
            get_text("health_ok", lang),
            parse_mode="Markdown"
        )
    except Exception:
        await update.message.reply_text(
            get_text("health_fail", lang),
            parse_mode="Markdown"
        )
        raise  # Fehler sauber an global_error_handler weiterreichen
