# bot/handlers/shutdown.py

import logging
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.error_reporter import report_error
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

async def shutdown_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler for /shutdown command.
    Gracefully shuts down the bot after notifying the admin.
    """
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Admin"

    try:
        # Vorwarnung senden
        await update.message.reply_text(
            "⚠️ *Shutdown initiated...*\nBot will terminate operations in a few seconds.",
            parse_mode="Markdown"
        )
        logger.warning(f"/shutdown triggered by {user} (Chat ID: {chat_id})")

        # kleine Pause für saubere Übertragung
        await asyncio.sleep(2)

        # Bot sauber stoppen
        await context.application.stop()
        await context.application.shutdown()

        logger.info("✅ Bot shutdown completed successfully.")

    except Exception as e:
        await report_error(context.bot, chat_id, e, context_info="Shutdown Handler Error")
        logger.critical(f"Critical error during shutdown: {e}")
