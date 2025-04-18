from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name or "Trader"
    lang = update.effective_user.language_code or "en"

    if lang.startswith("de"):
        text = (
            f"Hey {user}, willkommen bei **A.R.K.** – deinem Trading-Mentor!\n\n"
            "Ich helfe dir, Märkte zu verstehen, Chancen zu erkennen und Fehler zu vermeiden.\n"
            "Gib /signal ein, wenn du bereit bist – ich analysiere live mit dir."
        )
    else:
        text = (
            f"Hey {user}, welcome to **A.R.K.** – your personal trading mentor!\n\n"
            "I’ll help you understand the markets, spot opportunities and avoid rookie mistakes.\n"
            "Type /signal to begin – let’s dive in together."
        )

    await update.message.reply_markdown(text)

start_handler = CommandHandler("start", start)