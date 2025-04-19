import ccxt
import talib
import pandas as pd
import datetime

def analyse_market(symbol='BTC/USDT', timeframe='5m'):
    # Binance API verwenden (oder eine andere, die unterstützt wird)
    exchange = ccxt.binance()

    # Holen von OHLCV-Daten (Open, High, Low, Close, Volume)
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
    
    # Wandeln in ein DataFrame
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    # Berechnung des RSI (Relative Strength Index)
    df['rsi'] = talib.RSI(df['close'], timeperiod=14)

    # Berechnung des MACD (Moving Average Convergence Divergence)
    df['macd'], df['macdsignal'], df['macdhist'] = talib.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)

    # Beispiel für Trend-Analyse:
    if df['rsi'].iloc[-1] < 30:
        trend = "Buy"
    elif df['rsi'].iloc[-1] > 70:
        trend = "Sell"
    else:
        trend = "Hold"

    # Beispiel für Signal-Stärke basierend auf RSI und MACD
    confidence = 4  # Vertrauen (z. B. basierend auf RSI und MACD)
    
    # Erkennung des Candlestick-Musters
    pattern = "Bullish Engulfing"  # Beispiel für das erkannte Muster (müsste noch implementiert werden)
    
    # Zusätzliche Infos zur Analyse (RSI und MACD)
    extra_info = f"RSI: {df['rsi'].iloc[-1]}, MACD: {df['macd'].iloc[-1]}"

    # Aktuelles Datum und Uhrzeit
    now = datetime.datetime.utcnow()

    # Zurückgegebenes Ergebnis
    return {
        "timestamp": now.isoformat(),
        "trend": trend,
        "confidence": confidence,
        "pattern": pattern,
        "extra_info": extra_info
    }