# bot/utils/data_provider.py

import os
import requests
import yfinance as yf
from datetime import datetime

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

def is_market_open_hour():
    """Entscheidet, ob Finnhub (US-Zeit) oder yfinance (Off-Zeit) genutzt wird."""
    now_utc = datetime.utcnow()
    hour = now_utc.hour
    return 13 <= hour <= 22  # Finnhub-Zeitraum (ca. 21:00–08:00 Bali-Zeit)

def fetch_data(symbol: str, interval: str = "1h", limit: int = 100):
    """Lädt Marktdaten von Finnhub oder yfinance je nach Uhrzeit."""

    if is_market_open_hour():
        return fetch_from_finnhub(symbol, interval, limit)
    else:
        return fetch_from_yfinance(symbol, interval, limit)

def fetch_from_finnhub(symbol: str, interval: str, limit: int):
    url = f"https://finnhub.io/api/v1/stock/candle"
    resolution = interval_to_finnhub(interval)

    params = {
        "symbol": symbol,
        "resolution": resolution,
        "count": limit,
        "token": FINNHUB_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get("s") != "ok":
            raise ValueError(f"Finnhub Error: {data.get('s')}")

        candles = []
        for i in range(len(data["t"])):
            candles.append({
                "datetime": datetime.utcfromtimestamp(data["t"][i]),
                "open": data["o"][i],
                "high": data["h"][i],
                "low": data["l"][i],
                "close": data["c"][i]
            })

        return candles

    except Exception as e:
        print(f"[ERROR] Finnhub fetch failed for {symbol}: {e}")
        return None

def fetch_from_yfinance(symbol: str, interval: str, limit: int):
    yf_interval = interval if interval in ["1m", "5m", "15m", "1h", "1d"] else "1h"
    try:
        df = yf.download(tickers=symbol, interval=yf_interval, period="7d")
        if df.empty:
            return None

        candles = []
        df = df.tail(limit)
        for index, row in df.iterrows():
            candles.append({
                "datetime": index.to_pydatetime(),
                "open": row["Open"],
                "high": row["High"],
                "low": row["Low"],
                "close": row["Close"]
            })

        return candles

    except Exception as e:
        print(f"[ERROR] yfinance fetch failed for {symbol}: {e}")
        return None

def interval_to_finnhub(interval: str):
    mapping = {
        "1m": "1",
        "5m": "5",
        "15m": "15",
        "30m": "30",
        "1h": "60",
        "4h": "240",
        "1d": "D"
    }
    return mapping.get(interval, "60")
