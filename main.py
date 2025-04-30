"""
A.R.K. – Ultra Resilient Main Entry Point.
Initialisiert den Telegram Bot, registriert alle Commands, startet alle Loops.
Made in Bali. Engineered with German Precision.
"""

import asyncio
import nest_asyncio
from telegram.ext import ApplicationBuilder, CommandHandler
from telegram import Bot
from bot.handlers.commands import (
    start,
    help_command,
    analyze_symbol_handler,
    signal_handler,
    status_handler,
    uptime_handler,
    set_language_handler,
    shutdown_handler,
    monitor_handler
)
from bot.handlers.global_error_handler import global_error_handler
from bot.config.settings import get_settings
from bot.utils.logger import setup_logger
from bot.startup.startup_task import execute_startup_tasks
from bot.auto.auto_signal_loop import auto_signal_loop  # <<< Wichtig

# === Logger & Settings ===
logger = setup_logger(__name__)
config = get_settings()

# === Async Patch für Railway etc. ===
nest_asyncio.apply()

# === Ultra Resilient Webhook Cleanup ===
async def force_webhook_cleanup():
    try:
        logger.info("⚙️ [Init] Attempting to remove existing webhook...")
        bot = Bot(config["BOT_TOKEN"])
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("✅ [Init] Webhook successfully removed.")
    except Exception as e:
        logger.warning(f"⚠️ [Init] Webhook cleanup failed: {e}")

# === Main Routine ===
async def main():
    logger.info("🚀 [Main] Launch sequence initiated...")

    try:
        # 1. Zuerst: Webhook sicher entfernen
        await force_webhook_cleanup()

        # 2. Application starten
        application = ApplicationBuilder().token(config["BOT_TOKEN"]).build()

        # 3. Command Handler registrieren
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("analyse", analyze_symbol_handler))
        application.add_handler(CommandHandler("signal", signal_handler))
        application.add_handler(CommandHandler("status", status_handler))
        application.add_handler(CommandHandler("uptime", uptime_handler))
        application.add_handler(CommandHandler("setlanguage", set_language_handler))
        application.add_handler(CommandHandler("shutdown", shutdown_handler))
        application.add_handler(CommandHandler("monitor", monitor_handler))

        # 4. Globaler Error-Handler
        application.add_error_handler(global_error_handler)

        # 5. Startup Tasks
        await execute_startup_tasks(application)

        # 7. Polling starten
        logger.info("✅ [Main] A.R.K. Bot online. Awaiting user interaction...")
        await application.run_polling(poll_interval=1.0)

    except Exception as e:
        logger.critical(f"🔥 [Main] Critical Failure: {e}")
        raise

# === Startpunkt ===
if __name__ == "__main__":
    asyncio.run(main())
