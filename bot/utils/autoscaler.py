# bot/utils/autoscaler.py

import os
from telegram import Bot

DEFAULT_SYMBOLS = [
    "US100", "US30", "SPX500", "IWM", "QQQ", "DIA", "MDY",
    "VTI", "VOO", "SPY", "XLF", "XLK", "XLE"
]

FALLBACK_SYMBOLS = [
    "AAPL", "MSFT", "TSLA", "NVDA", "META",
    "AMZN", "GOOGL", "BRK.B", "UNH", "JPM"
]

def get_scaled_symbols(current_count: int, max_count: int = 150) -> tuple:
    # Berechnet die finale Liste an Symbolen, ergänzt wenn nötig aus FALLBACK_SYMBOLS.
    needed = max_count // 12 - current_count  # max 12 Signale pro Symbol/Stunde
    final = DEFAULT_SYMBOLS.copy()

    added = []
    for sym in FALLBACK_SYMBOLS:
        if needed <= 0:
            break
        if sym not in final:
            final.append(sym)
            added.append(sym)
            needed -= 1
    return final, added

async def run_autoscaler(bot: Bot, chat_id: int):
    # Führt den Autoscaler aus und sendet eine Nachricht bei Erweiterung.
    env_symbols = os.getenv("AUTO_SIGNAL_SYMBOLS", "")
    current = [s.strip() for s in env_symbols.split(",") if s.strip()]
    scaled, new_added = get_scaled_symbols(len(current))

    if new_added:
        os.environ["AUTO_SIGNAL_SYMBOLS"] = ",".join(scaled)
        added_str = ", ".join(new_added)
        msg = f"🚀 A.R.K. Auto-Scaler aktiviert!\nNeue Symbole ergänzt: {added_str}"
        await bot.send_message(chat_id=chat_id, text=msg)
    else:
        await bot.send_message(chat_id=chat_id, text="✔️ A.R.K. Auto-Scaler: Alle Symbole bereits optimal.")
