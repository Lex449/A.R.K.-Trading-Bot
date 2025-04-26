# bot/main.py

import asyncio
import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler
from bot.handlers.commands import start, help_command, analyze_symbol, set_language
from bot.handlers.signal import signal_handler
from bot.handlers.status import status_handler
from bot.handlers.shutdown import shutdown_handler
from bot.auto.auto_signal import auto_signal_loop
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings
from bot.utils.logging import setup_logger

# === Setup Logging ===
setup_logger()

# === Load Environment ===
load_dotenv()
config = get_settings()
TOKEN = config["BOT_TOKEN"]

# === Start Telegram Bot ===
async def start_telegram_bot():
    logging.info("🚀 Starting A.R.K. Bot – Made in Bali. Engineered with German Precision.")

    app = ApplicationBuilder().token(TOKEN).build()

    # Register Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("analyse", analyze_symbol))
    app.add_handler(CommandHandler("setlanguage", set_language))
    app.add_handler(CommandHandler("signal", signal_handler))
    app.add_handler(CommandHandler("status", status_handler))
    app.add_handler(CommandHandler("shutdown", shutdown_handler))

    return app

# === Main Application ===
async def main():
    app = await start_telegram_bot()

    # Launch Auto Signal Loop separately
    auto_signal_task = asyncio.create_task(auto_signal_loop())

    try:
        await app.start()
        await app.updater.start_polling()
        logging.info("✅ Bot polling and auto-signal running.")
        await app.updater.idle()
    except Exception as e:
        logging.critical(f"❌ Critical Error in Bot: {e}")
        await report_error(app.bot, int(config["TELEGRAM_CHAT_ID"]), e, context_info="Main Polling Error")
    finally:
        auto_signal_task.cancel()
        await app.stop()
        await app.shutdown()
        logging.info("🛑 Bot stopped cleanly.")

# === Entry Point ===
if __name__ == "__main__":
    asyncio.run(main())
