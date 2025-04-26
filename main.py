# bot/main.py

import asyncio
import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler
from telegram import Update
from bot.handlers.commands import start, help_command, analyze_symbol, set_language
from bot.handlers.signal import signal_handler
from bot.handlers.status import status
from bot.handlers.shutdown import shutdown_handler
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings
from bot.scheduler.scheduler import setup_scheduler
from bot.utils.logging import setup_logger

# === Global Logger Setup ===
setup_logger()

# === Load Environment Variables ===
load_dotenv()

# === Load and Validate Config ===
config = get_settings()
TOKEN = config["BOT_TOKEN"]

# === Main Async Bot Application ===
async def main():
    from logging import getLogger
    logger = getLogger(__name__)

    logger.info("🚀 A.R.K. Bot 2.0 – Made in Bali. Engineered with German Precision. Initializing...")

    app = ApplicationBuilder().token(TOKEN).build()

    # === Register Command Handlers ===
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("analyse", analyze_symbol))
    app.add_handler(CommandHandler("setlanguage", set_language))
    app.add_handler(CommandHandler("signal", signal_handler))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("shutdown", shutdown_handler))

    # === Setup Background Scheduler ===
    setup_scheduler(app)

    # === Run Bot with Error Handling ===
    try:
        await app.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logger.critical(f"❌ Critical Error in Bot Execution: {e}")
        await report_error(app.bot, int(config["TELEGRAM_CHAT_ID"]), e, context_info="Main Polling Crash")

# === Entrypoint ===
if __name__ == "__main__":
    asyncio.run(main())
