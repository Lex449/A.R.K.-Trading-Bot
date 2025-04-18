from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from bot.config.settings import get_settings
from bot.utils.analysis import generate_signal

async def analyse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    settings = get_settings()
    api_key = settings["twelvedata"]["api_key"]
    markets = settings["markets"]

    responses = []
    for market in markets:
        result = generate_signal(market, api_key)
        if result:
            line = f"• {market}: {result['signal']} ({result['rating']}⭐️)"
        else:
            line = f"• {market}: Analysefehler"
        responses.append(line)

    await update.message.reply_text("🧠 *Marktüberblick:*\n" + "\n".join(responses), parse_mode="Markdown")

analyse_handler = CommandHandler("analyse", analyse)