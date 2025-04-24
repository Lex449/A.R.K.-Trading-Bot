# bot/handlers/help.py

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.utils.language import get_language

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_language(update)

    if lang == "de":
        message = (
            "🧠 *A.R.K. Hilfe & Übersicht*\n"
            "-------------------------------------\n"
            "`/start` – Starte den Trading-Mentor\n"
            "`/analyse` – Live-Marktüberblick mit Ranking\n"
            "`/signal` – Konkretes Einstiegssignal abrufen\n"
            "`/status` – System-Check deines A.R.K. Bots\n"
            "`/recap` – Täglicher Rückblick (bald)\n"
            "`/shutdown` – Bot manuell stoppen (nur Admin)\n\n"
            "📣 _Tipp: Ruhige Hände, klare Signale. A.R.K. denkt für dich mit._\n"
            "💬 Feedback? Community? → [Telegram-Channel](https://t.me/arktradingcommunity)"
        )
    else:
        message = (
            "🧠 *A.R.K. Help & Commands*\n"
            "-------------------------------------\n"
            "`/start` – Launch your trading mentor\n"
            "`/analyse` – Live market scan & signal ranking\n"
            "`/signal` – Get your current entry signal\n"
            "`/status` – System diagnostics & uptime check\n"
            "`/recap` – Daily review (coming soon)\n"
            "`/shutdown` – Shutdown command (admin only)\n\n"
            "📣 _Tip: Stay patient. Precision wins. Let A.R.K. do the thinking._\n"
            "💬 Feedback or support? → [Telegram Community](https://t.me/arktradingcommunity)"
        )

    await update.message.reply_markdown(message)

help_handler = CommandHandler("help", help_command)
