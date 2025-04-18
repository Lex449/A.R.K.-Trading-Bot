import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from bot.config.settings import get_settings
from bot.handlers.start import start
from bot.handlers.ping import ping
from bot.handlers.status import status
from bot.handlers.shutdown import shutdown
from bot.handlers.signal import signal
from bot.handlers.analyse import analyse
from bot.handlers.error_handler import error_handler

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Lade Einstellungen
settings = get_settings()

# Baue Application
application = ApplicationBuilder().token(settings["TELEGRAM_BOT_TOKEN"]).build()

# Handler registrieren
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("ping", ping))
application.add_handler(CommandHandler("status", status))
application.add_handler(CommandHandler("shutdown", shutdown))
application.add_handler(CommandHandler("signal", signal))
application.add_handler(CommandHandler("analyse", analyse))

# Error-Handler
application.add_error_handler(error_handler)

# Starte den Bot
if __name__ == "__main__":
    application.run_polling()