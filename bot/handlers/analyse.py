from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.utils.analysis import analyse_market

async def analyse(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🔍 Analyse läuft...")

    symbol = "US100/USDT"
    result = analyse_market(symbol)

    if result:
        trend = result["trend"]
        confidence = result["confidence"]
        pattern = result["pattern"]
        stars = "⭐️" * confidence + "✩" * (5 - confidence)

        message = (
            f"📈 *Analyse für {symbol}*\n"
            f"Trend: *{trend}*\n"
            f"Daten: *{pattern}*\n"
            f"Bewertung: {stars}\n\n"
            f"_Diese Analyse ist informativ – kein Einstiegssignal._"
        )
    else:
        message = (
            f"ℹ️ Analyse konnte nicht durchgeführt werden.\n"
            f"_Bitte später erneut versuchen._"
        )

    await update.message.reply_markdown(message)

analyse_handler = CommandHandler("analyse", analyse)