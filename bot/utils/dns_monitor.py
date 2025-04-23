# bot/utils/dns_monitor.py

import aiohttp
import asyncio
from datetime import datetime
from telegram import Bot
from bot.config.settings import get_settings

notified = False  # Flag für Benachrichtigung, ob Domain erreichbar

async def check_dns_and_notify():
    """Überwacht die DNS-Verbindung und sendet Benachrichtigung, wenn die Domain erreichbar ist."""
    global notified
    settings = get_settings()
    bot = Bot(token=settings["BOT_TOKEN"])
    url = "https://arktradingbot.com"

    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200 and not notified:
                        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
                        message = (
                            f"✅ *A.R.K. meldet sich:*\n"
                            f"Deine Domain `arktradingbot.com` ist jetzt **live & über HTTPS** erreichbar.\n"
                            f"Alles läuft stabil.\n\n"
                            f"_Zeit:_ {timestamp}"
                        )
                        await bot.send_message(
                            chat_id=settings["DANIEL_TELEGRAM_ID"],
                            text=message,
                            parse_mode="Markdown"
                        )
                        notified = True
        except Exception as e:
            print(f"[DNS CHECK ERROR] {e}")

        await asyncio.sleep(900)  # 15 Minuten warten, bevor erneut geprüft wird
