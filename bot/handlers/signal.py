from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.utils.analysis import analyse_market
from bot.utils.formatter import format_signal
from bot.config.settings import get_settings

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("📡 Analysiere Märkte...")

    symbols = ["US100/USDT", "US30/USDT", "US500/USDT"]
    results = []

    for symbol in symbols:
        result = analyse_market(symbol)

        if result:
            trend = result["trend"]
            confidence = result["confidence"]
            pattern = result["pattern"]
            formatted_signal = format_signal(symbol, trend, confidence, pattern)
            results.append(formatted_signal)
        else:
            results.append(f"⚠️ Keine Analyse-Daten für {symbol}")

    message = "\n\n".join(results)
    await update.message.reply_markdown(message)

signal_handler = CommandHandler("signal", signal)
