from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from bot.utils.analysis import generate_signal
from bot.config.settings import get_settings

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    market = "NDX"
    settings = get_settings()
    signal_data = generate_signal(market, settings["twelvedata"]["api_key"])

    if signal_data:
        msg = (
            f"📊 *Signal für {market}*\n\n"
            f"Typ: {signal_data['signal']}\n"
            f"RSI: {signal_data['rsi']:.2f}\n"
            f"EMA: {signal_data['ema']:.2f}\n"
            f"Candlestick: {signal_data['pattern']}\n"
            f"⭐️ Qualität: {signal_data['rating']} Sterne"
        )
    else:
        msg = f"⚠️ Kein valides Signal erkannt."

    await update.message.reply_markdown(msg)

signal_handler = CommandHandler("signal", signal)