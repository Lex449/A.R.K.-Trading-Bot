from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.utils.analysis import analyse_market
from bot.utils.formatter import format_signal

async def analyse(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🔍 Analyse läuft...")

    symbol = "US100/USDT"
    result = analyse_market(symbol)

    if result:
        message = format_signal(symbol, result["trend"], result["confidence"], result["pattern"])
    else:
        message = (
            f"ℹ️ Analyse konnte nicht durchgeführt werden.\n"
            f"_Bitte später erneut versuchen._"
        )

    await update.message.reply_markdown(message)

analyse_handler = CommandHandler("analyse", analyse)