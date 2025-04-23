import talib
import pandas as pd

def candle_analysis(df):
    """
    Führt eine technische Analyse der Candlestick-Daten durch.
    """

    # Berechnung des Relative Strength Index (RSI)
    rsi = talib.RSI(df['close'], timeperiod=14)

    # Berechnung des einfachen gleitenden Durchschnitts (SMA)
    sma = talib.SMA(df['close'], timeperiod=30)

    # Erkennen von Candlestick-Mustern
    engulfing = talib.CDLENGULFING(df['open'], df['high'], df['low'], df['close'])  # Engulfing-Muster
    hammer = talib.CDLHAMMER(df['open'], df['high'], df['low'], df['close'])  # Hammer-Muster
    doji = talib.CDLDOJI(df['open'], df['high'], df['low'], df['close'])  # Doji-Muster

    # Das letzte Element in den Arrays enthält das neueste Muster.
    last = df.iloc[-1]

    # Entscheidung: Long/Short basierend auf RSI, SMA und Mustern
    trend = "Neutral"
    if rsi[-1] < 30 and engulfing[-1] != 0:  # Kaufsignal
        trend = "Long"
    elif rsi[-1] > 70 and engulfing[-1] != 0:  # Verkaufssignal
        trend = "Short"
    
    # Musterentscheidung
    pattern = "Neutral"
    if hammer[-1] != 0:
        pattern = "Hammer"
    elif doji[-1] != 0:
        pattern = "Doji"
    elif engulfing[-1] != 0:
        pattern = "Engulfing"

    # Vertrauen (Confidence) - höher, wenn RSI im neutralen Bereich ist und das Muster stark ist
    confidence = 4 if 30 < rsi[-1] < 70 else 2

    return {"trend": trend, "pattern": pattern, "confidence": confidence}
