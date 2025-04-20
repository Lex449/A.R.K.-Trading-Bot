from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def recap(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = (
        "🧾 *Tägliches Recap (Beta)*\n"
        "-----------------------------\n"
        "✅ Überwachte Märkte: US100, US30, NAS100, SPX500\n"
        "⭐️ Signale heute: 3 erkannt\n"
        "📈 Beste Bewertung: US100 (Long-Signal)\n"
        "📉 Warnsignal: NAS100 (Short-Muster erkannt)\n"
        "\n_A.R.K. analysiert, du entscheidest._"
    )
    await update.message.reply_markdown(message)

recap_handler = CommandHandler("recap", recap)