"""
A.R.K. Daily Recap Job – Session Summary with Motivation.
Built for consistency, discipline, and user engagement.
"""

import logging
from telegram import Bot
from telegram.ext import ContextTypes
from bot.utils.session_tracker import get_session_report, reset_session_data
from bot.utils.error_reporter import report_error
from bot.utils.logger import setup_logger
from bot.config.settings import get_settings

# Setup structured logger
logger = setup_logger(__name__)

# Load configuration
config = get_settings()

async def daily_recap_job(context: ContextTypes.DEFAULT_TYPE):
    """
    Sends a daily trading session recap to Telegram.
    Resets session tracker after completion.
    """
    bot: Bot = context.bot
    chat_id = int(config["TELEGRAM_CHAT_ID"])

    try:
        logger.info("[Daily Recap] Starting daily recap...")

        # Retrieve session report
        session_summary = get_session_report()

        # Add motivational closure
        motivation_text = (
            "\n\n🌟 *Remember:* Every great trader was built by daily discipline.\n"
            "Stay the course. Tomorrow we level up again. 🚀"
        )

        # Full compiled message
        full_message = session_summary + motivation_text

        await bot.send_message(
            chat_id=chat_id,
            text=full_message,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

        logger.info("[Daily Recap] Successfully sent daily session recap.")

        # Reset session tracker
        reset_session_data()
        logger.info("[Daily Recap] Session tracker reset for next trading day.")

    except Exception as e:
        logger.error(f"[Daily Recap] Error while sending daily recap: {str(e)}")
        await report_error(bot, chat_id, e, context_info="Daily Recap Job")
