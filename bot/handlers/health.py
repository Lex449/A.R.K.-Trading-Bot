"""
A.R.K. Health Check Handler – Ultra Premium Resilience Build.
Provides bilingual system health confirmation with maximum reliability.
"""

from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.logger import setup_logger
from bot.utils.error_reporter import report_error

# Setup structured logger
logger = setup_logger(__name__)

async def health_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Responds to the /health command.
    Bilingual, ultra-stable, clean design.
    """
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"
    lang = get_language(chat_id) or "en"

    try:
        # Compose success message
        health_message = get_text("health_ok", lang) or "✅ *System Health Check:* All systems operational."
        
        await update.message.reply_text(
            health_message,
            parse_mode="Markdown"
        )

        logger.info(f"[HealthCheck] System health confirmed for {user} (Chat ID: {chat_id}).")

    except Exception as e:
        # Compose fallback error message
        fallback_message = get_text("health_fail", lang) or "❌ *System Health Check:* Failure detected."

        await update.message.reply_text(
            fallback_message,
            parse_mode="Markdown"
        )

        logger.error(f"[HealthCheck] Health check failed for {user}: {e}")

        # Report the error via Telegram alert system
        await report_error(context.bot, chat_id, e, context_info="Health Check Command Error")
