# main.py

import os
import asyncio
import nest_asyncio
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

from bot.handlers.start import start_handler
from bot.handlers.ping import ping_handler
from bot.handlers.status import status_handler
from bot.handlers.signal import signal_handler
from bot.handlers.analyse import analyse_handler
from bot.handlers.shutdown import shutdown_handler
from bot.handlers.recap import recap_handler
from bot.handlers.help import help_handler

from bot.utils.error_handler import handle_error
from bot.auto.auto_signal import auto_signal_loop

# === ENV laden ===
load_dotenv()
bot_token = os.getenv("BOT_TOKEN")

if not bot_token:
    raise ValueError("❌ BOT_TOKEN fehlt. Bitte in .env oder Railway Variable setzen!")

print("✅ Bot-Token geladen. Initialisiere A.R.K...")

# === Telegram App vorbereiten ===
app = ApplicationBuilder().token(bot_token).build()

# === Handler binden ===
app.add_handler(start_handler)
app.add_handler(ping_handler)
app.add_handler(status_handler)
app.add_handler(signal_handler)
app.add_handler(analyse_handler)
app.add_handler(recap_handler)
app.add_handler(shutdown_handler)
app.add_handler(help_handler)

app.add_error_handler(handle_error)

# === Async für Railway ===
nest_asyncio.apply()

# === Startfunktion ===
async def main():
    print("🚀 A.R.K. aktiviert. Signale werden überwacht...")
    asyncio.create_task(auto_signal_loop())
    await app.run_polling()

# === Starte Bot ===
asyncio.run(main())
