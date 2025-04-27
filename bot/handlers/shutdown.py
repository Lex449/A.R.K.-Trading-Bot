"""
A.R.K. Shutdown Handler – Ultra Premium Build.
Safely and gracefully terminates the bot with full reporting.
"""

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
    Handles the /shutdown command.
    Gracefully shuts down the bot after notification.
    """
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Admin"

    try:
        # Notify user about the shutdown
        await update.message.reply_text(
            "⚠️ *A.R.K. Shutdown initiated...*\n\n"
            "_Saving session, closing tasks, terminating bot operations..._\n\n"
            "🛡️ Please wait...",
            parse_mode="Markdown"
        )
        logger.warning(f"/shutdown triggered by {user} (Chat ID: {chat_id})")

        # Short delay to ensure message delivery
        await asyncio.sleep(3)

        # Gracefully stop the application
        await context.application.stop()
        await context.application.shutdown()

        logger.info("✅ A.R.K. Bot shutdown completed successfully.")

    except Exception as e:
        logger.critical(f"Critical shutdown error: {e}")
        await report_error(context.bot, chat_id, e, context_info="Shutdown Handler Critical Error")
