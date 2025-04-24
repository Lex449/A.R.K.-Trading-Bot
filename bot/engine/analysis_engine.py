# bot/engine/analysis_engine.py

from bot.engine.data_provider import get_candles
from bot.utils.indicator import calculate_rsi, calculate_ema, detect_candlestick_pattern

def analyze_market(symbol: str) -> dict | None:
    """
    Führt eine technische Analyse durch und liefert:
    - Trendrichtung basierend auf EMA-Schnitt
    - RSI zur Einschätzung von Überkauft-/Überverkauft-Zonen
    - Erkanntes Candlestick-Muster

    Returns:
        dict mit Analyseergebnis oder None bei Fehlern
    """
    candles = get_candles(symbol)
    if not candles or len(candles) < 50:
        return None

    closes = [c["close"] for c in candles]

    # Indikatoren berechnen
    rsi = calculate_rsi(closes)[-1]
    ema_short = calculate_ema(closes, 20)[-1]
    ema_long = calculate_ema(closes, 50)[-1]

    trend = "up" if ema_short > ema_long else "down"
    confidence = abs(ema_short - ema_long) / ema_long * 100

    # Pattern erkennen
    import pandas as pd
    df = pd.DataFrame(candles)
    pattern = detect_candlestick_pattern(df)

    return {
        "trend": trend,
        "confidence": round(confidence, 2),
        "rsi": round(rsi, 2),
        "pattern": pattern
    }
