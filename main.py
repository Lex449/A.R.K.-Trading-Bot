"""
A.R.K. – Ultra Resilient Main Entry Point.
Bereinigt Webhook, initialisiert Telegram Bot und startet alle Tasks.
"""

import asyncio
import nest_asyncio
from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler
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

# Logger & Settings
logger = setup_logger(__name__)
config = get_settings()
nest_asyncio.apply()

# === Main Routine ===
async def main():
    logger.info("🚀 [Main] Launching A.R.K...")

    try:
        # Step 1: Webhook entfernen – direkt, vor Bot-Erstellung!
        bot = Bot(token=config["BOT_TOKEN"])
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("✅ [Init] Webhook successfully removed.")

        # Step 2: Bot erstellen
        application = ApplicationBuilder().token(config["BOT_TOKEN"]).build()

        # Step 3: Command Handler
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("analyse", analyze_symbol_handler))
        application.add_handler(CommandHandler("signal", signal_handler))
        application.add_handler(CommandHandler("status", status_handler))
        application.add_handler(CommandHandler("uptime", uptime_handler))
        application.add_handler(CommandHandler("setlanguage", set_language_handler))
        application.add_handler(CommandHandler("shutdown", shutdown_handler))
        application.add_handler(CommandHandler("monitor", monitor_handler))

        # Step 4: Fehler-Handler
        application.add_error_handler(global_error_handler)

        # Step 5: Startup Tasks & Hintergrundjobs
        await execute_startup_tasks(application)

        # Step 6: Polling aktivieren
        logger.info("✅ [Main] A.R.K. fully online – Awaiting interaction.")
        await application.run_polling(poll_interval=1.0)

    except Exception as e:
        logger.critical(f"🔥 [Main] Fatal startup failure: {e}")
        raise

# === Entry Point ===
if __name__ == "__main__":
    asyncio.run(main())
