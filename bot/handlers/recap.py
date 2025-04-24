# bot/handlers/recap.py

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

recap_handler = CommandHandler("recap", lambda update, context: recap(update, context))

async def recap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "📊 *A.R.K. Daily Recap*\n"
        "-----------------------------\n"
        "Hier entsteht bald deine tägliche Zusammenfassung:\n"
        "- Anzahl starker Long-/Short-Signale\n"
        "- Qualität & Trefferquote\n"
        "- Persönlicher Performance-Bericht\n\n"
        "🛠️ _Modul ist in Entwicklung – du wirst benachrichtigt, sobald es aktiv ist._"
    )
    await update.message.reply_markdown(message)
