# bot/handlers/shutdown.py

import logging
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.error_reporter import report_error

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async def shutdown_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler for /shutdown command.
    Gracefully shuts down the bot after notifying the user.
    """
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Admin"

    try:
        await context.bot.send_message(
            chat_id=chat_id,
            text="⚠️ *Shutdown initiated.*\nThe bot will go offline shortly...",
            parse_mode="Markdown"
        )

        logger.warning(f"Shutdown command triggered by {user} (Chat ID: {chat_id})")

        # Kleine Pause für saubere Nachrichtensendung
        await asyncio.sleep(2)

        # Beende die Application
        await context.application.stop()
        await context.application.shutdown()
        logger.info("A.R.K. Bot shutdown successfully.")

    except Exception as e:
        await report_error(context.bot, chat_id, e, context_info="Shutdown Command Error")
        logger.error(f"Error during shutdown command: {e}")
