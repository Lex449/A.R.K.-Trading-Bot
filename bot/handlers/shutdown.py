import logging
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.error_reporter import report_error

# Setup logger for shutdown handler
logger = logging.getLogger(__name__)

async def shutdown_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Gracefully shuts down the bot after notifying the user.
    """
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Admin"

    try:
        await context.bot.send_message(
            chat_id=chat_id,
            text="⚠️ *Shutdown initiated.*\nThe bot will go offline shortly.",
            parse_mode="Markdown"
        )

        logger.warning(f"Shutdown command triggered by {user} (Chat ID: {chat_id})")

        # Wait a moment to ensure messages are delivered
        await asyncio.sleep(2)

        # Shutdown the application gracefully
        await context.application.stop()
        await context.application.shutdown()
        logger.info("✅ A.R.K. Bot shutdown completed.")

    except Exception as e:
        logger.error(f"Error during shutdown: {e}")
        await report_error(context.bot, chat_id, e, context_info="Shutdown Handler Error")
