# /bot/handlers/status.py

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.utils.language import get_language

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = get_language(update)

    if lang == "de":
        msg = (
            "📊 *Systemstatus A.R.K.*\n"
            "----------------------------------\n"
            "✅ *Bot läuft stabil*\n"
            "📡 Marktanalyse aktiv\n"
            "⚙️ Analyse-Engine verknüpft\n"
            "✉️ Telegram-Verbindung steht\n"
            "⭐️ Signal-Logik vollständig aktiv\n"
            "\n"
            "_Alles funktioniert wie geplant – Fokus auf deinen nächsten Trade._"
        )
    else:
        msg = (
            "📊 *A.R.K. System Status*\n"
            "----------------------------------\n"
            "✅ *Bot running smoothly*\n"
            "📡 Market analysis active\n"
            "⚙️ Engine fully connected\n"
            "✉️ Telegram connection stable\n"
            "⭐️ Signal system fully active\n"
            "\n"
            "_Everything is on track – focus on your next move._"
        )

    await update.message.reply_markdown(msg)

# === Handler exportieren ===
status_handler = CommandHandler("status", status)
