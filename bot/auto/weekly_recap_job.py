"""
A.R.K. Weekly Recap – Full Strategic Reflection and Reset Engine.
Engineered for elite traders to sharpen long-term consistency and mindset.
"""

from telegram import Bot
from bot.utils.session_tracker import get_weekly_report, reset_weekly_data
from bot.utils.logger import setup_logger
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings
from bot.utils.i18n import get_text
from bot.utils.language import get_language

# Setup structured logger
logger = setup_logger(__name__)
config = get_settings()

async def weekly_recap_job(application, chat_id=None):
    """
    Sends a detailed weekly performance recap + motivational reset.
    Also resets weekly session data.
    """

    try:
        bot = application.bot if application else Bot(token=config["BOT_TOKEN"])
        target_chat_id = chat_id or int(config["TELEGRAM_CHAT_ID"])

        lang = get_language(target_chat_id) or "en"

        # === Retrieve Weekly Report ===
        weekly_report = get_weekly_report()

        # === Motivational End of Week Text ===
        motivation = get_text("weekly_motivation", lang) or (
            "\n\n🏆 *Weekly Reflection:*\n"
            "_Winners reset, refocus, and reload._\n"
            "The market waits for no one. 🚀"
        )

        # === Full Message Composition ===
        message = (
            f"📈 *Weekly Trading Recap*\n\n"
            f"{weekly_report}"
            f"{motivation}"
        )

        # === Send Recap Message ===
        await bot.send_message(
            chat_id=target_chat_id,
            text=message,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

        logger.info(f"✅ Weekly Recap successfully sent to {target_chat_id}.")

        # === Reset Weekly Session Tracker ===
        reset_weekly_data()
        logger.info(f"♻️ Weekly session data reset successfully for {target_chat_id}.")

    except Exception as e:
        await report_error(
            application.bot if application else Bot(token=config["BOT_TOKEN"]),
            chat_id or int(config["TELEGRAM_CHAT_ID"]),
            e,
            context_info="Weekly Recap Job"
        )
        logger.error(f"❌ Critical error during Weekly Recap: {e}")
