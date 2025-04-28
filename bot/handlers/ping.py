"""
A.R.K. Ping Handler – Lightning Response & Stability Test.
Ultra Clean Build – Built like a Königsegg Jesko Absolut.
"""

import time
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.error_reporter import report_error
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles /ping command.
    Measures and returns the bot's response latency.
    """
    chat_id = update.effective_chat.id
    lang = get_language(chat_id) or "en"

    try:
        # Measure time taken to respond
        start_time = time.time()
        sent_message = await update.message.reply_text(get_text("ping_check", lang))
        end_time = time.time()

        # Calculate latency in milliseconds
        latency_ms = int((end_time - start_time) * 1000)

        # Prepare response message with latency
        pong_message = get_text("ping_pong", lang).format(latency=latency_ms)

        # Edit the message to display latency information
        await sent_message.edit_text(pong_message, parse_mode="Markdown")

        # Log the ping request and response latency
        logger.info(f"[Ping] Latency for {chat_id}: {latency_ms}ms")

    except Exception as e:
        # If an error occurs, report it and inform the user
        await report_error(context.bot, chat_id, e, context_info="Ping Command Error")
        logger.error(f"[Ping Error] Error occurred during ping: {e}")
        await update.message.reply_text(
            get_text("ping_error", lang), parse_mode="Markdown"
        )
