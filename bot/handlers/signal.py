from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.utils.analysis import analyse_market

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("📡 Markt wird analysiert...\nEinen Moment...")

    symbol = "US100/USDT"
    result = analyse_market(symbol)

    if result:
        trend = result["trend"]
        confidence = result["confidence"]
        pattern = result["pattern"]
        stars = "⭐️" * confidence + "✩" * (5 - confidence)

        message = (
            f"📊 *Live-Signal für {symbol}*\n"
            f"Trend: *{trend}*\n"
            f"Muster: *{pattern}*\n"
            f"Signalqualität: {stars}\n\n"
            f"_Analyse durchgeführt von A.R.K._"
        )
    else:
        message = (
            f"⚠️ Kein Signal erkannt für {symbol}.\n"
            f"_A.R.K. bleibt wachsam._"
        )

    await update.message.reply_markdown(message)

signal_handler = CommandHandler("signal", signal)