# bot/engine/analysis_engine.py

import pandas as pd
from bot.engine.data_provider import get_candles
from bot.utils.indicator import calculate_rsi, calculate_ema, detect_candlestick_pattern
from bot.config.settings import get_settings

settings = get_settings()

def analyze_market(symbol: str) -> dict | None:
    """
    Führt eine präzise technische Analyse auf Bugatti-Niveau durch:
    - EMA-Trendrichtung (short > long → bullisch)
    - RSI-Wert (überkauft/überverkauft)
    - Candlestick-Pattern-Erkennung (optional)
    """

    candles = get_candles(symbol)
    if not candles or len(candles) < 50:
        return None

    closes = [c["close"] for c in candles]

    # Dynamische Indikatorberechnung
    rsi = calculate_rsi(closes, settings["RSI_PERIOD"])[-1]
    ema_short = calculate_ema(closes, settings["EMA_SHORT_PERIOD"])[-1]
    ema_long = calculate_ema(closes, settings["EMA_LONG_PERIOD"])[-1]

    trend = "up" if ema_short > ema_long else "down"
    confidence = round(abs(ema_short - ema_long) / ema_long * 100, 2)

    # Pattern Detection
    df = pd.DataFrame(candles)
    pattern = detect_candlestick_pattern(df)

    return {
        "trend": trend,
        "confidence": confidence,
        "rsi": round(rsi, 2),
        "pattern": pattern
    }
