# bot/handlers/global_error_handler.py

"""
A.R.K. Global Error Handler – Ultra Diamond Defense
Fängt ALLE unhandled Errors im System sicher ab und meldet sie sofort.
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings
from bot.utils.logger import setup_logger

# Setup Structured Logger
logger = setup_logger(__name__)
config = get_settings()

async def global_error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Globale Catch-All Error-Handler-Funktion.
    Jede unvorhergesehene Exception wird hier sicher aufgefangen und gemeldet.
    """
    bot = context.bot
    fallback_chat_id = int(config["TELEGRAM_CHAT_ID"])

    try:
        error = context.error
        chat_id = fallback_chat_id

        if update and hasattr(update, "effective_chat") and update.effective_chat:
            chat_id = update.effective_chat.id

        logger.error(f"⚠️ [GlobalError] {error}")

        # Fehler sauber reporten
        await report_error(bot, chat_id, error, context_info="Global Handler Exception")

        # Nutzer optional über Fehler informieren
        if update and hasattr(update, "message") and update.message:
            await update.message.reply_text(
                text="⚠️ *Oops, something went wrong!* Our team has been notified.",
                parse_mode="Markdown"
            )

        logger.info(f"✅ [GlobalErrorHandler] Error processed successfully for Chat ID: {chat_id}")

    except Exception as fallback_error:
        # Falls der Error Handler selbst crasht
        logger.critical(f"🔥 [Fatal Crash in GlobalErrorHandler] {repr(fallback_error)}")
        await report_error(bot, fallback_chat_id, fallback_error, context_info="Fatal Crash in Global ErrorHandler")
