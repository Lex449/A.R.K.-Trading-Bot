from telegram import Update
from telegram.ext import ContextTypes

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Signal-Scanner aktiviert.\n"
        "Ich prüfe gerade RSI, EMA und Candle-Muster.\n"
        "Du bekommst Bescheid, sobald ein Einstieg möglich ist."
    )