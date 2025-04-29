# main.py

"""
A.R.K. Bot Main Entry – Ultra Stable Wall Street Version 3.0
Made in Bali. Engineered with German Precision.
"""

import asyncio
import logging
import nest_asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler
from bot.startup.startup_tasks import startup_tasks
from bot.handlers.commands import (
    start,
    help_command,
    analyze_symbol_handler,
    signal_handler,
    status_handler,
    shutdown_handler,
    test_signal,
    test_analyse,
    set_language,
    uptime_handler
)
from bot.handlers.global_error_handler import global_error_handler
from bot.config.settings import get_settings
from bot.utils.logger import setup_logger

# Logger Init
setup_logger(__name__)
nest_asyncio.apply()

# Config Load
config = get_settings()
TOKEN = config["BOT_TOKEN"]
CHAT_ID = int(config["TELEGRAM_CHAT_ID"])

async def main():
    """
    Main async entry point for the A.R.K. Bot.
    """
    logging.info("🚀 A.R.K. Trading Bot 3.0 – Full Launch Sequence Started.")

    app = ApplicationBuilder().token(TOKEN).post_init(startup_tasks).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("analyse", analyze_symbol_handler))
    app.add_handler(CommandHandler("signal", signal_handler))
    app.add_handler(CommandHandler("status", status_handler))
    app.add_handler(CommandHandler("shutdown", shutdown_handler))
    app.add_handler(CommandHandler("testsignal", test_signal))
    app.add_handler(CommandHandler("testanalyse", test_analyse))
    app.add_handler(CommandHandler("setlanguage", set_language))
    app.add_handler(CommandHandler("uptime", uptime_handler))

    # Global error catcher
    app.add_error_handler(global_error_handler)

    try:
        await app.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logging.critical(f"❌ [Main] Critical startup error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
