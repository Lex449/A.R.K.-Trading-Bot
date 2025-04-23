from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.utils.analysis import analyse_market
from bot.utils.formatter import format_signal

async def analyse(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🔍 Analyse läuft...")

    symbols = ["US100/USDT", "US30/USDT", "US500/USDT"]
    results = []

    for symbol in symbols:
        result = analyse_market(symbol)

        if result:
            message = format_signal(symbol, result["trend"], result["confidence"], result["pattern"])
        else:
            message = (
                f"ℹ️ Analyse konnte nicht durchgeführt werden.\n"
                f"_Bitte später erneut versuchen._"
            )
        results.append(message)

    await update.message.reply_markdown("\n\n".join(results))

analyse_handler = CommandHandler("analyse", analyse)
