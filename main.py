# bot/main.py

import asyncio
import logging
import os
from dotenv import load_dotenv
import nest_asyncio
from telegram.ext import ApplicationBuilder, CommandHandler
from bot.handlers.commands import start, help_command, analyse_symbol, set_language
from bot.auto.auto_signal import auto_signal_loop
from bot.utils.error_reporter import report_error

# === Logging Setup ===
logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# === Environment Preparation ===
load_dotenv()
nest_asyncio.apply()

# === Environment Variables Loading ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

required_env_vars = {
    "BOT_TOKEN": BOT_TOKEN,
    "TELEGRAM_CHAT_ID": TELEGRAM_CHAT_ID,
    "FINNHUB_API_KEY": FINNHUB_API_KEY
}

missing_vars = [key for key, value in required_env_vars.items() if not value]
if missing_vars:
    logger.error(f"❌ Missing required environment variables: {', '.join(missing_vars)}. Exiting.")
    exit(1)

# === Main Application ===
async def main():
    try:
        app = ApplicationBuilder().token(BOT_TOKEN).build()

        # === Register Command Handlers ===
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("analyse", analyse_symbol))
        app.add_handler(CommandHandler("setlanguage", set_language))

        logger.info("🚀 A.R.K. Trading Bot activated and ready for commands.")

        # === Start Auto-Signal Loop asynchronously ===
        asyncio.create_task(auto_signal_loop())

        # === Run the Bot ===
        await app.run_polling()

    except Exception as e:
        logger.critical(f"Critical Error in Main Loop: {e}")
        # Attempt to send error to Telegram
        try:
            from telegram import Bot
            bot = Bot(token=BOT_TOKEN)
            await report_error(bot, int(TELEGRAM_CHAT_ID), e, context_info="Main Application Error")
        except Exception as inner_error:
            logger.critical(f"Failed to report main error via Telegram: {inner_error}")

if __name__ == "__main__":
    asyncio.run(main())
