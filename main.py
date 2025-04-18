# main.py

import asyncio
from telegram.ext import ApplicationBuilder
from bot.config.settings import get_settings
from bot.handlers.start import start
from bot.handlers.ping import ping
from bot.handlers.signal import signal
from bot.handlers.status import status
from bot.handlers.shutdown import shutdown
from bot.utils.error_handler import handle_error

async def main():
    settings = get_settings()

    application = ApplicationBuilder().token(settings["TOKEN"]).build()

    application.add_handler(start)
    application.add_handler(ping)
    application.add_handler(signal)
    application.add_handler(status)
    application.add_handler(shutdown)

    application.add_error_handler(handle_error)

    print("A.R.K. gestartet und bereit.")
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())