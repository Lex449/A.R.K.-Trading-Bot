from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def recap(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = (
        "🧾 *Tageszusammenfassung (Beta)*\n"
        "-----------------------------------\n"
        "✅ Anzahl geprüfter Märkte: 4\n"
        "📡 Ausgelöste Signale: 3\n"
        "📈 Beste Performance: US100\n"
        "⚠️ Verlustvermeidung durch Analyse: 1 Fall\n"
        "\n_A.R.K. bleibt fokussiert – dein Wachstum ist das Ziel._"
    )
    await update.message.reply_markdown(message)

recap_handler = CommandHandler("recap", recap)