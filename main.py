import asyncio
from telegram.ext import ApplicationBuilder
from bot.config.settings import get_settings
from bot.handlers.start import start
from bot.handlers.ping import ping
from bot.handlers.signal import signal
from bot.handlers.status import status
from bot.handlers.shutdown import shutdown

async def main():
    settings = get_settings()

    application = ApplicationBuilder().token(settings["TOKEN"]).build()

    application.add_handler(start)
    application.add_handler(ping)
    application.add_handler(signal)
    application.add_handler(status)
    application.add_handler(shutdown)

    print("A.R.K. ist bereit.")
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())