# bot/utils/data_provider.py

import os
import requests
import yfinance as yf
from datetime import datetime
from bot.engine.symbol_map import map_symbol

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

def is_market_open_hour():
    """Entscheidet, ob Finnhub (US-Zeit) oder yfinance (Off-Zeit) genutzt wird."""
    now_utc = datetime.utcnow().hour
    return 13 <= now_utc <= 22  # Finnhub-Zeitraum (ca. 21:00–08:00 Bali-Zeit)

def fetch_data(symbol: str, interval: str = "1m", limit: int = 100):
    """Lädt Marktdaten je nach Marktzeit – bevorzugt Finnhub, fallback yfinance."""
    if is_market_open_hour():
        return fetch_from_finnhub(symbol, interval, limit)
    return fetch_from_yfinance(symbol, interval, limit)

def fetch_from_finnhub(symbol: str, interval: str, limit: int):
    mapped = map_symbol(symbol)
    resolution = interval_to_finnhub(interval)
    url = "https://finnhub.io/api/v1/stock/candle"
    
    to_time = int(datetime.utcnow().timestamp())
    from_time = to_time - (limit * 60 * int(resolution))

    params = {
        "symbol": mapped,
        "resolution": resolution,
        "from": from_time,
        "to": to_time,
        "token": FINNHUB_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get("s") != "ok":
            raise ValueError(f"Finnhub Error: {data.get('s')}")

        return [
            {
                "datetime": datetime.utcfromtimestamp(data["t"][i]),
                "open": data["o"][i],
                "high": data["h"][i],
                "low": data["l"][i],
                "close": data["c"][i]
            }
            for i in range(len(data["t"]))
        ]
    except Exception as e:
        print(f"[ERROR] Finnhub fetch failed for {symbol}: {e}")
        return None

def fetch_from_yfinance(symbol: str, interval: str, limit: int):
    mapped = map_symbol(symbol, fallback=True)
    yf_interval = interval if interval in ["1m", "5m", "15m", "1h", "1d"] else "1m"

    try:
        df = yf.download(tickers=mapped, interval=yf_interval, period="7d", progress=False)
        if df.empty:
            return None

        df = df.tail(limit)
        return [
            {
                "datetime": index.to_pydatetime(),
                "open": row["Open"],
                "high": row["High"],
                "low": row["Low"],
                "close": row["Close"]
            }
            for index, row in df.iterrows()
        ]
    except Exception as e:
        print(f"[ERROR] yfinance fetch failed for {symbol}: {e}")
        return None

def interval_to_finnhub(interval: str):
    return {
        "1m": "1",
        "5m": "5",
        "15m": "15",
        "30m": "30",
        "1h": "60",
        "4h": "240",
        "1d": "D"
    }.get(interval, "1")
