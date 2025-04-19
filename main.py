import asyncio
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
from dotenv import load_dotenv
import os
from bot.utils.analysis import analyse_market  # Importiere die Marktanalyse-Funktion

# Lade die .env-Datei
load_dotenv()

# Hole den Bot-Token aus der .env-Datei
bot_token = os.getenv("BOT_TOKEN")

# Überprüfe, ob der Token geladen wurde
if not bot_token:
    raise ValueError("BOT_TOKEN konnte nicht aus der .env-Datei geladen werden!")

print("Bot Token:", bot_token)

# Telegram Bot Anwendung erstellen
app = ApplicationBuilder().token(bot_token).build()

# Handler hinzufügen
app.add_handler(start_handler)
app.add_handler(ping_handler)
app.add_handler(status_handler)
app.add_handler(shutdown_handler)
app.add_handler(signal_handler)
app.add_handler(analyse_handler)
app.add_handler(testping_handler)

# Fehlerbehandlung aktivieren
app.add_error_handler(handle_error)

# Funktion zur Echtzeit-Analyse
async def realtime_analysis():
    while True:
        # Analysiere mehrere Indizes: US100, US30, NAS100, SPX500
        indices = ['US100/USDT', 'US30/USDT', 'NAS100/USDT', 'SPX500/USDT']
        for index in indices:
            result = analyse_market(symbol=index)

            if result:
                # Hier kannst du das Ergebnis an den Telegram-Bot senden
                trend = result["trend"]
                confidence = result["confidence"]
                pattern = result["pattern"]
                stars = "⭐️" * confidence + "✩" * (5 - confidence)

                # Sende das Signal an die Nutzer
                message = f"📊 *Marktanalyse für {index}*\nTrend: {trend}\nMuster: {pattern}\nSignalqualität: {stars}\n"
                await app.bot.send_message(chat_id="7699862580", text=message)  # Ersetze DEIN_CHAT_ID mit deinem ID

        # Warte 60 Sekunden, bevor die Analyse erneut ausgeführt wird
        await asyncio.sleep(60)  # Zeit in Sekunden

# DNS-Monitor und Bot gemeinsam starten
async def run_all():
    await app.initialize()  # Initialisiere den Bot
    await asyncio.gather(
        app.start(),  # Bot starten
        app.updater.start_polling(),  # Polling starten
        realtime_analysis()  # Echtzeit-Analyse in den Loop integrieren
    )

# Einstiegspunkt
if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(run_all())
        loop.run_forever()
    except RuntimeError as e:
        if str(e).startswith("This event loop is already running"):
            print("⚠️ Fehler: Event-Loop läuft bereits. Railway kann das verursachen.")
        else:
            raise