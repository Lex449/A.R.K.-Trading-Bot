# bot/engine/data_provider.py

import os
import requests
import yfinance as yf
from datetime import datetime
from bot.engine.symbol_map import map_symbol

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

def is_fallback_time():
    now = datetime.utcnow().hour
    return now < 7 or now > 22  # Fallback: außerhalb der Kernbörsenzeiten

def get_candles(symbol: str, interval: str = "5", limit: int = 100):
    """
    Entscheidet automatisch zwischen Finnhub und yfinance basierend auf Uhrzeit.
    """
    if is_fallback_time():
        return get_candles_yfinance(symbol, interval, limit)
    return get_candles_finnhub(symbol, interval, limit)

def get_candles_finnhub(symbol: str, interval: str = "5", limit: int = 100):
    mapped = map_symbol(symbol)
    url = "https://finnhub.io/api/v1/stock/candle"
    params = {
        "symbol": mapped,
        "resolution": interval,
        "count": limit,
        "token": FINNHUB_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"[DEBUG] Finnhub Request for {symbol} returned {response.status_code}: {response.text}")
        data = response.json()

        if data.get("s") != "ok":
            raise Exception(f"Finnhub returned status {data.get('s')}")

        return [{
            "timestamp": data["t"][i],
            "open": data["o"][i],
            "high": data["h"][i],
            "low": data["l"][i],
            "close": data["c"][i]
        } for i in range(len(data["t"]))]

    except Exception as e:
        print(f"[ERROR] Finnhub API failed: {e}")
        return []

def get_candles_yfinance(symbol: str, interval: str = "5", limit: int = 100):
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
        print(f"[ERROR] yfinance fallback failed: {e}")
        return []
