import talib
import pandas as pd

def candle_analysis(df):
    """
    Führt eine technische Analyse der Candlestick-Daten durch.
    Erkennt RSI, EMA-Trendrichtung, Candlestick-Muster und berechnet eine Confidence-Score.
    """

    # RSI-Berechnung
    rsi = talib.RSI(df['close'], timeperiod=14)

    # EMA-Berechnung für Trendrichtung (Short = bearish, Long = bullish)
    ema_short = talib.EMA(df['close'], timeperiod=9)
    ema_long = talib.EMA(df['close'], timeperiod=21)

    # Candlestick Pattern Erkennung
    engulfing = talib.CDLENGULFING(df['open'], df['high'], df['low'], df['close'])
    hammer = talib.CDLHAMMER(df['open'], df['high'], df['low'], df['close'])
    doji = talib.CDLDOJI(df['open'], df['high'], df['low'], df['close'])

    # Letzter Wert jeder Analyse
    last_rsi = rsi.iloc[-1]
    last_ema_short = ema_short.iloc[-1]
    last_ema_long = ema_long.iloc[-1]
    last_engulfing = engulfing.iloc[-1]
    last_hammer = hammer.iloc[-1]
    last_doji = doji.iloc[-1]

    # Trendbestimmung
    trend = "Neutral"
    if last_rsi < 30 and last_ema_short > last_ema_long and last_engulfing != 0:
        trend = "Long"
    elif last_rsi > 70 and last_ema_short < last_ema_long and last_engulfing != 0:
        trend = "Short"

    # Muster-Label
    pattern = "Neutral"
    if last_hammer != 0:
        pattern = "Hammer"
    elif last_doji != 0:
        pattern = "Doji"
    elif last_engulfing != 0:
        pattern = "Engulfing"

    # Confidence-Skala von 1–5
    confidence = 1
    if pattern != "Neutral":
        confidence += 1
    if trend != "Neutral":
        confidence += 1
    if 45 < last_rsi < 55:
        confidence += 1
    if abs(last_ema_short - last_ema_long) > 0.1:
        confidence += 1

    return {
        "trend": trend,
        "pattern": pattern,
        "confidence": min(confidence, 5)
    }
