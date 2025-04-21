# bot/handlers/help.py

from telegram import Update
from telegram.ext import ContextTypes

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = update.effective_user.language_code or "en"

    if lang.startswith("de"):
        message = (
            "🛠️ *Hilfe & Übersicht*

"
            "`/start` – Starte mit A.R.K.
"
            "`/analyse` – Marktscan starten
"
            "`/signal` – Aktuelles Signal holen
"
            "`/status` – Bot-System prüfen
"
            "`/recap` – Rückblick erhalten
"
            "
📣 _Tipp: Ruhige Hände – starke Entscheidungen._"
        )
    else:
        message = (
            "🛠️ *Help & Overview*

"
            "`/start` – Launch A.R.K.
"
            "`/analyse` – Market scan
"
            "`/signal` – Get live signal
"
            "`/status` – Bot system check
"
            "`/recap` – Get daily recap
"
            "
📣 _Pro mindset. Smart entries._"
        )

    await update.message.reply_markdown(message))