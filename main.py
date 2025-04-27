# bot/main.py

import asyncio
import logging
import nest_asyncio
from telegram.ext import ApplicationBuilder, CommandHandler
from bot.handlers.commands import start, help_command, analyze_symbol, set_language
from bot.handlers.signal import signal_handler
from bot.handlers.status import status_handler
from bot.handlers.shutdown import shutdown_handler
from bot.auto.auto_signal import auto_signal_loop
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings
from bot.utils.logging import setup_logger
from telegram import Update

# === Setup Logging ===
setup_logger()

# === Allow nested event loops (important for Replit and Railway) ===
nest_asyncio.apply()

# === Load configuration ===
config = get_settings()
TOKEN = config["BOT_TOKEN"]

async def start_auto_signals(app):
    """
    Separate Task for Auto Signal Loop
    """
    try:
        await auto_signal_loop()
    except Exception as e:
        await report_error(app.bot, int(config["TELEGRAM_CHAT_ID"]), e, context_info="Auto Signal Loop")

async def main():
    logging.info("🚀 A.R.K. Bot 2.0 – Made in Bali. Engineered with German Precision.")

    # Initialize Application
    app = ApplicationBuilder().token(TOKEN).build()

    # Register Command Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("analyse", analyze_symbol))
    app.add_handler(CommandHandler("setlanguage", set_language))
    app.add_handler(CommandHandler("signal", signal_handler))
    app.add_handler(CommandHandler("status", status_handler))
    app.add_handler(CommandHandler("shutdown", shutdown_handler))

    # Start Auto-Signal Loop in Background
    asyncio.create_task(start_auto_signals(app))

    # Start Polling
    await app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    asyncio.run(main())
