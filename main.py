import asyncio
import os
from telegram.ext import ApplicationBuilder
from dotenv import load_dotenv

# === Handler ===
from bot.handlers.start import start_handler
from bot.handlers.ping import ping_handler
from bot.handlers.status import status_handler
from bot.handlers.signal import signal_handler
from bot.handlers.analyse import analyse_handler
from bot.handlers.recap import recap_handler

# === Utils ===
from bot.utils.analysis import analyse_market
from bot.utils.error_handler import handle_error

# === Lade .env ===
load_dotenv()
bot_token = os.getenv("BOT_TOKEN")

if not bot_token:
    raise ValueError("❌ BOT_TOKEN fehlt in der .env-Datei!")

print("✅ BOT_TOKEN geladen")

# === Telegram App erstellen ===
app = ApplicationBuilder().token(bot_token).build()

# === Handler hinzufügen ===
app.add_handler(start_handler)
app.add_handler(ping_handler)
app.add_handler(status_handler)
app.add_handler(signal_handler)
app.add_handler(analyse_handler)
app.add_handler(recap_handler)

# === Fehlerbehandlung aktivieren ===
app.add_error_handler(handle_error)

# === Live-Analyse-Loop ===
async def realtime_analysis():
    while True:
        indices = ['US100/USDT', 'US30/USDT', 'NAS100/USDT', 'SPX500/USDT']
        for symbol in indices:
            result = analyse_market(symbol)
            if result:
                trend = result["trend"]
                confidence = result["confidence"]
                pattern = result["pattern"]
                stars = "⭐️" * confidence + "✩" * (5 - confidence)

                message = (
                    f"📊 *Live-Analyse für {symbol}*\n"
                    f"Trend: *{trend}*\n"
                    f"Muster: *{pattern}*\n"
                    f"Signalqualität: {stars}\n\n"
                    f"_A.R.K. überwacht den Markt für dich._"
                )

                await app.bot.send_message(
                    chat_id="7699862580",  # Deine Telegram-ID
                    text=message,
                    parse_mode="Markdown"
                )

        await asyncio.sleep(60)

# === Starte Bot + Analyse gemeinsam ===
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
        loop = asyncio.get_event_loop()
        loop.create_task(run_all())
        loop.run_forever()
    except RuntimeError as e:
        if "event loop is already running" in str(e):
            print("⚠️ Railway-Loop läuft bereits.")
        else:
            raise