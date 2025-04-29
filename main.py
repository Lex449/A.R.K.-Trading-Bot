"""
A.R.K. Bot Main Entry – Ultra Stable Wall Street Version
Made in Bali. Engineered with German Precision.
"""

import asyncio
import logging
import nest_asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

# === Handlers ===
from bot.handlers.commands import (
    start,
    help_command,
    analyze_symbol_handler,
    signal_handler,
    status_handler,
    shutdown_handler,
    uptime_handler,
    set_language_handler
)

# === Startup Tasks ===
from bot.startup.startup_tasks import startup_tasks

# === Utilities ===
from bot.handlers.global_error_handler import global_error_handler
from bot.utils.logger import setup_logger
from bot.config.settings import get_settings

# === Logger Setup ===
setup_logger(__name__)

# === Allow nested event loops (for Railway etc.) ===
nest_asyncio.apply()

# === Settings Load ===
config = get_settings()
TOKEN = config["BOT_TOKEN"]
CHAT_ID = int(config["TELEGRAM_CHAT_ID"])

async def main():
    """
    Main Bot Runner – Launch A.R.K. fully.
    """
    logging.info("🚀 A.R.K. Trading Bot – Full Ultra Stability Mode activated.")

    app = ApplicationBuilder().token(TOKEN).post_init(startup_tasks).build()

    # Register Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("analyse", analyze_symbol_handler))
    app.add_handler(CommandHandler("signal", signal_handler))
    app.add_handler(CommandHandler("status", status_handler))
    app.add_handler(CommandHandler("uptime", uptime_handler))
    app.add_handler(CommandHandler("setlanguage", set_language_handler))
    app.add_handler(CommandHandler("shutdown", shutdown_handler))

    # Register Error Handler
    app.add_error_handler(global_error_handler)

    # Start Polling
    try:
        await app.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logging.critical(f"🔥 [Main] Critical error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
