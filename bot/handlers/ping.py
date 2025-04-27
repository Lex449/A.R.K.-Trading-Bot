"""
A.R.K. Ping Handler – Lightning-fast Response Check.
"""

from telegram import Update
from telegram.ext import ContextTypes
import time

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Responds to /ping command with response time.
    """
    start_time = time.time()
    sent_message = await update.message.reply_text("🏓 Pinging...")
    end_time = time.time()

    latency_ms = int((end_time - start_time) * 1000)

    await sent_message.edit_text(f"🏓 *Pong!* Response time: `{latency_ms} ms`", parse_mode="Markdown")
