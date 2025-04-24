# bot/handlers/signal.py

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.engine.analysis_engine import analyze_market
from bot.utils.formatter import format_signal
from bot.config.settings import get_settings

settings = get_settings()
signal_handler = CommandHandler("signal", lambda update, context: signal(update, context))

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("📡 Scanning markets...")

    results = []

    for symbol in settings["AUTO_SIGNAL_SYMBOLS"]:
        try:
            result = analyze_market(symbol)
            if result:
                message = format_signal(
                    symbol=symbol,
                    trend=result["trend"],
                    confidence=result["confidence"],
                    pattern=result["pattern"],
                    rsi=result["rsi"]
                )
                results.append(message)
            else:
                results.append(f"⚠️ No valid signal for `{symbol}`.")
        except Exception as e:
            results.append(f"❌ Error while analyzing `{symbol}`: `{e}`")

    response = "\n\n".join(results)
    await update.message.reply_markdown(response)
