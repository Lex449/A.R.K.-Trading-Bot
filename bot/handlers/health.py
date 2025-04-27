"""
A.R.K. Health Check – Minimalistic Ultra Build.
Checks if Bot runs stable.
"""

from telegram import Update
from telegram.ext import ContextTypes

async def health_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Responds to /health command with bot status.
    """
    try:
        await update.message.reply_text("✅ *A.R.K. Health Check:* System operational!", parse_mode="Markdown")
    except Exception:
        await update.message.reply_text("❌ *A.R.K. Health Check:* System error detected!", parse_mode="Markdown")
