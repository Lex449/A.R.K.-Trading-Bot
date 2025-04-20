from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = update.effective_user.language_code

    if lang == "de":
        message = (
            "Willkommen bei A.R.K. – deinem persönlichen KI-Trading-Mentor.\n\n"
            "Ich helfe dir dabei, die Märkte zu verstehen, Fehler zu vermeiden und sicher zu wachsen.\n\n"
            "Du bist nicht allein:\n"
            "→ Tritt jetzt der A.R.K. Community bei für Support & Austausch:\n"
            "https://t.me/arktradingcommunity"
        )
    else:
        message = (
            "Welcome to A.R.K. – your personal AI trading mentor.\n\n"
            "I’m here to help you understand the markets, avoid costly mistakes, and grow with confidence.\n\n"
            "You’re not alone:\n"
            "→ Join the A.R.K. Community for support & exchange:\n"
            "https://t.me/arktradingcommunity"
        )

    await update.message.reply_text(message)