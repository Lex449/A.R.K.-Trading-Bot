# bot/main.py

import asyncio
import logging
import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler
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

# === Load .env ===
load_dotenv()

# === Validate critical ENV variables ===
config = get_settings()
TOKEN = config["BOT_TOKEN"]

async def main():
    logging.info("🚀 A.R.K. Bot 2.0 – Made in Bali. Engineered with German Precision.")

    # === Build Application ===
    app = ApplicationBuilder().token(TOKEN).build()

    # === Register Handlers ===
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("analyse", analyze_symbol))
    app.add_handler(CommandHandler("setlanguage", set_language))
    app.add_handler(CommandHandler("signal", signal_handler))
    app.add_handler(CommandHandler("status", status_handler))
    app.add_handler(CommandHandler("shutdown", shutdown_handler))

    # === Initialize Application ===
    await app.initialize()

    # === Start Application ===
    await app.start()

    # === Launch Auto Signal Loop parallel ===
    async def run_background_tasks():
        try:
            await auto_signal_loop()
        except Exception as e:
            await report_error(app.bot, int(config["TELEGRAM_CHAT_ID"]), e, context_info="Auto Signal Loop Error")

    asyncio.create_task(run_background_tasks())

    # === Run Polling separately ===
    await app.updater.start_polling()

    # === Wait until shutdown signal ===
    await app.stop()
    await app.shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("💤 Bot shutdown signal received.")
