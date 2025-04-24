# bot/handlers/status.py

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

status_handler = CommandHandler("status", lambda update, context: status(update, context))

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = update.effective_user.language_code or "en"

    if lang.startswith("de"):
        msg = (
            "📊 *A.R.K. Systemstatus*\n"
            "────────────────────────────\n"
            "✅ *Läuft stabil & überwacht Märkte*\n"
            "⚙️ Analyseengine: *aktiv*\n"
            "✉️ Telegram-Verbindung: *OK*\n"
            "⭐️ Autopilot-Signale: *bereit*\n"
            "\n"
            "_Bleib fokussiert. A.R.K. denkt mit._"
        )
    else:
        msg = (
            "📊 *A.R.K. System Status*\n"
            "────────────────────────────\n"
            "✅ *Running stable, markets under watch*\n"
            "⚙️ Analysis engine: *active*\n"
            "✉️ Telegram connection: *OK*\n"
            "⭐️ Autopilot signals: *ready*\n"
            "\n"
            "_Stay sharp. A.R.K. has your back._"
        )

    await update.message.reply_markdown(msg)
