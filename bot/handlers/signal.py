from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from bot.config.settings import get_settings
from bot.utils.analysis import generate_signal

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    market = "NDX"
    settings = get_settings()
    signal_data = generate_signal(market, settings["twelvedata"]["api_key"])

    if signal_data:
        msg = (
            f"📈 *Signal für {market}*\n\n"
            f"Typ: {signal_data['signal']}\n"
            f"RSI: {signal_data['rsi']:.2f}\n"
            f"EMA: {signal_data['ema']:.2f}\n"
            f"Candlestick: {signal_data['pattern']}\n"
            f"⭐️ Bewertung: {signal_data['rating']} Sterne"
        )
    else:
        msg = "⚠️ Kein valides Signal erkannt – der Markt ist heute schweigsam."

    await update.message.reply_markdown(msg)

signal_handler = CommandHandler("signal", signal)