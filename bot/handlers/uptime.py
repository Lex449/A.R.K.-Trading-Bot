"""
A.R.K. Uptime Handler – Tracks and displays Bot session uptime.
Ultra Premium Build: Clean, Safe, Elegant.
"""

import os
import json
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.logger import setup_logger
from bot.utils.error_reporter import report_error

# Setup structured logger
logger = setup_logger(__name__)

# Session file location
SESSION_FILE = "session_data.json"

async def uptime(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles /uptime command.
    Provides the bot's operational uptime since last session start.
    """
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"

    try:
        if not os.path.exists(SESSION_FILE):
            await update.message.reply_text(
                "ℹ️ *Uptime Data:* No session data available yet.",
                parse_mode="Markdown"
            )
            logger.warning(f"Uptime request but session_data.json not found (User: {user})")
            return

        # Load session data
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            session_data = json.load(f)

        start_time_iso = session_data.get("start_time")
        if not start_time_iso:
            await update.message.reply_text(
                "⚠️ *Error:* Start time missing in session data.",
                parse_mode="Markdown"
            )
            logger.error(f"Session start time missing (User: {user})")
            return

        start_time = datetime.fromisoformat(start_time_iso)
        now = datetime.utcnow()
        uptime_duration = now - start_time

        days = uptime_duration.days
        hours, remainder = divmod(uptime_duration.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        uptime_str = f"{days}d {hours}h {minutes}m" if days else f"{hours}h {minutes}m"

        # Reply with uptime info
        await update.message.reply_text(
            f"⏱️ *A.R.K. Uptime:*\n\n`{uptime_str}`",
            parse_mode="Markdown"
        )

        logger.info(f"Uptime sent to {user} (Uptime: {uptime_str})")

    except Exception as e:
        await update.message.reply_text(
            "❌ *Critical Error:* Unable to retrieve uptime data.",
            parse_mode="Markdown"
        )
        await report_error(context.bot, chat_id, e, context_info="Uptime Handler Error")
        logger.critical(f"Critical error retrieving uptime: {e}")
