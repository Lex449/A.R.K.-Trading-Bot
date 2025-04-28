"""
A.R.K. Daily Recap Engine – Ultra Session Wrap-Up Build.
Provides clean daily summaries, psychological reinforcement, and automatic session resets.

Built for: Disciplined Traders, Long-Term Growth, and Maximum Efficiency.
"""

from telegram import Bot
from bot.utils.session_tracker import get_today_report, reset_today_data
from bot.utils.logger import setup_logger
from bot.utils.error_reporter import report_error
from bot.utils.i18n import get_text
from bot.utils.language import get_language
from bot.config.settings import get_settings

# Setup Logger
logger = setup_logger(__name__)
config = get_settings()

async def daily_recap_job(application, chat_id=None):
    """
    Sends the daily session summary to the user and resets today's tracking stats.
    """

    try:
        lang = get_language(chat_id) or "en"

        bot = application.bot if application else Bot(token=config["BOT_TOKEN"])
        target_chat_id = chat_id or int(config["TELEGRAM_CHAT_ID"])

        # === Fetch today's performance report ===
        today_report = get_today_report()

        # === Motivational Closing ===
        motivation_text = get_text("daily_motivation", lang) or (
            "\n\n🌟 *Consistency beats talent.*\n"
            "Tomorrow we level up even sharper. 🚀"
        )

        full_message = f"{today_report}{motivation_text}"

        # === Send the Recap ===
        await bot.send_message(
            chat_id=target_chat_id,
            text=full_message,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
        logger.info(f"✅ Daily Recap sent successfully to {target_chat_id}.")

        # === Reset today's session for a clean start ===
        reset_today_data()
        logger.info("♻️ Today's session tracker reset successfully.")

    except Exception as e:
        logger.error(f"❌ [Daily Recap Job] Critical error: {e}")
        await report_error(bot, chat_id or int(config["TELEGRAM_CHAT_ID"]), e, context_info="Daily Recap Job Failure")
