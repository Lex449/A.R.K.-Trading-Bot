# bot/engine/data_provider.py

import os
import yfinance as yf
import finnhub
from datetime import datetime
from bot.engine.symbol_map import map_symbol

# Finnhub API-Key laden und Client initialisieren
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)

def is_fallback_time():
    """
    True, wenn außerhalb der Hauptbörsenzeiten → yfinance fallback.
    """
    now = datetime.utcnow().hour
    return now < 7 or now > 22

def get_candles(symbol: str, interval: str = "5", limit: int = 100):
    """
    Automatischer Switch zwischen Finnhub und yfinance basierend auf Uhrzeit.
    """
    if is_fallback_time():
        return get_candles_yfinance(symbol, interval, limit)
    return get_candles_finnhub(symbol, interval, limit)

def get_candles_finnhub(symbol: str, interval: str = "5", limit: int = 100):
    """
    Holt Marktdaten direkt über offiziellen Finnhub-Client.
    """
    mapped = map_symbol(symbol)
    try:
        candles = finnhub_client.stock_candles(symbol=mapped, resolution=interval, count=limit)

        print(f"[DEBUG] Finnhub Client for {symbol}: Status = {candles.get('s')}")

        if candles.get("s") != "ok":
            raise Exception(f"Finnhub returned status {candles.get('s')}")

        return [{
            "timestamp": candles["t"][i],
            "open": candles["o"][i],
            "high": candles["h"][i],
            "low": candles["l"][i],
            "close": candles["c"][i]
        } for i in range(len(candles["t"]))]

    except Exception as e:
        print(f"[ERROR] Finnhub Client failed for {symbol}: {e}")
        return []

def get_candles_yfinance(symbol: str, interval: str = "5", limit: int = 100):
    """
    Holt Fallback-Daten über Yahoo Finance.
    """
    yf_symbol = map_symbol(symbol, fallback=True)
    try:
        df = yf.download(tickers=yf_symbol, period="5d", interval=f"{interval}m", progress=False)
        df = df.tail(limit)

        return [{
            "timestamp": int(index.timestamp()),
            "open": row["Open"],
            "high": row["High"],
            "low": row["Low"],
            "close": row["Close"]
        } for index, row in df.iterrows()]

    except Exception as e:
        print(f"[ERROR] yfinance fallback failed for {symbol}: {e}")
        return []
