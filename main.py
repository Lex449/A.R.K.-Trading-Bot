# bot/main.py

import asyncio
import logging
import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler
from telegram import Update
from bot.handlers.commands import start, help_command, analyze_symbol, set_language
from bot.handlers.signal import signal_handler
from bot.handlers.status import status_handler
from bot.handlers.shutdown import shutdown_handler
from bot.auto.auto_signal import auto_signal_loop
from bot.utils.error_reporter import report_error
from bot.utils.logging import setup_logger
from bot.config.settings import get_settings

# === Setup Logging ===
setup_logger()

# === Load .env Variables ===
load_dotenv()

# === Load Settings ===
config = get_settings()
TOKEN = config["BOT_TOKEN"]

async def run_bot():
    logging.info("🚀 A.R.K. Bot 2.0 – Made in Bali. Engineered with German Precision.")

    # === Build the Application ===
    app = ApplicationBuilder().token(TOKEN).build()

    # === Register Handlers ===
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("analyse", analyze_symbol))
    app.add_handler(CommandHandler("setlanguage", set_language))
    app.add_handler(CommandHandler("signal", signal_handler))
    app.add_handler(CommandHandler("status", status_handler))
    app.add_handler(CommandHandler("shutdown", shutdown_handler))

    # === Initialize App (Important!) ===
    await app.initialize()

    # === Start Auto Signal Loop (Parallel) ===
    asyncio.create_task(auto_signal_loop())

    # === Start Polling ===
    await app.start()
    await app.updater.start_polling()

    # === Keep Bot Running ===
    await app.updater.idle()

    # === Shutdown Safely ===
    await app.stop()
    await app.shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(run_bot())
    except Exception as e:
        logging.critical(f"❌ Critical Error in Bot Main Loop: {e}")
