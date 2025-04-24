# bot/auto/auto_signal.py

import asyncio
from datetime import datetime
from telegram import Bot
from bot.config.settings import get_settings
from bot.utils.trading_logic import generate_trade_signal

config = get_settings()
bot = Bot(token=config["BOT_TOKEN"])
chat_id = config["DANIEL_TELEGRAM_ID"]

last_sent_signals = {}

def log(msg: str):
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] {msg}")

async def send_signal_to_telegram(signal: dict):
    message = (
        f"📡 *Auto-Signal: {signal['symbol']}*\n"
        f"Preis: `{signal['price']}`\n"
        f"Signal: *{signal['signal']}* ({signal['confidence']}⭐️)\n"
        f"RSI: `{signal['rsi']:.2f}`\n"
        f"Trend: `{signal['trend']}`\n"
        f"Muster: `{signal['pattern']}`\n"
        f"Kommentar: _{signal['comment']}_\n\n"
        f"_A.R.K. scannt rund um die Uhr – präzise & ohne Emotionen._"
    )

    await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
    log(f"✅ Signal gesendet für {signal['symbol']} → {signal['signal']}")

async def auto_signal_loop():
    log("🔁 Auto-Signal-Loop läuft...")

    symbols = config["AUTO_SIGNAL_SYMBOLS"]
    interval = config["AUTO_SIGNAL_INTERVAL"]
    max_per_hour = config["MAX_SIGNALS_PER_HOUR"]

    while True:
        current_hour = datetime.now().strftime("%Y-%m-%d %H")

        for symbol in symbols:
            try:
                result = generate_trade_signal(symbol)

                if not result or result.get("signal") is None:
                    log(f"⏸️ {symbol}: Kein verwertbares Signal.")
                    continue

                key = f"{symbol}_{current_hour}"
                if last_sent_signals.get(key, 0) >= max_per_hour:
                    log(f"⚠️ {symbol}: Max. Signale erreicht ({max_per_hour}/h)")
                    continue

                await send_signal_to_telegram(result)
                last_sent_signals[key] = last_sent_signals.get(key, 0) + 1

            except Exception as e:
                log(f"❌ Fehler bei {symbol}: {e}")

        await asyncio.sleep(interval)
