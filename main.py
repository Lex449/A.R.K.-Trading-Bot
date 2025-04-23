import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from bot.handlers.start import start_handler
from bot.handlers.ping import ping_handler
from bot.handlers.signal import signal_handler
from bot.handlers.status import status_handler
from bot.handlers.analyse import analyse_handler
from bot.handlers.recap import recap_handler
from bot.handlers.shutdown import shutdown_handler
from bot.utils.error_handler import handle_error
from bot.auto.auto_signal import auto_signal_loop  # Automatische Signale
import asyncio
import nest_asyncio

# === ENV laden ===
load_dotenv()
bot_token = os.getenv("BOT_TOKEN")

if not bot_token:
    raise ValueError("❌ BOT_TOKEN fehlt in der .env-Datei!")

print("✅ Bot-Token geladen. A.R.K. startet...")

# === App erstellen ===
app = Application.builder().token(bot_token).build()

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
async def main():
    try:
        print("🚀 Bot läuft im Polling-Modus...")
        
        # Auto-Signals in einem separaten Task ausführen
        asyncio.create_task(auto_signal_loop())  # Das automatische Signal läuft im Hintergrund

        # Starte den Polling-Modus des Bots
        await app.run_polling()

    except Exception as e:
        print(f"❌ Fehler im Hauptprozess: {e}")

if __name__ == "__main__":
    # Bei Verwendung von asyncio innerhalb von Replit/Colab/andere Asynchrone Umgebungen wird nest_asyncio verwendet
    nest_asyncio.apply()  # Dies löst das Event-Loop-Problem, wenn es mehrfach ausgeführt wird.
    
    # Starte das Hauptprogramm
    asyncio.run(main())