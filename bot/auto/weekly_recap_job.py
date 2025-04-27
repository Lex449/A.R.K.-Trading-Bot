"""
A.R.K. Weekly Recap Job – Full Weekly Trading Summary with Motivation.
Built for traders who play the long game.
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

async def weekly_recap_job(context: ContextTypes.DEFAULT_TYPE):
    """
    Sends a full weekly trading session recap to Telegram.
    Resets session tracker afterward.
    """
    bot: Bot = context.bot
    chat_id = int(config["TELEGRAM_CHAT_ID"])

    try:
        logger.info("[Weekly Recap] Starting weekly recap...")

        # Retrieve session report
        session_summary = get_session_report()

        # Add weekly motivational closure
        motivation_text = (
            "\n\n🏆 *End of Week Reflections:*\n"
            "You survived another week in the markets. Not everyone does.\n"
            "Consistency, discipline, and focus are your real assets.\n\n"
            "Next week: Reset. Refocus. Reload. 🚀"
        )

        # Full compiled message
        full_message = (
            "📈 *A.R.K. Weekly Trading Recap*\n\n"
            f"{session_summary}\n\n"
            f"{motivation_text}"
        )

        await bot.send_message(
            chat_id=chat_id,
            text=full_message,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

        logger.info("[Weekly Recap] Successfully sent weekly session recap.")

        # Reset session tracker after weekly cycle
        reset_session_data()
        logger.info("[Weekly Recap] Session tracker reset after weekly cycle.")

    except Exception as e:
        logger.error(f"[Weekly Recap] Error while sending weekly recap: {str(e)}")
        await report_error(bot, chat_id, e, context_info="Weekly Recap Job")
