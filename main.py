"""
A.R.K. Bot Main Entry – Ultra Stable Wall Street Version 2.0
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
from bot.handlers.global_error_handler import global_error_handler  # <-- FIX: richtiger Import
from bot.handlers.set_my_commands import set_bot_commands

# === Auto Signal Loop ===
from bot.auto.auto_signal_loop import auto_signal_loop

# === Utilities ===
from bot.utils.error_reporter import report_error
from bot.utils.logger import setup_logger
from bot.config.settings import get_settings

# === Setup Logging ===
setup_logger(__name__)

# === Allow nested event loops (Railway / Replit Support) ===
nest_asyncio.apply()

# === Load Config ===
config = get_settings()
TOKEN = config["BOT_TOKEN"]

async def startup_tasks(application):
    """
    Launches background services when Bot starts (no polling conflict).
    """
    try:
        # Delete old webhook to ensure polling works
        await application.bot.delete_webhook(drop_pending_updates=True)

        # Start Auto Signal Loop
        asyncio.create_task(auto_signal_loop(application.bot))

        # Set clean /command list
        await set_bot_commands(application)

    except Exception as e:
        await report_error(application.bot, int(config["TELEGRAM_CHAT_ID"]), e, context_info="Startup Task Error")

async def main():
    logging.info("🚀 A.R.K. Trading Bot 2.0 – Wall Street Stability Mode activated.")

    # Initialize Bot Application
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

    # === Start Bot ===
    await app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    asyncio.run(main())
