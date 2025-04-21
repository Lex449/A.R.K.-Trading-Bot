import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

# === Handler ===
from bot.handlers.start import start_handler
from bot.handlers.ping import ping_handler
from bot.handlers.signal import signal_handler
from bot.handlers.status import status_handler
from bot.handlers.analyse import analyse_handler
from bot.handlers.recap import recap_handler
from bot.handlers.shutdown import shutdown_handler

# === Fehlerbehandlung ===
from bot.utils.error_handler import handle_error

# === ENV laden ===
load_dotenv()
bot_token = os.getenv("BOT_TOKEN")

if not bot_token:
    raise ValueError("❌ BOT_TOKEN fehlt in der .env-Datei!")

print("✅ Bot-Token geladen. A.R.K. startet...")

# === App erstellen ===
app = ApplicationBuilder().token(bot_token).build()

# === Handler hinzufügen ===
app.add_handler(start_handler)
app.add_handler(ping_handler)
app.add_handler(signal_handler)
app.add_handler(status_handler)
app.add_handler(analyse_handler)
app.add_handler(recap_handler)
app.add_handler(shutdown_handler)

# === Fehlerbehandlung aktivieren ===
app.add_error_handler(handle_error)

# === Einstiegspunkt ===
if __name__ == "__main__":
    app.run_polling(non_stop=True)