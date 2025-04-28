import logging
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.error_reporter import report_error
from bot.utils.logger import setup_logger
from bot.utils.i18n import get_text

# Setup structured logger
logger = setup_logger(__name__)

async def shutdown_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the /shutdown command.
    Gracefully shuts down the bot after notification.
    """
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Admin"
    language = get_language(chat_id) or "en"

    try:
        # Notify user about the shutdown
        shutdown_message = get_text("shutdown_message", language)

        await update.message.reply_text(
            shutdown_message,
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
