import asyncio
from telegram import Bot
from bot.config.settings import get_settings
from bot.utils.analysis import analyse_market

async def run_auto_signals(app):
    settings = get_settings()
    bot = Bot(token=settings["BOT_TOKEN"])
    chat_id = settings["DANIEL_TELEGRAM_ID"]

    indices = ["US100/USDT", "SPX500/USDT", "NAS100/USDT", "DJI/USDT"]

    while True:
        for symbol in indices:
            result = analyse_market(symbol)

            if result:
                trend = result["trend"]
                confidence = result["confidence"]
                pattern = result["pattern"]
                stars = "⭐️" * confidence + "✩" * (5 - confidence)

                message = (
                    f"📡 *Automatisches Signal*\n"
                    f"Symbol: *{symbol}*\n"
                    f"Trend: *{trend}*\n"
                    f"Muster: *{pattern}*\n"
                    f"Qualität: {stars}"
                )

                await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")

        await asyncio.sleep(60)  # jede Minute neu analysieren