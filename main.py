import asyncio
import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

# === Handler-Imports ===
from bot.handlers.start import start_handler
from bot.handlers.ping import ping_handler
from bot.handlers.status import status_handler
from bot.handlers.shutdown import shutdown_handler
from bot.handlers.signal import signal_handler
from bot.handlers.analyse import analyse_handler
from bot.handlers.testping import testping_handler
from bot.handlers.recap import recap_handler

# === Utils & Config ===
from bot.config.settings import get_settings
from bot.utils.error_handler import handle_error
from bot.utils.analysis import analyse_market

# === .env laden ===
load_dotenv()
bot_token = os.getenv("BOT_TOKEN")

if not bot_token:
    raise ValueError("❌ BOT_TOKEN fehlt in der .env-Datei!")

print("✅ BOT_TOKEN erfolgreich geladen")

# === App erstellen ===
app = ApplicationBuilder().token(bot_token).build()

# === Handler registrieren ===
app.add_handler(start_handler)
app.add_handler(ping_handler)
app.add_handler(status_handler)
app.add_handler(shutdown_handler)
app.add_handler(signal_handler)
app.add_handler(analyse_handler)
app.add_handler(testping_handler)
app.add_handler(recap_handler)

# === Fehlerbehandlung aktivieren ===
app.add_error_handler(handle_error)

# === Live-Analyse-Schleife ===
async def realtime_analysis():
    while True:
        indices = ['US100/USDT', 'US30/USDT', 'NAS100/USDT', 'SPX500/USDT']
        for index in indices:
            result = analyse_market(symbol=index)
            if result:
                trend = result["trend"]
                confidence = result["confidence"]
                pattern = result["pattern"]
                stars = "⭐️" * confidence + "✩" * (5 - confidence)

                message = (
                    f"📊 *Live-Analyse für {index}*\n"
                    f"Trend: *{trend}*\n"
                    f"Muster: *{pattern}*\n"
                    f"Signalqualität: {stars}\n\n"
                    f"_A.R.K. überwacht den Markt für dich._"
                )

                await app.bot.send_message(
                    chat_id="7699862580",
                    text=message,
                    parse_mode="Markdown"
                )
        await asyncio.sleep(60)

# === Bot + Analyse gemeinsam starten ===
async def run_all():
    await app.initialize()
    await asyncio.gather(
        app.start(),
        app.updater.start_polling(),
        realtime_analysis()
    )

# === Einstiegspunkt ===
if __name__ == "__main__":
    try:
        asyncio.run(run_all())
    except RuntimeError as e:
        if "event loop is already running" in str(e):
            print("⚠️ Railway Loop läuft bereits – alles okay.")
        else:
            raise