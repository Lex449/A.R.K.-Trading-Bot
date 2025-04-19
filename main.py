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
import asyncio

# Einstellungen laden
settings = get_settings()

# Telegram-Bot Anwendung aufbauen
app = ApplicationBuilder().token(settings["TOKEN"]).build()

# Handler registrieren
app.add_handler(start_handler)
app.add_handler(ping_handler)
app.add_handler(status_handler)
app.add_handler(shutdown_handler)
app.add_handler(signal_handler)
app.add_handler(analyse_handler)
app.add_handler(testping_handler)

# Fehlerbehandlung aktivieren
app.add_error_handler(handle_error)

# DNS-Monitoring starten
async def run_dns_monitor():
    while True:
        await check_dns_and_notify()
        await asyncio.sleep(900)  # Alle 15 Minuten erneut überprüfen

# Bot und DNS-Monitoring gemeinsam starten
async def run():
    # Starte DNS-Monitoring und Polling für den Bot parallel
    await asyncio.gather(
        run_dns_monitor(),
        app.run_polling()  # Startet den Bot
    )

if __name__ == "__main__":
    try:
        asyncio.run(run())
    except RuntimeError as e:
        if str(e).startswith("This event loop is already running"):
            print("⚠️ Fehler: Event-Loop läuft bereits. Railway kann das verursachen.")
        else:
            raise