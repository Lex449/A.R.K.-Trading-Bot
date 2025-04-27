"""
A.R.K. Daily Recap – Session Summary + Motivation.
Perfect for disciplined traders who build success daily.
"""

from telegram import Bot
from bot.utils.session_tracker import get_today_report, reset_today_data
from bot.utils.logger import setup_logger
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings

# Setup Logger
logger = setup_logger(__name__)
config = get_settings()

async def daily_recap_job(application, chat_id=None):
    """
    Sends daily recap and resets today's tracker.
    """
    try:
        bot = application.bot if application else Bot(token=config["BOT_TOKEN"])
        target_chat_id = chat_id or int(config["TELEGRAM_CHAT_ID"])

        today_report = get_today_report()

        motivation = (
            "\n\n🌟 *Remember:* Consistency beats luck.\n"
            "Tomorrow we rise sharper and stronger. 🚀"
        )

        message = f"{today_report}{motivation}"

        await bot.send_message(
            chat_id=target_chat_id,
            text=message,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

        logger.info(f"✅ Daily Recap sent successfully to {target_chat_id}.")

        # Reset Today Tracker
        reset_today_data()
        logger.info("♻️ Today's session data reset successfully.")

    except Exception as e:
        await report_error(bot, chat_id, e, context_info="Daily Recap Job")
        logger.error(f"❌ Error during Daily Recap: {e}")
