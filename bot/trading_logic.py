from bot.candles import candle_analysis
from bot.utils.data_fetcher import fetch_market_data
import time

def analyze_trades(symbol: str, interval: str, start_date: str, end_date: str):
    """
    Analysiert die Marktdaten und trifft Entscheidungen über Kauf oder Verkauf.
    """

    # Abrufen der historischen Marktdaten
    data = fetch_market_data(symbol, interval, start_date, end_date)
    
    # Durchführen der Candlestick-Analyse
    rsi, sma, engulfing = candle_analysis(data)

    # Berechnen der Signalrichtung basierend auf RSI, SMA und Mustern
    if rsi[-1] < 30 and engulfing[-1] != 0:  # Wenn RSI unter 30 und ein Engulfing-Muster da ist -> Long (Kaufen)
        action = "BUY"
    elif rsi[-1] > 70 and engulfing[-1] != 0:  # Wenn RSI über 70 und ein Engulfing-Muster da ist -> Short (Verkaufen)
        action = "SELL"
    else:
        action = "HOLD"

    print(f"Signal für {symbol}: {action}")

    return action


def execute_trade(symbol, action):
    """
    Simuliert die Ausführung eines Trades.
    (Kann später an ein tatsächliches Trading-System angebunden werden)
    """
    if action == "BUY":
        print(f"Kaufbefehl für {symbol}")
        # Hier könnte ein echter API-Aufruf zum Kauf von Aktien/Futures/Kryptos kommen
    elif action == "SELL":
        print(f"Verkaufsbefehl für {symbol}")
        # Hier könnte ein echter API-Aufruf zum Verkauf von Aktien/Futures/Kryptos kommen
    else:
        print(f"Kein Signal für {symbol}. Warten...")

# Beispiel für automatisierten Handel mit regelmäßigem Abrufen und Ausführen von Trades
def automated_trading(symbols=["US100/USDT", "US30/USDT", "SPX500/USDT"]):
    while True:
        for symbol in symbols:
            action = analyze_trades(symbol, "1h", "2022-01-01", "2023-01-01")
            execute_trade(symbol, action)
            time.sleep(300)  # Warten für 5 Minuten bis zum nächsten Trade
