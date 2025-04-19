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
from bot.utils.dns_monitor import check_dns_and_notify
from dotenv import load_dotenv
import os

# Lade die .env-Datei
load_dotenv()

# Holen der Einstellungen aus der .env-Datei
settings = get_settings()
print("Bot Token:", os.getenv("BOT_TOKEN"))
print("Daniel's Telegram ID:", os.getenv("DANIEL_TELEGRAM_ID"))

# Telegram Bot Anwendung erstellen
app = ApplicationBuilder().token(settings["TOKEN"]).build()

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
    await asyncio.gather(
        app.initialize(),            # Initialisierung des Bots
        check_dns_and_notify(),      # DNS-Monitoring
        app.start(),                 # Bot starten
        app.updater.start_polling()  # Polling starten
    )

# Einstiegspunkt
if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(run_all())
        loop.run_forever()
    except RuntimeError as e:
        if str(e).startswith("This event loop is already running"):
            print("⚠️ Fehler: Event-Loop läuft bereits. Railway kann das verursachen.")
        else:
            raise