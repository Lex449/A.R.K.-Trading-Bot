"""
A.R.K. Bot Main Entry – Ultra Stable Infinity Build 2025
Made in Bali. Engineered with German Precision.
"""

import asyncio
import logging
import nest_asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

# === Core Handlers ===
from bot.handlers.commands import start, help_command, analyze_symbol_handler, set_language
from bot.handlers.global_error_handler import global_error_handler

# === Auto Systems ===
from bot.auto.heartbeat_manager import start_heartbeat_manager
from bot.auto.connection_watchdog import start_connection_watchdog
from bot.auto.auto_signal_loop import auto_signal_loop
from bot.auto.daily_scheduler import start_daily_scheduler

# === Utilities ===
from bot.handlers.set_my_commands import set_bot_commands
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings
from bot.utils.logger import setup_logger

# === Setup Logger immediately ===
setup_logger(__name__)

# === Allow nested event loops for Replit / Railway ===
nest_asyncio.apply()

# === Load Settings ===
config = get_settings()
TOKEN = config["BOT_TOKEN"]
CHAT_ID = int(config["TELEGRAM_CHAT_ID"])

async def startup_tasks(application):
    """
    Executes all essential startup tasks safely.
    """
    try:
        # Remove webhook before starting polling (mandatory for Railway)
        await application.bot.delete_webhook(drop_pending_updates=True)
        logging.info("✅ Webhook removed successfully.")

        # Set bot commands
        await set_bot_commands(application)
        logging.info("✅ Bot commands set successfully.")

        # Start Schedulers & Loops
        start_heartbeat_manager(application, CHAT_ID)
        start_connection_watchdog(application, CHAT_ID)
        start_daily_scheduler(application, CHAT_ID)

        # Start Auto Signal Loop
        asyncio.create_task(auto_signal_loop())

        logging.info("🚀 Startup tasks completed. A.R.K. ready for action.")

    except Exception as e:
        await report_error(application.bot, CHAT_ID, e, context_info="Startup Tasks Error")
        logging.error(f"❌ Error during startup tasks: {e}")

async def main():
    """
    Main runner for A.R.K. Trading Bot Infinity Version.
    """
    logging.info("🚀 A.R.K. Trading Bot – Infinity Stability Mode ACTIVATED.")

    # Build Application
    app = ApplicationBuilder().token(TOKEN).post_init(startup_tasks).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("analyse", analyze_symbol_handler))
    app.add_handler(CommandHandler("setlanguage", set_language))

    # Set Global Error Handler
    app.add_error_handler(global_error_handler)

    # Start polling for updates
    try:
        await app.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logging.critical(f"🔥 [Main] Fatal error during polling: {e}")
        await report_error(app.bot, CHAT_ID, e, context_info="Main Polling Error")

if __name__ == "__main__":
    asyncio.run(main())
