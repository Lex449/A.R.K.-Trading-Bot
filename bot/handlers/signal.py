from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.utils.analysis import analyse_market

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("📡 Signal wird analysiert...\nEinen Moment Geduld...")

    symbol = "US100/USDT"  # Du kannst das später dynamisch machen (z. B. aus User-Input)
    result = analyse_market(symbol=symbol)

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
            f"_Ermittelt durch A.R.K. – deinem KI-Trading-Mentor._"
        )
    else:
        message = (
            f"⚠️ Aktuell kein klares Signal für {symbol}.\n"
            f"A.R.K. beobachtet weiter den Markt und gibt Bescheid, sobald ein Einstieg erkennbar ist."
        )

    await update.message.reply_markdown(message)

signal_handler = CommandHandler("signal", signal)