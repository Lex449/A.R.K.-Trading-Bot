"""
A.R.K. Bot Main Entry – Ultra Stable Wall Street Version 2.5
Made in Bali. Engineered with German Precision.
"""

import asyncio
import logging
import nest_asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

# === Core Handlers ===
from bot.handlers.commands import (
    start,
    help_command,
    analyze_symbol_handler,
    set_language,
    health_check,
    signal_handler,
    status_handler,
    shutdown_handler,
)
from bot.handlers.global_error_handler import global_error_handler
from bot.handlers.set_my_commands import set_bot_commands

# === Startup Systems ===
from bot.auto.heartbeat_manager import start_heartbeat_manager
from bot.auto.connection_watchdog import start_connection_watchdog
from bot.auto.auto_signal_loop import auto_signal_loop

# === Utilities ===
from bot.config.settings import get_settings
from bot.utils.logger import setup_logger
from bot.utils.error_reporter import report_error

# Setup Logger immediately
setup_logger(__name__)

# Allow nested event loops (important for Railway/Replit)
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
        chat_id = CHAT_ID

        # Remove webhook (critical for polling mode!)
        await application.bot.delete_webhook(drop_pending_updates=True)
        logging.info("✅ Webhook cleared successfully.")

        # Set command menu
        await set_my_commands(application)
        logging.info("✅ Bot commands set successfully.")

        # Start Heartbeat + Watchdog Systems
        start_heartbeat_manager(application, chat_id)
        start_connection_watchdog(application, chat_id)

        # Start Auto Signal Loop
        asyncio.create_task(auto_signal_loop())

        logging.info("🚀 Startup completed. Bot is fully operational.")

    except Exception as e:
        await report_error(application.bot, chat_id, e, context_info="Startup Task Error")
        logging.error(f"❌ Error during startup tasks: {e}")

async def main():
    """
    Main entry for running the A.R.K. Bot.
    """
    logging.info("🚀 A.R.K. Trading Bot 2.5 – Full Ultra Stability Activated.")

    app = ApplicationBuilder().token(TOKEN).post_init(startup_tasks).build()

    # Register Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("analyse", analyze_symbol_handler))
    app.add_handler(CommandHandler("setlanguage", set_language))
    app.add_handler(CommandHandler("health", health_check))
    app.add_handler(CommandHandler("signal", signal_handler))
    app.add_handler(CommandHandler("status", status_handler))
    app.add_handler(CommandHandler("shutdown", shutdown_handler))

    # Register Global Error Handler
    app.add_error_handler(global_error_handler)

    # Start Polling
    try:
        await app.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logging.critical(f"🔥 [Main] Bot failed with critical error: {e}")
        await report_error(app.bot, CHAT_ID, e, context_info="Main Polling Crash")

if __name__ == "__main__":
    asyncio.run(main())
