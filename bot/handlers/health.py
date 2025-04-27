"""
A.R.K. Health Check – Minimalistic Ultra Build.
Checks if the bot runs stable like a Königsegg Jesko Absolut.
"""

from telegram import Update
from telegram.ext import ContextTypes

async def health_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Responds to /health command with bot status.
    Ultra-minimalistic, ultra-stable response.
    """
    try:
        await update.message.reply_text(
            "✅ *A.R.K. Health Check:* System operational!",
            parse_mode="Markdown"
        )
    except Exception as e:
        await update.message.reply_text(
            "❌ *A.R.K. Health Check:* System error detected!",
            parse_mode="Markdown"
        )
        raise e  # Fehler sauber nach oben werfen für globales Handling
