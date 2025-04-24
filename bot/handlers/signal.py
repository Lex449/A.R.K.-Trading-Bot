# /bot/handlers/signal.py

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.engine.analysis import analyze_symbol
from bot.utils.formatter import format_signal
from bot.config.settings import get_settings

signal_handler = CommandHandler("signal", lambda update, context: signal(update, context))

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sendet ein kompaktes Markt-Signal für alle aktiven Assets."""
    await update.message.reply_text("📡 A.R.K. scannt aktuelle Marktlage...")

    settings = get_settings()
    symbols = settings["AUTO_SIGNAL_SYMBOLS"]
    messages = []

    for symbol in symbols:
        try:
            result = analyze_symbol(symbol)
            if result:
                msg = format_signal(
                    symbol=symbol,
                    trend=result.get("trend", "Neutral"),
                    confidence=result.get("confidence", 0),
                    pattern=result.get("pattern", "Kein Muster")
                )
            else:
                msg = f"⚠️ Keine Analyse möglich für {symbol}."
        except Exception as e:
            msg = f"❌ Fehler bei Analyse von {symbol}: {e}"
        
        messages.append(msg)

    await update.message.reply_markdown("\n\n".join(messages))
