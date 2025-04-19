import talib
import pandas as pd

# Angenommene Candlestick-Daten (öffnen, hoch, niedrig, schließen)
def candle_analysis(df):
    # RSI (Relative Strength Index)
    rsi = talib.RSI(df['close'], timeperiod=14)
    
    # Moving Average (SMA)
    sma = talib.SMA(df['close'], timeperiod=30)
    
    # Engulfing Pattern erkennen
    engulfing = talib.CDLENGULFING(df['open'], df['high'], df['low'], df['close'])

    return rsi, sma, engulfing