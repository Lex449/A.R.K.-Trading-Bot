# bot/handlers/signal.py

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.engine.analysis_engine import analyze_market
from bot.utils.formatter import format_signal
from bot.utils.language import get_language

signal_handler = CommandHandler("signal", lambda update, context: signal(update, context))

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_language(update)
    symbols = ["US100", "US30", "DE40", "JP225", "HK50", "SPX500"]
    results = []

    if lang == "de":
        await update.message.reply_text("📡 Analysiere Hauptmärkte...")
    else:
        await update.message.reply_text("📡 Scanning major markets...")

    for symbol in symbols:
        result = analyze_market(symbol)
        if result:
            formatted = format_signal(
                symbol=symbol,
                trend=result["trend"],
                confidence=result["confidence"],
                pattern=result["pattern"],
                lang=lang
            )
            results.append(formatted)
        else:
            error_msg = f"⚠️ Keine Daten für {symbol}" if lang == "de" else f"⚠️ No data for {symbol}"
            results.append(error_msg)

    await update.message.reply_markdown("\n\n".join(results))
