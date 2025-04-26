import logging
import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler
from bot.handlers.commands import start, help_command, analyse_symbol, set_language
from bot.auto.auto_signal import auto_signal_loop
from telegram import Update

# === Setup Logging ===
logging.basicConfig(
    format='[%(asctime)s] %(levelname)s – %(message)s',
    level=logging.INFO
)

# === ENV laden ===
load_dotenv()

# === Umgebungsvariablen prüfen ===
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    logging.error("❌ BOT_TOKEN fehlt – Abbruch.")
    exit(1)

# === Hauptfunktion ===
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # === Handler ===
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("analyse", analyse_symbol))
    app.add_handler(CommandHandler("setlanguage", set_language))

    # === Log und Start-Info ===
    logging.info("🚀 A.R.K. Bot 1.0 – Made in Bali. Engineered with German Precision.")
    
    # === Starte den Bot sauber ===
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
