from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.utils.analysis import analyse_market

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("📡 Analysiere US100...")

    result = analyse_market("US100/USDT")
    if result:
        msg = (
            f"📊 *Signal für US100/USDT*\n"
            f"Trend: *{result['trend']}*\n"
            f"Muster: *{result['pattern']}*\n"
            f"Qualität: {'⭐️' * result['confidence']}"
        )
    else:
        msg = "⚠️ Aktuell kein klares Signal."
    await update.message.reply_markdown(msg)

signal_handler = CommandHandler("signal", signal)