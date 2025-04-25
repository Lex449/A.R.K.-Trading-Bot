# bot/auto/auto_signal.py
from bot.engine.analysis_engine import analyze_symbol
import asyncio
from datetime import datetime
from telegram import Bot
from bot.config.settings import get_settings
from bot.engine.analysis_engine import analyze_market  # Sicherstellen, dass der Import korrekt ist
from bot.utils.autoscaler import get_scaled_limit

# Bot- und Chat-Initialisierung
config = get_settings()
bot = Bot(token=config["BOT_TOKEN"])
chat_id = config["TELEGRAM_CHAT_ID"]
last_sent_signals = {}

# Verbesserte Logging-Funktion
def log(msg):
    """Präzise Log-Ausgaben für Debugging und Nachverfolgung."""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

# Signal senden an Telegram
async def send_signal(symbol: str, result: dict):
    """Sendet ein Handelssignal an Telegram mit allen wichtigen Marktdaten."""
    message = (
        f"📡 *Auto-Signal: {symbol}*\n"
        f"Preis: `{result['price']}`\n"
        f"Signal: *{result['signal']}*\n"
        f"RSI: `{result['rsi']:.2f}`\n"
        f"Trend: {result['trend']}\n"
        f"Muster: `{result['pattern']}`\n\n"
        f"_A.R.K. scannt rund um die Uhr – nur bei echtem Vorteil._"
    )
    try:
        await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
        log(f"✅ Signal gesendet für {symbol} → {result['signal']}")
    except Exception as e:
        log(f"[ERROR] Fehler beim Senden von Signal für {symbol}: {e}")

# Auto-Signal Loop – überprüft die Symbole regelmäßig
async def auto_signal_loop():
    """Schleife, die kontinuierlich die Symbole überprüft und Signale sendet."""
    symbols = config["AUTO_SIGNAL_SYMBOLS"]
    interval = config["SIGNAL_CHECK_INTERVAL_SEC"]
    log("⏱️ Auto-Signal-Loop gestartet...")

    while True:
        current_hour = datetime.utcnow().strftime("%Y-%m-%d %H")
        max_per_hour = get_scaled_limit(symbols)

        for symbol in symbols:
            try:
                # Marktdaten analysieren
                result = await analyze_market(symbol)
                if not result or not result.get("signal"):
                    log(f"[DEBUG] {symbol} → Kein verwertbares Signal.")
                    continue

                key = f"{symbol}_{current_hour}"
                if last_sent_signals.get(key, 0) >= max_per_hour:
                    log(f"⚠️ {symbol} → Limit erreicht ({max_per_hour}/h)")
                    continue

                # Signal senden
                await send_signal(symbol, result)
                last_sent_signals[key] = last_sent_signals.get(key, 0) + 1

            except Exception as e:
                log(f"[ERROR] Fehler bei {symbol}: {e}")

        # Schlafen für das Intervall
        await asyncio.sleep(interval)
