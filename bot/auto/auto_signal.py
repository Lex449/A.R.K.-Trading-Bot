# bot/auto/auto_signal.py
# Automatischer Signal-Loop, der regelmäßig Signale generiert und versendet

import asyncio
import datetime
from telegram import Bot
from bot.utils.analysis import analyze_symbol
from bot.config import config

bot = Bot(token=config.TELEGRAM_TOKEN)

async def send_auto_signal(symbol: str):
    """Führt die Analyse durch und sendet ein Signal (falls vorhanden) automatisch an den Bot-Channel."""
    try:
        analysis = analyze_symbol(symbol)
        if not analysis or not analysis.get("signal"):
            return  # Kein Signal vorhanden

        signal = analysis["signal"]
        emoji = "🚀" if signal == "LONG" else "🔻"
        text = (
            f"*A.R.K. Auto-Signal*\n"
            f"Symbol: `{symbol}`\n"
            f"Signal: *{signal}* {emoji}\n"
            f"RSI: `{round(analysis['rsi'], 2)}`\n"
            f"Trend: `{analysis['trend']}`\n"
            f"Muster: `{analysis['pattern']}`\n"
            f"Preis: `${round(analysis['price'], 2)}`\n"
            f"_Zeitpunkt: {datetime.datetime.now().strftime('%H:%M:%S')}_"
        )

        await bot.send_message(
            chat_id=config.TELEGRAM_CHAT_ID,
            text=text,
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"[AutoSignal-Fehler] {e}")

async def auto_signal_loop():
    """Wiederholt ausgeführter Loop, der alle Märkte regelmäßig analysiert und Signale versendet."""
    symbols = config.AUTO_SIGNAL_SYMBOLS
    interval = config.AUTO_SIGNAL_INTERVAL  # z. B. alle 60 Sekunden

    print(f"Auto-Signal-Loop gestartet ({interval}s Intervall)...")

    while True:
        for symbol in symbols:
            await send_auto_signal(symbol)
        await asyncio.sleep(interval)