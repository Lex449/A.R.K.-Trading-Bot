# bot/handlers/signal.py

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.engine.analysis_engine import analyze_market
from bot.utils.formatter import format_signal

signal_handler = CommandHandler("signal", lambda update, context: signal(update, context))

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("📡 Starte Analyse der Märkte...")

    symbols = ["US100", "US30", "DE40", "JP225", "HK50", "SPX500"]
    results = []

    for symbol in symbols:
        try:
            result = analyze_market(symbol)
            if result:
                trend = result["trend"]
                confidence = result["confidence"]
                pattern = result["pattern"]
                message = format_signal(symbol, trend, confidence, pattern)
                results.append(message)
            else:
                results.append(f"⚠️ Keine Daten verfügbar für {symbol}.")
        except Exception as e:
            results.append(f"❌ Fehler bei Analyse von {symbol}: {e}")

    final_message = "\n\n".join(results)
    await update.message.reply_markdown(final_message)
