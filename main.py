import os
import asyncio
import nest_asyncio
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

from bot.handlers.start import start_handler
from bot.handlers.ping import ping_handler
from bot.handlers.signal import signal_handler
from bot.handlers.status import status_handler
from bot.handlers.analyse import analyse_handler
from bot.handlers.recap import recap_handler
from bot.handlers.shutdown import shutdown_handler
from bot.utils.error_handler import handle_error
from bot.auto.auto_signal import auto_signal_loop

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

# === Replit-Kompatibilität herstellen ===
nest_asyncio.apply()

async def main():
    print("🚀 Bot läuft im Polling-Modus (Replit-safe)...")

    await app.initialize()
    asyncio.create_task(auto_signal_loop())  # Auto-Signale starten
    await app.start()  # Starte Bot
    await app.updater.start_polling()  # Explizit Polling-Modus starten
    await app.updater.idle()  # Bis Stop warten

# Starte Event Loop
asyncio.get_event_loop().run_until_complete(main())