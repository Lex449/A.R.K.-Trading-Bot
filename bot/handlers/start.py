from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.utils.language import get_language

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = get_language(update)

    messages = {
        "de": "Willkommen bei *A.R.K.* – deinem persönlichen Trading-Mentor.\n\nSende /signal, um aktuelle Marktsignale zu erhalten.",
        "en": "Welcome to *A.R.K.* – your personal trading mentor.\n\nSend /signal to receive current market signals."
    }

    await update.message.reply_text(messages[lang], parse_mode="Markdown")

start_handler = CommandHandler("start", start)