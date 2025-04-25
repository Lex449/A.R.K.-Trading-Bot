# main.py

import asyncio
import logging
import nest_asyncio
import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler
from bot.handlers.commands import start, help_command, analyse_symbol, set_language
from bot.auto.auto_signal import auto_signal_loop

# === Setup Logging ===
logging.basicConfig(
    format='[%(asctime)s] %(levelname)s – %(message)s',
    level=logging.INFO
)

# === ENV vorbereiten ===
load_dotenv()
nest_asyncio.apply()
TOKEN = os.getenv("BOT_TOKEN")

# === Main ===
async def main():
    if not TOKEN:
        logging.error("❌ BOT_TOKEN nicht gefunden in .env – Abbruch.")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    # === Befehle verbinden ===
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("analyse", analyse_symbol))
    app.add_handler(CommandHandler("setlanguage", set_language))

    # === Auto-Signal starten ===
    app.create_task(auto_signal_loop())

    # === Startmeldung ===
    logging.info("🚀 A.R.K. Bot 1.0 aktiviert – bereit für Signale und Befehle...")

    # === Bot starten ===
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
