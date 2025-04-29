"""
A.R.K. Bot Main Entry – Ultra Stable Wall Street Version 2.5
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
    set_language,
    signal_handler,
    status_handler,
    shutdown_handler,
    health_check
)
from bot.handlers.global_error_handler import global_error_handler
from bot.handlers.set_my_commands import set_bot_commands  # Korrekt!

# === Auto Systems ===
from bot.auto.daily_scheduler import daily_scheduler
from bot.auto.heartbeat_manager import start_heartbeat_manager

# === Utilities ===
from bot.config.settings import get_settings
from bot.utils.logger import setup_logger
from bot.utils.error_reporter import report_error

# Setup Logger
setup_logger(__name__)

# Allow nested event loops
nest_asyncio.apply()

# Load Settings
config = get_settings()
TOKEN = config["BOT_TOKEN"]
CHAT_ID = int(config["TELEGRAM_CHAT_ID"])

async def startup_tasks(application):
    """
    Startup Task Launcher – Initializes background loops and schedulers.
    """
    try:
        await application.bot.delete_webhook(drop_pending_updates=True)
        logging.info("✅ Webhook cleared successfully.")

        # Start all Schedulers
        daily_scheduler(application, CHAT_ID)
        await start_heartbeat_manager(application, CHAT_ID)

        # Set Commands
        await set_bot_commands(application)  # ✅ corrected

        logging.info("✅ Startup tasks completed.")

    except Exception as e:
        await report_error(application.bot, CHAT_ID, e, context_info="Startup Task Error")
        logging.error(f"❌ Startup Error: {e}")

async def main():
    """
    Main function to launch the bot.
    """
    logging.info("🚀 A.R.K. Trading Bot – Full Ultra Stability Activated.")

    # Build the app
    app = ApplicationBuilder().token(TOKEN).post_init(startup_tasks).build()

    # Register Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("analyse", analyze_symbol_handler))
    app.add_handler(CommandHandler("setlanguage", set_language))
    app.add_handler(CommandHandler("signal", signal_handler))
    app.add_handler(CommandHandler("status", status_handler))
    app.add_handler(CommandHandler("health", health_check))
    app.add_handler(CommandHandler("shutdown", shutdown_handler))

    # Global Error Handler
    app.add_error_handler(global_error_handler)

    # Run polling
    try:
        await app.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logging.critical(f"🔥 Bot crashed: {e}")
        await report_error(app.bot, CHAT_ID, e, context_info="Main Polling Error")

if __name__ == "__main__":
    asyncio.run(main())
