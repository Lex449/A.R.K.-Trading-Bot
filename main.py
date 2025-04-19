# main.py

from telegram.ext import ApplicationBuilder
from bot.handlers.start import start
from bot.handlers.ping import ping
from bot.handlers.status import status
from bot.handlers.shutdown import shutdown
from bot.handlers.signal import signal
from bot.handlers.analyse import analyse
from bot.config.settings import get_settings
from bot.utils.error_handler import handle_error

# Einstellungen laden
settings = get_settings()

# Bot-Anwendung erstellen
app = ApplicationBuilder().token(settings["TOKEN"]).build()

# Handler hinzufügen
app.add_handler(start)
app.add_handler(ping)
app.add_handler(status)
app.add_handler(shutdown)
app.add_handler(signal)
app.add_handler(analyse)

# Fehlerbehandlung
app.add_error_handler(handle_error)

# Bot starten
if __name__ == "__main__":
    app.run_polling()