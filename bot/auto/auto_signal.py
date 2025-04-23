import asyncio
import os
import time
from datetime import datetime
from telegram import Bot
from bot.utils.analysis import analyze_symbol
from bot.config import config

bot = Bot(token=os.getenv("BOT_TOKEN"))

# Signal-Tracking
last_sent_signals = {}

def log(message):
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] {message}")

async def send_signal(symbol, signal_data):
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not chat_id:
        log("❌ TELEGRAM_CHAT_ID fehlt in der .env")
        return

    message = (
        f"**Auto Signal für {symbol}**\n"
        f"Preis: {signal_data['price']}\n"
        f"Signal: {signal_data['signal']} ⭐️\n"
        f"RSI: {signal_data['rsi']:.2f}\n"
        f"Trend: {signal_data['trend']}\n"
        f"Muster: {signal_data['pattern']}"
    )
    await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
    log(f"✅ Signal gesendet für {symbol}: {signal_data['signal']}")

async def auto_signal_loop():
    symbols = config.AUTO_SIGNAL_SYMBOLS
    interval = int(config.SIGNAL_CHECK_INTERVAL_SEC)
    max_signals = int(config.MAX_SIGNALS_PER_HOUR)

    log("🔄 Auto-Signal-Loop gestartet...")

    while True:
        current_hour = datetime.now().strftime("%Y-%m-%d %H")
        for symbol in symbols:
            try:
                result = analyze_symbol(symbol)
                if not result or not result.get("signal"):
                    continue

                last_key = f"{symbol}_{current_hour}"
                if last_sent_signals.get(last_key, 0) >= max_signals:
                    continue  # Skip if max per hour reached

                await send_signal(symbol, result)
                last_sent_signals[last_key] = last_sent_signals.get(last_key, 0) + 1

            except Exception as e:
                log(f"❌ Fehler bei Analyse von {symbol}: {e}")

        await asyncio.sleep(interval)