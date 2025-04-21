# bot/auto/auto_signal.py

import asyncio
from telegram import Bot
from bot.utils.analysis import analyse_market
from bot.utils.formatter import format_signal
from bot.config.settings import get_settings

async def auto_signal_loop():
    settings = get_settings()
    bot = Bot(token=settings["BOT_TOKEN"])
    chat_id = settings["DANIEL_TELEGRAM_ID"]  # Nur du bekommst die Auto-Signale

    indices = ["US100/USDT", "US30/USDT", "NAS100/USDT", "SPX500/USDT"]

    while True:
        for symbol in indices:
            try:
                result = analyse_market(symbol)

                if result:
                    trend = result["trend"]
                    confidence = result["confidence"]
                    pattern = result["pattern"]
                    message = format_signal(symbol, trend, confidence, pattern)

                    await bot.send_message(
                        chat_id=chat_id,
                        text=message,
                        parse_mode="Markdown"
                    )

            except Exception as e:
                print(f"⚠️ Fehler bei Analyse von {symbol}: {e}")

        await asyncio.sleep(300)  # 5 Minuten Pause zwischen den Loops
