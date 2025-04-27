"""
A.R.K. Uptime Handler – Tracks Bot Session Uptime.
"""

from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime
import os
import json

# Session File Location
SESSION_FILE = "session_data.json"

async def uptime(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Responds to /uptime command with bot uptime.
    """
    try:
        if not os.path.exists(SESSION_FILE):
            await update.message.reply_text("ℹ️ Uptime data not available.")
            return

        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            session_data = json.load(f)

        start_time = datetime.fromisoformat(session_data.get("start_time"))
        now = datetime.utcnow()
        uptime_duration = now - start_time

        days = uptime_duration.days
        hours, remainder = divmod(uptime_duration.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        uptime_str = f"{days}d {hours}h {minutes}m" if days > 0 else f"{hours}h {minutes}m"

        await update.message.reply_text(f"⏱️ *Uptime:* `{uptime_str}`", parse_mode="Markdown")

    except Exception:
        await update.message.reply_text("⚠️ Error retrieving uptime data.", parse_mode="Markdown")
