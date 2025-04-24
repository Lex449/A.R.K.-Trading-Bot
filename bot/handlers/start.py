# bot/handlers/start.py

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.utils.language import get_language

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name
    lang = get_language(update)

    if lang == "de":
        msg = (
            f"Willkommen bei *A.R.K.*, {name}!\n\n"
            f"Ich bin dein persönlicher KI-Trading-Mentor. Bereit für deine ersten Signale?\n"
            f"→ Tritt der Community bei: https://t.me/arktradingcommunity"
        )
    else:
        msg = (
            f"Welcome to *A.R.K.*, {name}!\n\n"
            f"I'm your personal AI trading mentor. Ready for your first signals?\n"
            f"→ Join the community: https://t.me/arktradingcommunity"
        )

    await update.message.reply_markdown(msg)

start_handler = CommandHandler("start", start)
