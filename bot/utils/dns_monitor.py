# bot/utils/dns_monitor.py

import aiohttp
import asyncio
from datetime import datetime
from telegram import Bot
from bot.config.settings import get_settings

notified = False  # Flag, ob Notification schon gesendet wurde

async def check_dns_and_notify():
    """
    Überwacht die Erreichbarkeit der Domain & benachrichtigt bei erfolgreichem Ping.
    """
    global notified
    settings = get_settings()
    bot = Bot(token=settings["BOT_TOKEN"])
    domain = "https://arktradingbot.com"

    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(domain, timeout=10) as response:
                    if response.status == 200 and not notified:
                        time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
                        message = (
                            f"✅ *Domain aktiv!*\n"
                            f"`{domain}` ist jetzt **live & erreichbar** über HTTPS.\n\n"
                            f"_Zeitpunkt:_ {time}"
                        )
                        await bot.send_message(
                            chat_id=settings["TELEGRAM_CHAT_ID"],
                            text=message,
                            parse_mode="Markdown"
                        )
                        notified = True
        except Exception as e:
            print(f"[DNS Monitor] Fehler: {e}")

        await asyncio.sleep(900)  # Alle 15 Minuten prüfen
