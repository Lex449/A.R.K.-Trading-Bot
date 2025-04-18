from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from bot.utils.analysis import generate_signal
from bot.config.settings import get_settings

async def analyse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    settings = get_settings()
    api_key = settings["twelvedata"]["api_key"]
    markets = settings["markets"]

    results = []
    for market in markets:
        signal_data = generate_signal(market, api_key)
        if signal_data:
            results.append(f"• {market}: {signal_data['signal']} ({signal_data['rating']}⭐️)")
        else:
            results.append(f"• {market}: Analysefehler")

    await update.message.reply_text("📈 *Marktanalyse:*\n\n" + "\n".join(results), parse_mode="Markdown")

analyse_handler = CommandHandler("analyse", analyse)