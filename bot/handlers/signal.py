from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.utils.analysis import analyse_market
from bot.utils.formatter import format_signal

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("📡 Analysiere US100...")

    result = analyse_market("US100/USDT")
    if result:
        message = format_signal("US100/USDT", result["trend"], result["confidence"], result["pattern"])
    else:
        message = "⚠️ Aktuell kein klares Signal."

    await update.message.reply_markdown(message)

signal_handler = CommandHandler("signal", signal)