import logging
import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler
from bot.handlers.start import start
from bot.handlers.ping import ping
from bot.handlers.status import status
from bot.handlers.signal import signal
from bot.handlers.shutdown import shutdown
from bot.handlers.analyse import analyse
from bot.utils.error_handler import error_handler
from bot.config.settings import get_settings

logger = logging.getLogger(__name__)

async def main():
    settings = get_settings()
    application = ApplicationBuilder().token(settings.TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ping", ping))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("signal", signal))
    application.add_handler(CommandHandler("shutdown", shutdown))
    application.add_handler(CommandHandler("analyse", analyse))

    application.add_error_handler(error_handler)

    logger.info("Bot started successfully.")
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())