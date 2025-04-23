import asyncio
from datetime import datetime
from telegram import Bot
from bot.config.settings import get_settings
from bot.utils.analysis import analyze_symbol

config = get_settings()
bot = Bot(token=config["BOT_TOKEN"])
chat_id = config["TELEGRAM_CHAT_ID"]

last_sent_signals = {}

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

async def send_signal(symbol: str, result: dict):
    message = (
        f"📡 *Auto-Signal: {symbol}*\n"
        f"Preis: `{result['price']}`\n"
        f"Signal: *{result['signal']}*\n"
        f"RSI: `{result['rsi']:.2f}`\n"
        f"Trend: {result['trend']}\n"
        f"Muster: {result['pattern']}\n\n"
        f"_A.R.K. scannt rund um die Uhr – nur bei echtem Vorteil._"
    )
    await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
    log(f"✅ Signal gesendet für {symbol} → {result['signal']}")

async def auto_signal_loop():
    symbols = config["AUTO_SIGNAL_SYMBOLS"]
    interval = config["AUTO_SIGNAL_INTERVAL"]
    max_per_hour = config["MAX_SIGNALS_PER_HOUR"]

    log("⏱️ Auto-Signal-Loop gestartet...")

    while True:
        current_hour = datetime.now().strftime("%Y-%m-%d %H")
        for symbol in symbols:
            try:
                result = analyze_symbol(symbol)
                if not result or not result.get("signal"):
                    log(f"🔍 {symbol} → Kein verwertbares Signal.")
                    continue

                key = f"{symbol}_{current_hour}"
                if last_sent_signals.get(key, 0) >= max_per_hour:
                    log(f"⚠️ {symbol} → Max Signals für diese Stunde erreicht.")
                    continue

                await send_signal(symbol, result)
                last_sent_signals[key] = last_sent_signals.get(key, 0) + 1

            except Exception as e:
                log(f"❌ Fehler bei {symbol}: {e}")

        await asyncio.sleep(interval)
