from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.utils.analysis import analyse_market

async def analyse(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🔍 Marktanalyse wird durchgeführt...")

    symbol = "US100/USDT"
    result = analyse_market(symbol=symbol)

    if result:
        trend = result["trend"]
        confidence = result["confidence"]
        pattern = result["pattern"]
        stars = "⭐️" * confidence + "✩" * (5 - confidence)

        message = (
            f"📈 *Analyse für {symbol}*\n"
            f"Trend: *{trend}*\n"
            f"Muster: *{pattern}*\n"
            f"Bewertung: {stars}\n\n"
            f"_Diese Analyse dient zur Orientierung – kein Einstiegssignal._"
        )
    else:
        message = (
            f"ℹ️ Für {symbol} wurde aktuell kein relevantes Muster erkannt.\n"
            f"_A.R.K. beobachtet weiter._"
        )

    await update.message.reply_markdown(message)

analyse_handler = CommandHandler("analyse", analyse)