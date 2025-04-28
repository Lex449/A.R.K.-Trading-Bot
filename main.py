"""
A.R.K. Bot Main Entry – Hyper Stable Wall Street Version 2.0
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

# === Auto Modules ===
from bot.auto.auto_signal_loop import auto_signal_loop
from bot.auto.daily_scheduler import start_daily_analysis_scheduler
from bot.auto.heartbeat_scheduler import start_heartbeat

# === Utilities ===
from bot.utils.error_reporter import report_error
from bot.utils.logger import setup_logger
from bot.config.settings import get_settings

# === Setup Structured Logging ===
setup_logger(__name__)

# === Allow nested event loops (Railway / Replit Support) ===
nest_asyncio.apply()

# === Load Configuration ===
config = get_settings()
TOKEN = config["BOT_TOKEN"]

async def startup_tasks(application):
    """
    Launches background services on startup.
    """
    try:
        # Clean old webhook
        await application.bot.delete_webhook(drop_pending_updates=True)

        # Start Auto Signal Monitoring
        asyncio.create_task(auto_signal_loop())

        # Start Daily Analysis Scheduler
        start_daily_analysis_scheduler(application)

        # Start Heartbeat Scheduler
        start_heartbeat(application)

        # Set available bot commands
        await set_bot_commands(application)

        logging.info("✅ [Startup] All startup tasks completed successfully.")

    except Exception as e:
        await report_error(application.bot, int(config["TELEGRAM_CHAT_ID"]), e, context_info="Startup Task Error")

async def main():
    logging.info("🚀 A.R.K. Trading Bot 2.0 – Hyper Stable Wall Street Mode activated.")

    # Initialize Application
    app = ApplicationBuilder().token(TOKEN).post_init(startup_tasks).build()

    # === Register Command Handlers ===
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("analyse", analyze_symbol_handler))
    app.add_handler(CommandHandler("setlanguage", set_language))
    app.add_handler(CommandHandler("signal", signal_handler))
    app.add_handler(CommandHandler("status", status_handler))
    app.add_handler(CommandHandler("shutdown", shutdown_handler))
    app.add_handler(CommandHandler("testsignal", test_signal))
    app.add_handler(CommandHandler("testanalyse", test_analyse))

    # === Global Error Handler ===
    app.add_error_handler(global_error_handler)

    # === Start Polling ===
    await app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    asyncio.run(main())
