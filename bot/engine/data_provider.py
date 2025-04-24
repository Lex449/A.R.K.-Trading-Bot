# bot/engine/data_provider.py

import yfinance as yf
from datetime import datetime
from bot.engine.finnhub_client import finnhub_client
from bot.engine.symbol_map import map_symbol

def is_fallback_time():
    now = datetime.utcnow().hour
    return now < 7 or now > 22  # Fallback außerhalb der Hauptbörsenzeiten

def get_candles(symbol: str, interval: str = "5", limit: int = 100):
    if is_fallback_time():
        return get_candles_yfinance(symbol, interval, limit)
    return get_candles_finnhub(symbol, interval, limit)

def get_candles_finnhub(symbol: str, interval: str = "5", limit: int = 100):
    mapped = map_symbol(symbol)

    try:
        response = finnhub_client.stock_candles(
            symbol=mapped,
            resolution=interval,
            count=limit
        )

        print(f"[DEBUG] Finnhub response for {symbol}: {response}")

        if response.get("s") != "ok":
            raise Exception(f"Finnhub returned status {response.get('s')}")

        return [{
            "timestamp": response["t"][i],
            "open": response["o"][i],
            "high": response["h"][i],
            "low": response["l"][i],
            "close": response["c"][i]
        } for i in range(len(response["t"]))]

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
