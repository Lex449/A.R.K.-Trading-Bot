"""
A.R.K. Monitor Command – Real-Time API Usage Status
Displays current API usage rate and system call count.
"""

from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.usage_monitor import usage_monitor
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.logger import setup_logger

logger = setup_logger(__name__)

async def monitor_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        chat_id = update.effective_chat.id
        lang = get_language(chat_id)

        call_count = usage_monitor.get_call_count()
        rate = usage_monitor.get_rate_per_minute()
        duration = usage_monitor.get_elapsed_minutes()

        # Optional: Bewertung je nach Rate
        if rate < 75:
            emoji = "🟢"
            comment = "Safe"
        elif rate < 140:
            emoji = "🟡"
            comment = "Caution"
        else:
            emoji = "🔴"
            comment = "CRITICAL – Reduce usage!"

        msg = (
            f"{emoji} *API Usage Monitor*\n\n"
            f"*Total Calls:* `{call_count}`\n"
            f"*Uptime:* `{duration:.1f} min`\n"
            f"*Calls/min:* `{rate:.2f}`\n"
            f"*Status:* `{comment}`\n\n"
            "_Auto-monitoring is active._"
        )

        await update.message.reply_text(msg, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"[MonitorCommand] Failed: {e}")
        await update.message.reply_text("⚠️ Error loading monitor status.")
