"""
A.R.K. Weekly Recap – Full Weekly Session + Motivation.
Built for elite long-term traders.
"""

from telegram import Bot
from bot.utils.session_tracker import get_weekly_report, reset_weekly_data
from bot.utils.logger import setup_logger
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings

# Setup Logger
logger = setup_logger(__name__)
config = get_settings()

async def weekly_recap_job(application, chat_id=None):
    """
    Sends weekly recap and resets weekly tracker.
    """
    try:
        bot = application.bot if application else Bot(token=config["BOT_TOKEN"])
        target_chat_id = chat_id or int(config["TELEGRAM_CHAT_ID"])

        weekly_report = get_weekly_report()

        motivation = (
            "\n\n🏆 *End of Week Reflection:*\n"
            "Success isn't built in a day, but momentum is.\n"
            "Reset. Refocus. Reload. 🚀"
        )

        message = f"📈 *Weekly Trading Recap*\n\n{weekly_report}{motivation}"

        await bot.send_message(
            chat_id=target_chat_id,
            text=message,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

        logger.info(f"✅ Weekly Recap sent successfully to {target_chat_id}.")

        # Reset Weekly Tracker
        reset_weekly_data()
        logger.info("♻️ Weekly session data reset successfully.")

    except Exception as e:
        await report_error(bot, chat_id, e, context_info="Weekly Recap Job")
        logger.error(f"❌ Error during Weekly Recap: {e}")
