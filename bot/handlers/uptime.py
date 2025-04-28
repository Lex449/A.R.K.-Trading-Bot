"""
A.R.K. Uptime Handler – Ultra Premium Session Tracker.
Monitors and reports bot operational uptime with maximum safety and style.
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
    Sends real-time bot uptime information since session start.
    """

    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"

    try:
        if not os.path.exists(SESSION_FILE):
            await update.message.reply_text(
                "ℹ️ *Uptime Info:*\n_No active session data available yet._",
                parse_mode="Markdown"
            )
            logger.warning(f"[Uptime] No session_data.json found (User: {user}).")
            return

        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            session_data = json.load(f)

        start_time_iso = session_data.get("start_time")
        if not start_time_iso:
            await update.message.reply_text(
                "⚠️ *Uptime Error:*\n_Session start time missing._",
                parse_mode="Markdown"
            )
            logger.error(f"[Uptime] Start time missing (User: {user}).")
            return

        start_time = datetime.fromisoformat(start_time_iso)
        now = datetime.utcnow()
        uptime_duration = now - start_time

        days = uptime_duration.days
        hours, remainder = divmod(uptime_duration.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        uptime_str = f"{days}d {hours}h {minutes}m" if days else f"{hours}h {minutes}m"

        # Build clean uptime message
        message = (
            f"⏱️ *A.R.K. Session Uptime*\n\n"
            f"`{uptime_str}`\n\n"
            "_Relentless precision. Relentless progress._"
        )

        await update.message.reply_text(
            message,
            parse_mode="Markdown"
        )

        logger.info(f"[Uptime] Uptime sent to {user} → {uptime_str}.")

    except Exception as e:
        logger.critical(f"[Uptime] Critical error retrieving uptime: {e}")
        await update.message.reply_text(
            "❌ *Critical Error:*\n_Unable to retrieve uptime information._",
            parse_mode="Markdown"
        )
        await report_error(context.bot, chat_id, e, context_info="Uptime Handler Failure")
