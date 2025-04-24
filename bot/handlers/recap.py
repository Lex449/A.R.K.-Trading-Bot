# bot/handlers/recap.py

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.utils.language import get_language

recap_handler = CommandHandler("recap", lambda update, context: recap(update, context))

async def recap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_language(update)

    if lang == "de":
        message = (
            "📊 *A.R.K. Tagesrückblick*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "Noch ist dieses Modul in Arbeit...\n\n"
            "In Kürze erhältst du hier automatisch:\n"
            "• Anzahl der Signale (Long/Short)\n"
            "• Qualität & Trefferquote\n"
            "• Deine persönliche Performance\n\n"
            "🛠️ _A.R.K. analysiert. Du wirst benachrichtigt, sobald alles bereit ist._"
        )
    else:
        message = (
            "📊 *A.R.K. Daily Recap*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "This feature is still under development...\n\n"
            "Soon you’ll receive:\n"
            "• Number of signals (Long/Short)\n"
            "• Quality & accuracy\n"
            "• Your personal performance\n\n"
            "🛠️ _A.R.K. is analyzing. You'll be notified as soon as it's ready._"
        )

    await update.message.reply_markdown(message)
