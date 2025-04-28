"""
A.R.K. Bot Main Entry – NASA Wall Street Defense Edition.
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

# === Core Systems ===
from bot.auto.auto_signal_loop import auto_signal_loop
from bot.auto.watchdog_monitor import watchdog_monitor
from bot.auto.heartbeat_scheduler import start_heartbeat
from bot.auto.daily_scheduler import start_daily_analysis_scheduler
from bot.auto.connection_watchdog_scheduler import start_watchdog

# === Utilities ===
from bot.utils.error_reporter import report_error
from bot.utils.logger import setup_logger
from bot.config.settings import get_settings

# === Pre-Init: Logger Early Setup ===
setup_logger(__name__)

# === Allow Nested Event Loops for Railway, Replit etc. ===
nest_asyncio.apply()

# === Load Core Configuration ===
config = get_settings()
TOKEN = config["BOT_TOKEN"]
CHAT_ID = int(config["TELEGRAM_CHAT_ID"])

async def startup_tasks(application):
    """
    🚀 Launches all critical startup tasks safely and independently.
    """
    try:
        await application.bot.delete_webhook(drop_pending_updates=True)
        logging.info("✅ Webhook cleared successfully.")

        # === Launching Background Systems ===
        start_daily_analysis_scheduler(application, CHAT_ID)  # Daily summaries, resets
        start_heartbeat(application, CHAT_ID)  # Heartbeat monitoring
        start_watchdog(application, CHAT_ID)  # Connection watchdog

        # === Core Trading Loop ===
        asyncio.create_task(auto_signal_loop())

        # === Core Stability Monitor ===
        asyncio.create_task(watchdog_monitor(application))

        # === Configure User Commands ===
        await set_bot_commands(application)

        logging.info("✅ All startup tasks completed successfully.")

    except Exception as e:
        await report_error(application.bot, CHAT_ID, e, context_info="Startup Task Failure")
        logging.error(f"❌ Startup error: {e}")

async def main():
    """
    Core Runner for A.R.K. Trading Bot 2.2 NASA Wall Street Edition
    """
    logging.info("🚀 A.R.K. Trading Bot – NASA Wall Street Defense ACTIVATED.")

    application = ApplicationBuilder().token(TOKEN).post_init(startup_tasks).build()

    # === Register Commands ===
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("analyse", analyze_symbol_handler))
    application.add_handler(CommandHandler("setlanguage", set_language))
    application.add_handler(CommandHandler("signal", signal_handler))
    application.add_handler(CommandHandler("status", status_handler))
    application.add_handler(CommandHandler("shutdown", shutdown_handler))
    application.add_handler(CommandHandler("testsignal", test_signal))
    application.add_handler(CommandHandler("testanalyse", test_analyse))

    # === Attach Global Error Handling ===
    application.add_error_handler(global_error_handler)

    # === Go Live Polling ===
    await application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
