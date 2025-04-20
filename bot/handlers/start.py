from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    name = update.effective_user.first_name
    lang = update.effective_user.language_code or "en"
    if lang.startswith("de"):
        msg = f"Willkommen bei A.R.K., {name}!\n\nIch bin dein KI-Trading-Mentor.\n→ Tritt bei: https://t.me/arktradingcommunity"
    else:
        msg = f"Welcome to A.R.K., {name}!\n\nI'm your AI trading mentor.\n→ Join: https://t.me/arktradingcommunity"
    await update.message.reply_text(msg)

start_handler = CommandHandler("start", start)