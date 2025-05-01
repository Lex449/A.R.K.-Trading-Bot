"""
A.R.K. – Ultra Resilient Main Entry Point.
Bereinigt Webhook, initialisiert Telegram Bot und startet alle Tasks.
Made in Bali. Engineered with German Precision.
"""

import asyncio
import nest_asyncio
from telegram import Bot
from telegram.error import TelegramError
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

# Logger & ENV
logger = setup_logger(__name__)
config = get_settings()
nest_asyncio.apply()


# === Webhook Killer ===
async def force_webhook_deletion():
    try:
        bot = Bot(token=config["BOT_TOKEN"])
        logger.info("⚙️ [Webhook] Attempting to delete existing webhook...")
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("✅ [Webhook] Successfully deleted. Polling mode safe.")
    except TelegramError as te:
        logger.warning(f"⚠️ [Webhook] TelegramError during webhook deletion: {te}")
    except Exception as e:
        logger.error(f"❌ [Webhook] Failed to delete webhook: {e}")


# === Main Routine ===
async def main():
    logger.info("🚀 [Main] Booting A.R.K...")

    try:
        # Step 1 – Webhook-Schutz
        await force_webhook_deletion()

        # Step 2 – Bot-App starten
        application = ApplicationBuilder().token(config["BOT_TOKEN"]).build()

        # Step 3 – Command Handler
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("analyse", analyze_symbol_handler))
        application.add_handler(CommandHandler("signal", signal_handler))
        application.add_handler(CommandHandler("status", status_handler))
        application.add_handler(CommandHandler("uptime", uptime_handler))
        application.add_handler(CommandHandler("setlanguage", set_language_handler))
        application.add_handler(CommandHandler("shutdown", shutdown_handler))
        application.add_handler(CommandHandler("monitor", monitor_handler))

        # Step 4 – Fehlerbehandlung
        application.add_error_handler(global_error_handler)

        # Step 5 – Hintergrund-Jobs
        await execute_startup_tasks(application)

        # Step 6 – Starte Polling
        logger.info("✅ [Main] A.R.K. is now live and polling for events.")
        await application.run_polling(poll_interval=1.0)

    except Exception as e:
        logger.critical(f"🔥 [Main] Critical Launch Error: {e}")
        raise


# === Startpoint ===
if __name__ == "__main__":
    asyncio.run(main())
