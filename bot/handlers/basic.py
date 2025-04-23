from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.utils.language import get_language

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("✅ Bot is online! Ready for action.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    lang = get_language(update)

    if lang == "de":
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

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_language(update)

    if lang == "de":
        message = (
            "🛠️ *Hilfe & Übersicht*\n\n"
            "`/start` – Starte mit A.R.K.\n"
            "`/analyse` – Marktscan starten\n"
            "`/signal` – Aktuelles Signal holen\n"
            "`/status` – Bot-System prüfen\n"
            "`/recap` – Rückblick erhalten\n\n"
            "📣 _Tipp: Ruhige Hände – starke Entscheidungen._"
        )
    else:
        message = (
            "🛠️ *Help & Overview*\n\n"
            "`/start` – Launch A.R.K.\n"
            "`/analyse` – Market scan\n"
            "`/signal` – Get live signal\n"
            "`/status` – Bot system check\n"
            "`/recap` – Get daily recap\n\n"
            "📣 _Pro mindset. Smart entries._"
        )

    await update.message.reply_markdown(message)

ping_handler = CommandHandler("ping", ping)
status_handler = CommandHandler("status", status)
help_handler = CommandHandler("help", help_command)
