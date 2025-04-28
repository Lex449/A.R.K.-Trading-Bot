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
from bot.handlers.commands import start, help_command, analyze_symbol_handler, set_language
from bot.handlers.signal import signal_handler
from bot.handlers.status import status_handler
from bot.handlers.shutdown import shutdown_handler
from bot.handlers.test_signal import test_signal
from bot.handlers.test_analyse import test_analyse
from bot.handlers.global_error_handler import global_error_handler
from bot.handlers.set_my_commands import set_bot_commands

# === Scheduler & Auto Systems ===
from bot.auto.daily_scheduler import start_daily_analysis_scheduler
from bot.auto.heartbeat_scheduler import start_heartbeat
from bot.auto.watchdog_scheduler import start_watchdog

# === Utilities ===
from bot.utils.error_reporter import report_error
from bot.utils.logger import setup_logger
from bot.config.settings import get_settings

# Setup logger immediately
setup_logger(__name__)

# Allow nested event loops (important for Railway / Replit)
nest_asyncio.apply()

# Load settings
config = get_settings()
TOKEN = config["BOT_TOKEN"]
CHAT_ID = int(config["TELEGRAM_CHAT_ID"])

async def startup_tasks(application):
    """
    Startup Task Launcher – Initializes background loops and schedulers.
    """
    try:
        # Clear any existing webhooks
        await application.bot.delete_webhook(drop_pending_updates=True)
        logging.info("✅ Webhook cleared successfully.")

        # Schedule tasks
        start_daily_analysis_scheduler(application, CHAT_ID)
        start_heartbeat(application, CHAT_ID)
        start_watchdog(application, CHAT_ID)  # Watchdog needs to be started for continuous monitoring

        # Set bot commands
        await set_bot_commands(application)

        logging.info("✅ All startup tasks completed.")

    except Exception as e:
        await report_error(application.bot, CHAT_ID, e, context_info="Startup Task Error")
        logging.error(f"❌ Error during startup tasks: {e}")

async def main():
    """
    Main entry for running the A.R.K. Bot.
    """
    logging.info("🚀 A.R.K. Trading Bot 2.5 – Full Ultra Stability Activated.")

    # Initialize bot application
    app = ApplicationBuilder().token(TOKEN).post_init(startup_tasks).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("analyse", analyze_symbol_handler))
    app.add_handler(CommandHandler("setlanguage", set_language))
    app.add_handler(CommandHandler("signal", signal_handler))
    app.add_handler(CommandHandler("status", status_handler))
    app.add_handler(CommandHandler("shutdown", shutdown_handler))
    app.add_handler(CommandHandler("testsignal", test_signal))
    app.add_handler(CommandHandler("testanalyse", test_analyse))

    # Set global error handler
    app.add_error_handler(global_error_handler)

    # Start polling
    try:
        await app.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logging.critical(f"❌ [Main] Bot failed with error: {e}")
        await report_error(app.bot, CHAT_ID, e, context_info="Main Polling Error")

if __name__ == "__main__":
    asyncio.run(main())
