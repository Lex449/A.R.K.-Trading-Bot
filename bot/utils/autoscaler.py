import os
from telegram import Bot

# Die Standard-Symbole für den Auto-Scaler mit den richtigen TwelveData-Symbolen
DEFAULT_SYMBOLS = [
    "SPX",  # SPX500 → SPX
    "DJI",  # DIA → DJI
    "IXIC", # QQQ → IXIC
    "MDY",  # MDY bleibt MDY
    "VTI",  # VTI bleibt VTI
    "VOO",  # VOO bleibt VOO
    "SPY",  # SPY bleibt SPY
    "XLF",  # XLF bleibt XLF
    "XLK",  # XLK bleibt XLK
    "XLE",  # XLE bleibt XLE
    "AAPL", # AAPL bleibt AAPL
    "MSFT", # MSFT bleibt MSFT
    "TSLA", # TSLA bleibt TSLA
    "NVDA", # NVDA bleibt NVDA
    "META", # META bleibt META
    "AMZN", # AMZN bleibt AMZN
    "GOOGL",# GOOGL bleibt GOOGL
    "BRK.B",# BRK.B bleibt BRK.B
    "UNH",  # UNH bleibt UNH
    "JPM"   # JPM bleibt JPM
]

# Die Fallback-Symbole für zusätzliche Skalierung
FALLBACK_SYMBOLS = [
    "AAPL", "MSFT", "TSLA", "NVDA", "META",
    "AMZN", "GOOGL", "BRK.B", "UNH", "JPM"
]

def get_scaled_symbols(current_count: int, max_count: int = 150) -> tuple:
    """
    Berechnet und gibt eine Liste von Symbolen zurück, basierend auf der aktuellen Anzahl
    von Symbolen und der maximalen Anzahl, ergänzt mit Fallback-Symbolen, falls notwendig.
    """
    # Berechne die idealen Symbole basierend auf der maximalen Anzahl
    ideal_count = max_count // 12  # Optimierung basierend auf der maximalen Anzahl von 12 Symbolen
    additional_needed = max(ideal_count - current_count, 0)  # Berechnet, wie viele Symbole hinzugefügt werden müssen

    # Starte mit den Standard-Symbolen
    final = DEFAULT_SYMBOLS.copy()
    added = []

    for sym in FALLBACK_SYMBOLS:
        # Wenn noch zusätzliche Symbole benötigt werden
        if additional_needed <= 0:
            break
        if sym not in final:
            final.append(sym)  # Füge das Fallback-Symbol hinzu
            added.append(sym)  # Liste der hinzugefügten Symbole
            additional_needed -= 1  # Verringere die Anzahl der benötigten Symbole

    return final, added  # Gibt die finale Liste der Symbole und die neu hinzugefügten zurück

async def run_autoscaler(bot: Bot, chat_id: int):
    """
    Führt die Auto-Skalierung aus, überprüft, ob weitere Symbole ergänzt werden müssen
    und sendet ein Update an den Telegram-Chat.
    """
    # Hole die aktuell in der .env definierten Symbole
    env_symbols = os.getenv("AUTO_SIGNAL_SYMBOLS", "")
    current = [s.strip() for s in env_symbols.split(",") if s.strip()]  # Entferne Leerzeichen und leere Einträge
    
    # Berechne die Skalierung basierend auf der aktuellen Anzahl von Symbolen
    scaled, new_added = get_scaled_symbols(len(current))  # Hol die neuen Symbole und die zu ergänzende Liste

    # Aktualisiere die Umgebungsvariablen (für die lokale Nutzung)
    os.environ["AUTO_SIGNAL_SYMBOLS"] = ",".join(scaled)

    # Wenn neue Symbole hinzugefügt wurden, sende eine Nachricht
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
    Berechnet und gibt zurück, wie viele Signale pro Symbol pro Stunde erlaubt sind,
    basierend auf der maximalen Anzahl von Signalen.
    """
    count = len(symbols)
    return max(1, max_total // count)  # Berechnet das Maximum der erlaubten Signale pro Stunde
