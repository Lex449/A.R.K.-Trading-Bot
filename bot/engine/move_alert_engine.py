"""
Move Alert Engine – Ultra Realtime Bewegungsanalyse
Überwacht starke Marktbewegungen in 1-Minuten-Intervallen.
"""

import pandas as pd

async def detect_move_alert(df: pd.DataFrame) -> dict:
    """
    Analysiert die letzten Candles auf plötzliche Bewegungen.

    Args:
        df (pd.DataFrame): Candle-Daten (muss Spalten 'o', 'h', 'l', 'c' enthalten).

    Returns:
        dict: Move-Alert Informationen oder None, wenn keine starke Bewegung.
    """
    if df.empty or len(df) < 2:
        return None

    try:
        last_close = df.iloc[-1]["c"]
        prev_close = df.iloc[-2]["c"]

        move_percent = ((last_close - prev_close) / prev_close) * 100

        if abs(move_percent) >= 2.5:
            # Starker Move → Voller Alarm
            return {
                "type": "full",
                "move_percent": move_percent,
            }
        elif abs(move_percent) >= 2.0:
            # Frühwarnung
            return {
                "type": "warning",
                "move_percent": move_percent,
            }
        else:
            return None

    except Exception as e:
        return None
