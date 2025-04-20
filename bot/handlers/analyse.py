import ccxt
import pandas as pd
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator

def fetch_ohlcv(symbol: str, timeframe='5m', limit=100):
    exchange = ccxt.binance()
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        return df
    except Exception as e:
        print(f"Fehler beim Abrufen der Daten: {e}")
        return None

def analyse_market(symbol: str):
    df = fetch_ohlcv(symbol)
    if df is None or df.empty:
        return None

    # Berechne EMA20 und RSI14
    df['ema'] = EMAIndicator(close=df['close'], window=20).ema_indicator()
    df['rsi'] = RSIIndicator(close=df['close'], window=14).rsi()

    # Aktuelle Werte
    last_close = df['close'].iloc[-1]
    last_ema = df['ema'].iloc[-1]
    last_rsi = df['rsi'].iloc[-1]

    # Signal-Logik
    if last_rsi < 30 and last_close > last_ema:
        trend = "Long-Signal erkannt"
        stars = 5
    elif last_rsi > 70 and last_close < last_ema:
        trend = "Short-Signal erkannt"
        stars = 5
    else:
        trend = "Kein klares Signal"
        stars = 2

    return {
        "trend": trend,
        "pattern": f"RSI: {round(last_rsi, 1)} | EMA: {round(last_ema, 2)} | Close: {round(last_close, 2)}",
        "confidence": stars
    }