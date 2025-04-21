# bot/handlers/signal.py

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.utils.analysis import analyse_market

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("📡 Analysiere US100...")

    result = analyse_market("US100/USDT")

    if result:
        trend = result["trend"]
        confidence = result["confidence"]
        pattern = result["pattern"]

        stars = "⭐️" * confidence + "✩" * (5 - confidence)

        message = (
            f"📊 *Signal für US100/USDT*\n"
            f"Trend: *{trend}*\n"
            f"Muster: *{pattern}*\n"
            f"Qualität: {stars}\n\n"
            f"_Manuelle Abfrage – Entscheidung liegt bei dir._"
        )
    else:
        message = "⚠️ Aktuell kein klares Signal für US100."

    await update.message.reply_markdown(message)

signal_handler = CommandHandler("signal", signal)