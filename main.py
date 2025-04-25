import asyncio
import logging
import nest_asyncio
import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler
from bot.handlers.commands import start, help_command, analyse_symbol, set_language
from bot.auto.auto_signal import auto_signal_loop  # Import von auto_signal_loop bleibt

# === Setup Logging ===
logging.basicConfig(
    format='[%(asctime)s] %(levelname)s – %(message)s',
    level=logging.INFO
)

# === ENV vorbereiten ===
load_dotenv()
nest_asyncio.apply()

# === Umgebungsvariablen laden und prüfen ===
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    logging.error("❌ BOT_TOKEN nicht gefunden in .env – Abbruch.")
    exit(1)

TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
if not TELEGRAM_CHAT_ID:
    logging.error("❌ TELEGRAM_CHAT_ID nicht gefunden in .env – Abbruch.")
    exit(1)

TWELVEDATA_API_KEY = os.getenv("TWELVEDATA_API_KEY")
if not TWELVEDATA_API_KEY:
    logging.error("❌ TWELVEDATA_API_KEY nicht gefunden in .env – Abbruch.")
    exit(1)

INTERVAL = os.getenv("INTERVAL", "1min")
if INTERVAL not in ["1min", "5min", "15min", "30min", "60min"]:
    logging.error(f"❌ Ungültiges Intervall `{INTERVAL}` in .env. Erwartet: 1min, 5min, 15min, 30min oder 60min.")
    exit(1)

# === Main ===
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # === Befehle verbinden ===
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("analyse", analyse_symbol))
    app.add_handler(CommandHandler("setlanguage", set_language))

    # === Startmeldung ===
    logging.info("🚀 A.R.K. Bot 1.0 aktiviert – bereit für Signale und Befehle...")

    # === Bot starten ===
    await app.run_polling()

    # *** Hier den Auto-Signal Loop starten ***
    # Nachdem die Anwendung und der Bot initialisiert sind, starten wir den Auto-Signal-Loop
    await auto_signal_loop()

if __name__ == "__main__":
    asyncio.run(main())
