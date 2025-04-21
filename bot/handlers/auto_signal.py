import asyncio
from telegram import Bot
from datetime import datetime
from bot.config.settings import get_settings
from bot.utils.analysis import analyse_market

async def auto_signal_loop():
    settings = get_settings()
    bot = Bot(token=settings["BOT_TOKEN"])
    target_chat_id = settings["DANIEL_TELEGRAM_ID"]

    while True:
        symbol = "US100/USDT"
        result = analyse_market(symbol)

        if result:
            trend = result["trend"]
            confidence = result["confidence"]
            pattern = result["pattern"]
            stars = "⭐️" * confidence + "✩" * (5 - confidence)

            message = (
                f"📡 *Auto-Signal – {symbol}*\n"
                f"Trend: *{trend}*\n"
                f"Muster: *{pattern}*\n"
                f"Signalqualität: {stars}\n"
                f"_({datetime.now().strftime('%H:%M:%S')})_"
            )

            await bot.send_message(chat_id=target_chat_id, text=message, parse_mode="Markdown")

        await asyncio.sleep(60)