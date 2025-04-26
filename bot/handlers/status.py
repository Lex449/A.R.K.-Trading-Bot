# bot/handlers/status.py

import logging
from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime
import pytz
from bot.utils.session_tracker import get_session_summary
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.error_reporter import report_error
from bot.utils.market_time import is_trading_day, is_trading_hours

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler for /status command.
    Provides a live session summary including total signals, market status, and uptime.
    """
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"

    try:
        # Session Zusammenfassung holen
        summary_text = get_session_summary()

        # Aktuelle NY Zeit holen
        now_ny = datetime.now(pytz.timezone('America/New_York'))
        time_ny = now_ny.strftime("%H:%M:%S")

        # Marktstatus prüfen
        trading_day = is_trading_day()
        trading_hours = is_trading_hours()

        market_status = "✅ Market Open" if trading_day and trading_hours else "❌ Market Closed"
        day_status = "🗓️ Trading Day" if trading_day else "🛑 No Trading (Weekend or Holiday)"

        # Status Nachricht bauen
        message = (
            f"🔎 *Session Status for {user}*\n\n"
            f"{summary_text}\n\n"
            f"🕒 *New York Time:* `{time_ny}`\n"
            f"{day_status}\n"
            f"{market_status}\n\n"
            f"🚀 *Stay sharp. Manage your risk.*"
        )

        await context.bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")

        logger.info(f"Status requested by {user} (Chat ID: {chat_id})")

    except Exception as e:
        await report_error(context.bot, chat_id, e, context_info="Status Command Error")
        logger.error(f"Error during status command: {e}")
