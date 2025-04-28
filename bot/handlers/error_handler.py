import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings
from bot.utils.language import get_language
from bot.utils.i18n import get_text

# Setup Logger
logger = logging.getLogger(__name__)
config = get_settings()

async def global_error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Catches and reports ALL unhandled errors from the Telegram application.
    Guarantees maximum bot uptime and smooth crash reporting.
    Optimized for ultra-stability and multilingual support.
    """
    try:
        # Extract error details
        error = context.error
        chat_id = int(config["TELEGRAM_CHAT_ID"])

        # Retrieve user language for localized error reporting
        lang = get_language(update.effective_chat.id) or "en"

        # Log the error in the system logs with full details
        logger.error(f"⚠️ [Global Error] {error}")

        # Prepare error message for user-friendly reporting
        error_message = get_text("global_error_report", lang).format(error=str(error))

        # Send the error report via Telegram to the admin
        await report_error(context.bot, chat_id, error, context_info="Global Bot Error")
        
        # Send a localized error message to the user if appropriate
        if update:
            await update.message.reply_text(error_message, parse_mode="Markdown")
        
        # Optionally notify the user that the issue is being investigated
        logger.info(f"⚠️ [Error Handler] Error successfully reported to admin for chat ID: {chat_id}")

    except Exception as critical_failure:
        # Critical failure when trying to handle the original error
        logger.critical(f"🚨 [Critical Failure] Error inside Global Error Handler: {critical_failure}")
        # Report to admin if critical failure occurs in error handler
        await report_error(context.bot, chat_id, critical_failure, context_info="Critical Failure in Global Error Handler")
