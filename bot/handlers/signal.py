# bot/handlers/signal.py

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.engine.analysis_engine import analyze_market
from bot.utils.formatter import format_signal
from bot.config.settings import get_settings

signal_handler = CommandHandler("signal", lambda update, context: signal(update, context))

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    settings = get_settings()
    symbols = settings["AUTO_SIGNAL_SYMBOLS"]
    results = []

    await update.message.reply_text("📡 Starte Live-Scan...")

    for symbol in symbols:
        result = analyze_market(symbol)
        if result:
            formatted = format_signal(symbol, result["trend"], result["confidence"], result["pattern"])
            results.append(formatted)
        else:
            results.append(f"⚠️ Kein Signal für {symbol} verfügbar.")

    message = "\n\n".join(results)
    await update.message.reply_markdown(message)
