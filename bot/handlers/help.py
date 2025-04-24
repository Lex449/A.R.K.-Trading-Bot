# /bot/handlers/help.py

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.utils.language import get_language

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_language(update)

    if lang == "de":
        message = (
            "🛠️ *A.R.K. Hilfe & Übersicht*\n"
            "--------------------------------------\n"
            "`/start` – Starte deine Session mit A.R.K.\n"
            "`/analyse` – Live-Marktscan aller Top-Indizes\n"
            "`/signal` – Einzel-Signal auf Abruf\n"
            "`/status` – Systemstatus prüfen\n"
            "`/recap` – Tagesrückblick erhalten\n"
            "`/shutdown` – Bot sicher herunterfahren\n\n"
            "📈 _A.R.K. denkt, scannt, filtert – du entscheidest._"
        )
    else:
        message = (
            "🛠️ *A.R.K. Help & Commands*\n"
            "--------------------------------------\n"
            "`/start` – Start your session with A.R.K.\n"
            "`/analyse` – Scan all major indices live\n"
            "`/signal` – Instant signal on request\n"
            "`/status` – System check\n"
            "`/recap` – Get today’s recap\n"
            "`/shutdown` – Shutdown the bot safely\n\n"
            "📈 _A.R.K. thinks, scans, filters – your call._"
        )

    await update.message.reply_markdown(message)

# === Handler exportieren ===
help_handler = CommandHandler("help", help_command)
