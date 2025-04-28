# main.py

"""
A.R.K. Bot Main Entry – Ultra Stable Wall Street Version 2.1
Made in Bali. Engineered with German Precision.
"""

import asyncio
import logging
import nest_asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

# === Command Handlers ===
from bot.handlers.commands import start, help_command, analyze_symbol_handler, set_language
from bot.handlers.signal import signal_handler
from bot.handlers.status import status_handler
from bot.handlers.shutdown import shutdown_handler
from bot.handlers.test_signal import test_signal
from bot.handlers.test_analyse import test_analyse
from bot.handlers.global_error_handler import global_error_handler
from bot.handlers.set_my_commands import set_bot_commands

# === KI Engine Systems ===
from bot.engine.confidence_tuning import tune_confidence
from bot.utils.session_tracker import get_session_stats  # Angepasst: Importiert get_session_stats()

# === Auto Signal Loop ===
from bot.auto.auto_signal_loop import auto_signal_loop

# === Scheduler Systems ===
from bot.auto.daily_scheduler import start_daily_analysis_scheduler
from bot.auto.heartbeat_scheduler import start_heartbeat

# === Utilities ===
from bot.utils.error_reporter import report_error
from bot.utils.logger import setup_logger
from bot.config.settings import get_settings

# === Initialize Logger Early ===
setup_logger(__name__)

# === Allow Nested Event Loops (Railway / Replit) ===
nest_asyncio.apply()

# === Load Configuration ===
config = get_settings()
TOKEN = config["BOT_TOKEN"]
CHAT_ID = int(config["TELEGRAM_CHAT_ID"])

async def startup_tasks(application):
    """
    Launches essential background services at startup.
    """
    try:
        # Remove existing webhooks to avoid conflicts
        await application.bot.delete_webhook(drop_pending_updates=True)
        logging.info("✅ Webhook removed successfully.")

        # Start Background Schedulers
        start_daily_analysis_scheduler(application, CHAT_ID)
        start_heartbeat(application, CHAT_ID)

        # Start Auto Signal Detection Loop
        asyncio.create_task(auto_signal_loop())

        # Configure /commands for user interface
        await set_bot_commands(application)

        logging.info("✅ All startup tasks completed successfully.")

    except Exception as e:
        await report_error(application.bot, CHAT_ID, e, context_info="Startup Tasks")
        logging.error(f"❌ Error during startup tasks: {e}")

async def main():
    """
    Core Runner for A.R.K. Trading Bot 2.1
    """
    logging.info("🚀 A.R.K. Trading Bot 2.1 – Wall Street Stability Mode ACTIVATED.")

    # Initialize Bot Application
    application = ApplicationBuilder().token(TOKEN).post_init(startup_tasks).build()

    # === Register Command Handlers ===
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("analyse", analyze_symbol_handler))
    application.add_handler(CommandHandler("setlanguage", set_language))
    application.add_handler(CommandHandler("signal", signal_handler))  # Signal Handling integriert
    application.add_handler(CommandHandler("status", status_handler))
    application.add_handler(CommandHandler("shutdown", shutdown_handler))
    application.add_handler(CommandHandler("testsignal", test_signal))
    application.add_handler(CommandHandler("testanalyse", test_analyse))

    # === Attach Global Error Handler ===
    application.add_error_handler(global_error_handler)

    # === Run Polling (Bot Online) ===
    await application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    asyncio.run(main())
