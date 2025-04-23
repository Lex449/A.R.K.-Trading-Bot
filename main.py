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

if not bot_token or not bot_token.startswith("765"):  # Absicherung gegen falschen Token
    raise ValueError("❌ Ungültiger oder fehlender BOT_TOKEN in der .env oder Railway Variables!")

print("✅ Bot-Token erfolgreich geladen – A.R.K. wird initialisiert...")

# === Anwendung initialisieren ===
app = ApplicationBuilder().token(bot_token).build()

# === Handler einbinden ===
app.add_handler(start_handler)
app.add_handler(ping_handler)
app.add_handler(signal_handler)
app.add_handler(status_handler)
app.add_handler(analyse_handler)
app.add_handler(recap_handler)
app.add_handler(shutdown_handler)

# === Fehler-Logging aktivieren ===
app.add_error_handler(handle_error)

# === Async-Fix für Railway (nest_asyncio) ===
nest_asyncio.apply()

# === Hauptprozess definieren ===
async def main():
    try:
        print("🚀 A.R.K. Trading Bot läuft jetzt live im Polling-Modus!")
        asyncio.create_task(auto_signal_loop())  # Hintergrundanalyse aktivieren
        await app.run_polling()  # Bot starten

    except Exception as e:
        print(f"❌ Fataler Fehler beim Start: {e}")
        await asyncio.sleep(5)  # Retry-Delay (optional)
        raise

# === Ausführung ===
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())