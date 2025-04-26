# bot/main.py

import asyncio
import logging
import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler
from bot.handlers.commands import start, help_command, analyze_symbol, set_language
from bot.handlers.signal import signal_handler
from bot.handlers.status import status
from bot.handlers.shutdown import shutdown_handler
from bot.auto.auto_signal import auto_signal_loop
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings
from bot.utils.logging import setup_logger
from telegram import Update

# === Setup Logging ===
setup_logger()

# === Load .env ===
load_dotenv()

# === Validate critical ENV variables ===
config = get_settings()
TOKEN = config["BOT_TOKEN"]

# === Main Async Application ===
async def main():
    logging.info("🚀 A.R.K. Bot 2.0 – Made in Bali. Engineered with German Precision.")

    app = ApplicationBuilder().token(TOKEN).build()

    # === Register Handlers ===
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("analyse", analyze_symbol))
    app.add_handler(CommandHandler("setlanguage", set_language))
    app.add_handler(CommandHandler("signal", signal_handler))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("shutdown", shutdown_handler))

    # === Start Background Auto-Signal Loop ===
    async def start_auto_signals():
        try:
            await auto_signal_loop()
        except Exception as e:
            await report_error(app.bot, int(config["TELEGRAM_CHAT_ID"]), e, context_info="Auto Signal Loop")

    asyncio.create_task(start_auto_signals())

    # === Run Bot ===
    try:
        await app.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logging.critical(f"❌ Critical Error in Bot: {e}")
        await report_error(app.bot, int(config["TELEGRAM_CHAT_ID"]), e, context_info="Main Polling Error")

if __name__ == "__main__":
    asyncio.run(main())
