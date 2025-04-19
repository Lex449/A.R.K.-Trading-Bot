from bot.candles import detect_candlestick_patterns
from bot.utils.data_fetcher import fetch_market_data

def execute_trade(signal: str):
    print(f"Trade signal: {signal}")
    # Füge hier deine Handelslogik hinzu, z.B. API-Aufrufe zum Platzieren von Trades

def analyze_trades(symbol: str, interval: str, start_date: str, end_date: str):
    df = fetch_market_data(symbol, interval, start_date, end_date)

    patterns = detect_candlestick_patterns(df)

    # Überprüfe, ob ein Bullish oder Bearish Engulfing Muster erkannt wurde
    if patterns['Bullish Engulfing'][-1] > 0:
        execute_trade('LONG')
    elif patterns['Bearish Engulfing'][-1] < 0:
        execute_trade('SHORT')
    else:
        print("Kein Handelssignal")