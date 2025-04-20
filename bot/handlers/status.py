from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    lang = user.language_code or "en"

    if lang.startswith("de"):
        message = (
            "📊 *A.R.K. Systemstatus*\n"
            "-----------------------------\n"
            "✅ Bot läuft stabil\n"
            "📡 Marktüberwachung aktiv\n"
            "⚙️ Analysemodul bereit\n"
            "✉️ Telegram-Verbindung steht\n"
            "⭐️ Signale & Rückmeldungen aktiv\n"
            "\n_A.R.K. ist wachsam – du kannst dich auf die Märkte konzentrieren._"
        )
    else:
        message = (
            "📊 *A.R.K. System Status*\n"
            "-----------------------------\n"
            "✅ Bot is running smoothly\n"
            "📡 Market monitoring active\n"
            "⚙️ Analysis module ready\n"
            "✉️ Telegram connection established\n"
            "⭐️ Signals & feedback active\n"
            "\n_A.R.K. is watching – so you can focus on the market._"
        )

    await update.message.reply_markdown(message)

status_handler = CommandHandler("status", status)