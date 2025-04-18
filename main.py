import asyncio
import os
from aiogram import Bot, Dispatcher
from bot.config.settings import get_settings
from bot.utils.error_handler import notify_and_exit

from bot.handlers.start import start_handler
from bot.handlers.ping import ping_handler
from bot.handlers.status import status_handler
from bot.handlers.shutdown import shutdown_handler
from bot.handlers.signal import signal_handler
from bot.handlers.analyse import analyse_handler

# SETTINGS LADEN & FEHLER PRÜFEN
try:
    settings = get_settings()
except EnvironmentError as e:
    missing_var = str(e)
    asyncio.run(notify_and_exit(
        bot_token=os.getenv("BOT_TOKEN"),
        telegram_id=os.getenv("DANIEL_TELEGRAM_ID"),
        missing_var=missing_var
    ))

# BOT INITIALISIEREN
bot = Bot(token=settings["BOT_TOKEN"])
dp = Dispatcher()

# HANDLER REGISTRIEREN
dp.message.register(start_handler, commands=["start"])
dp.message.register(ping_handler, commands=["ping"])
dp.message.register(status_handler, commands=["status"])
dp.message.register(shutdown_handler, commands=["shutdown"])
dp.message.register(signal_handler, commands=["signal"])
dp.message.register(analyse_handler, commands=["analyse"])

# BOT STARTEN
async def main():
    print("✅ A.R.K. läuft!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())