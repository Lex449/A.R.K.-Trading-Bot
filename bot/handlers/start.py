from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_first_name = update.effective_user.first_name
    language_code = update.effective_user.language_code or 'en'

    if language_code.startswith('de'):
        welcome_message = (
            f"Willkommen bei A.R.K., {user_first_name}!\n\n"
            "Ich bin dein persönlicher KI-Trading-Mentor.\n"
            "Gemeinsam analysieren wir die Märkte, vermeiden Fehler und wachsen nachhaltig.\n\n"
            "→ Tritt der Community bei: https://t.me/arktradingcommunity"
        )
    else:
        welcome_message = (
            f"Welcome to A.R.K., {user_first_name}!\n\n"
            "I'm your personal AI trading mentor.\n"
            "Together, we’ll analyze markets, avoid mistakes, and grow with confidence.\n\n"
            "→ Join the community: https://t.me/arktradingcommunity"
        )

    await update.message.reply_text(welcome_message)

start_handler = CommandHandler("start", start)