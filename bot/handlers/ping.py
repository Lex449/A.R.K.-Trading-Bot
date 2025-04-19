from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.utils.language import get_language

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = get_language(update)

    messages = {
        "de": "✅ *Bot ist online!* Bereit für Action.",
        "en": "✅ *Bot is online!* Ready for action."
    }

    await update.message.reply_text(messages[lang], parse_mode="Markdown")

ping_handler = CommandHandler("ping", ping)