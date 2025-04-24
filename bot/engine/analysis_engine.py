from bot.engine.data_provider import get_candles
from bot.utils.indicator import calculate_rsi, calculate_ema, detect_candlestick_pattern
from bot.config.settings import get_settings
import pandas as pd

settings = get_settings()

def analyze_market(symbol: str) -> dict | None:
    """
    Führt eine technische Analyse durch basierend auf:
    - EMA-Schnitt für Trendrichtung
    - RSI für Überkauft-/Überverkauft-Zonen
    - Candlestick Pattern-Erkennung
    """

    candles = get_candles(symbol)
    if not candles or len(candles) < 50:
        return None

    closes = [c["close"] for c in candles]

    # Indikatoren berechnen mit dynamischen Settings
    rsi = calculate_rsi(closes, settings["RSI_PERIOD"])[-1]
    ema_short = calculate_ema(closes, settings["EMA_SHORT_PERIOD"])[-1]
    ema_long = calculate_ema(closes, settings["EMA_LONG_PERIOD"])[-1]

    trend = "up" if ema_short > ema_long else "down"
    confidence = abs(ema_short - ema_long) / ema_long * 100

    # Candlestick-Pattern-Erkennung
    df = pd.DataFrame(candles)
    pattern = detect_candlestick_pattern(df)

    return {
        "trend": trend,
        "confidence": round(confidence, 2),
        "rsi": round(rsi, 2),
        "pattern": pattern
    }
