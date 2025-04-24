# bot/handlers/start.py

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

start_handler = CommandHandler("start", lambda update, context: start(update, context))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name or "Trader"
    lang = update.effective_user.language_code or "en"

    if lang.startswith("de"):
        text = (
            f"Willkommen, {name}!\n\n"
            "Ich bin *A.R.K.* – dein KI-Trading-Mentor auf Telegram.\n"
            "Ich analysiere die Märkte live & sende dir hochwertige Einstiegssignale.\n"
            "📈 Fokus: *US100, DE40, US30, JP225, HK50*\n"
            "🧠 Engine: *RSI + EMA + Candle-Muster*\n\n"
            "_Tipp: Bleib ruhig. Handle präzise._"
        )
    else:
        text = (
            f"Welcome, {name}!\n\n"
            "I'm *A.R.K.* – your AI trading mentor on Telegram.\n"
            "I scan live markets & deliver quality entry signals.\n"
            "📈 Focus: *US100, DE40, US30, JP225, HK50*\n"
            "🧠 Engine: *RSI + EMA + Candle patterns*\n\n"
            "_Pro mindset. Precision matters._"
        )

    await update.message.reply_markdown(text)
