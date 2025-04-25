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
    """
    Gibt eine Liste an Symbolen zurück, ergänzt mit Fallbacks falls nötig.
    """
    ideal_count = max_count // 12
    additional_needed = max(ideal_count - current_count, 0)

    final = DEFAULT_SYMBOLS.copy()
    added = []

    for sym in FALLBACK_SYMBOLS:
        if additional_needed <= 0:
            break
        if sym not in final:
            final.append(sym)
            added.append(sym)
            additional_needed -= 1

    return final, added

async def run_autoscaler(bot: Bot, chat_id: int):
    """
    Prüft, ob weitere Symbole ergänzt werden sollten und sendet Update.
    """
    env_symbols = os.getenv("AUTO_SIGNAL_SYMBOLS", "")
    current = [s.strip() for s in env_symbols.split(",") if s.strip()]
    scaled, new_added = get_scaled_symbols(len(current))

    # ENV live updaten (für lokale Nutzung)
    os.environ["AUTO_SIGNAL_SYMBOLS"] = ",".join(scaled)

    if new_added:
        added_str = ", ".join(new_added)
        msg = (
            f"🚀 *Auto-Scaler aktiviert*\n"
            f"Neue Symbole hinzugefügt:\n`{added_str}`\n\n"
            f"_Dein Bot ist jetzt besser vorbereitet._"
        )
        await bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
    else:
        await bot.send_message(
            chat_id=chat_id,
            text="✅ *Auto-Scaler Check abgeschlossen:*\nAlle Symbole optimal.",
            parse_mode="Markdown"
        )

def get_scaled_limit(symbols: list, max_total: int = 150) -> int:
    """
    Gibt zurück, wie viele Signale pro Symbol pro Stunde erlaubt sind.
    """
    count = len(symbols)
    return max(1, max_total // count)
