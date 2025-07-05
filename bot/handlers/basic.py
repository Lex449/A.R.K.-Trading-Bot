"""
Basis-Befehle: /start, /help, /ping
"""

from telegram import Update
from telegram.ext import ContextTypes


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👋 Willkommen bei A.R.K.! Nutze /help für Befehle."
    )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "/ping – Liveness-Test\n"
        "/help – Diese Hilfe\n"
        "/recap – Tageszusammenfassung (wenn aktiviert)"
    )


async def cmd_ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🏓 Pong")
