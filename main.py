import asyncio
from telegram.ext import ApplicationBuilder
from bot.handlers.start import start_handler
from bot.handlers.ping import ping_handler
from bot.handlers.status import status_handler
from bot.handlers.shutdown import shutdown_handler
from bot.handlers.signal import signal_handler
from bot.handlers.analyse import analyse_handler
from bot.handlers.testping import testping_handler
from bot.config.settings import get_settings
from bot.utils.error_handler import handle_error
from dotenv import load_dotenv
import os

# Lade die .env-Datei
load_dotenv()

# Hole den Bot-Token aus der .env-Datei
bot_token = os.getenv("BOT_TOKEN")

# Überprüfe, ob der Token geladen wurde
if not bot_token:
    raise ValueError("BOT_TOKEN konnte nicht aus der .env-Datei geladen werden!")

print("Bot Token:", bot_token)

# Telegram Bot Anwendung erstellen
app = ApplicationBuilder().token(bot_token).build()

# Handler hinzufügen
app.add_handler(start_handler)
app.add_handler(ping_handler)
app.add_handler(status_handler)
app.add_handler(shutdown_handler)
app.add_handler(signal_handler)
app.add_handler(analyse_handler)
app.add_handler(testping_handler)

# Fehlerbehandlung aktivieren
app.add_error_handler(handle_error)

# DNS-Monitor und Bot gemeinsam starten
async def run_all():
    await app.initialize()            # Initialisiere den Bot
    await asyncio.gather(
        app.start(),                 # Bot starten
        app.updater.start_polling()  # Polling starten
    )

# Einstiegspunkt
if __name__ == "__main__":
    try:
        asyncio.run(run_all())  # Verwende asyncio.run anstelle von loop.create_task
    except RuntimeError as e:
        if str(e).startswith("This event loop is already running"):
            print("⚠️ Fehler: Event-Loop läuft bereits. Railway kann das verursachen.")
        else:
            raise