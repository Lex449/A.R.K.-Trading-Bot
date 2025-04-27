"""
A.R.K. Ping Handler – Lightning Response & Stability Test.
Ultra Clean Build – Built like a Königsegg Jesko Absolut.
"""

import time
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.language import get_language
from bot.utils.i18n import get_text

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles /ping command.
    Measures and returns the bot's response latency.
    """
    chat_id = update.effective_chat.id
    lang = get_language(chat_id) or "en"

    start_time = time.time()
    sent_message = await update.message.reply_text(get_text("ping_check", lang))
    end_time = time.time()

    latency_ms = int((end_time - start_time) * 1000)

    pong_message = get_text("ping_pong", lang).format(latency=latency_ms)

    await sent_message.edit_text(pong_message, parse_mode="Markdown")
