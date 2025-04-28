"""
A.R.K. Trading Bot – Ultra Stability Core
Born in Bali. Engineered with German Precision.
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
from bot.handlers.error_handler import global_error_handler
from bot.handlers.set_my_commands import set_bot_commands

# === Core Systems ===
from bot.auto.auto_signal_loop import auto_signal_loop
from bot.auto.heartbeat_scheduler import start_heartbeat
from bot.auto.watchdog_scheduler import start_watchdog
from bot.auto.daily_scheduler import start_daily_analysis_scheduler

# === Utilities ===
from bot.utils.logger import setup_logger
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings

# === Setup early Logger and Asyncio Patch ===
setup_logger(__name__)
nest_asyncio.apply()

# === Load Settings ===
config = get_settings()
TOKEN = config["BOT_TOKEN"]
CHAT_ID = int(config["TELEGRAM_CHAT_ID"])

async def startup_tasks(application):
    """
    Executes once after bot startup: Schedulers, Loops, Watchdog, Commands
    """
    try:
        await application.bot.delete_webhook(drop_pending_updates=True)
        logging.info("✅ Webhook deleted.")

        # Start Core Services
        start_heartbeat(application, CHAT_ID)
        start_watchdog(application, CHAT_ID)
        start_daily_analysis_scheduler(application, CHAT_ID)
        asyncio.create_task(auto_signal_loop())
        await set_bot_commands(application)

        logging.info("✅ Startup Tasks completed. A.R.K. Operational.")

    except Exception as e:
        await report_error(application.bot, CHAT_ID, e, context_info="Startup Tasks Error")
        logging.critical(f"❌ Startup Tasks Critical Error: {e}")

async def main():
    """
    A.R.K. – Main Launch Sequence
    """
    logging.info("🚀 A.R.K. Ultra System Booting...")

    # Create Bot Application
    application = ApplicationBuilder().token(TOKEN).post_init(startup_tasks).build()

    # === Register Core Handlers ===
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("analyse", analyze_symbol_handler))
    application.add_handler(CommandHandler("setlanguage", set_language))
    application.add_handler(CommandHandler("signal", signal_handler))
    application.add_handler(CommandHandler("status", status_handler))
    application.add_handler(CommandHandler("shutdown", shutdown_handler))
    application.add_handler(CommandHandler("testsignal", test_signal))
    application.add_handler(CommandHandler("testanalyse", test_analyse))

    # === Global Fallback Error Handler ===
    application.add_error_handler(global_error_handler)

    # === Start Polling for Updates ===
    await application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
