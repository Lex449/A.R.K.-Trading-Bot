import asyncio
from telegram import Bot
from bot.utils.analysis import analyze_symbol
from bot.config.settings import get_settings

async def auto_signal_loop():
    """Automatisierter Signal-Loop, der alle 5 Minuten läuft und Signale sendet."""
    settings = get_settings()
    bot = Bot(token=settings["BOT_TOKEN"])  # Bot mit dem Token aus der .env

    result = analyze_symbol("US100")
    if result and result["signal"]:
        message = f"📉 *A.R.K. Signal* für {result['symbol']}: *{result['signal']}*\n"
        message += f"Trend:" {result['trend']} | RSI: {result['rsi']:.2f}"
        await bot.send_message(
            chat_id=settings["TELEGRAM_CHAT_ID"],
            text=message,
            parse_mode='Markdown'
        )
