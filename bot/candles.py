import talib
import pandas as pd

def detect_candlestick_patterns(df: pd.DataFrame):
    # OHLC Daten aus DataFrame extrahieren
    open = df['open'].values
    high = df['high'].values
    low = df['low'].values
    close = df['close'].values

    # Candlestick-Muster erkennen
    patterns = {
        'Bullish Engulfing': talib.CDLENGULFING(open, high, low, close),
        'Bearish Engulfing': talib.CDLENGULFING(open, high, low, close),
        'Doji': talib.CDLDOJI(open, high, low, close),
        # Weitere Muster hinzufügen (z. B. Hammer, Shooting Star, etc.)
    }

    return patterns