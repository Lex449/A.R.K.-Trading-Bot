# bot/engine/data_provider.py

import os
import yfinance as yf
import time
from datetime import datetime
from bot.engine.finnhub_client import get_finnhub_client
from bot.engine.symbol_map import map_symbol

INTERVAL = os.getenv("INTERVAL", "1")  # Minutenintervall für Candles
FINNHUB_ENABLED_HOURS = range(7, 23)  # UTC-Zeitraum, in dem Finnhub aktiviert ist
CANDLE_LIMIT = 100  # Anzahl der abgefragten Kerzen

def is_fallback_time():
    return datetime.utcnow().hour not in FINNHUB_ENABLED_HOURS

def get_candles(symbol: str, interval: str = INTERVAL, limit: int = CANDLE_LIMIT):
    if is_fallback_time():
        return get_candles_yfinance(symbol, interval, limit)
    return get_candles_finnhub(symbol, interval, limit)

def get_candles_finnhub(symbol: str, interval: str = INTERVAL, limit: int = CANDLE_LIMIT):
    mapped = map_symbol(symbol)
    client = get_finnhub_client()

    to_time = int(time.time())
    from_time = to_time - (limit * 60 * int(interval))  # Intervall in Sekunden

    try:
        response = client.stock_candles(
            symbol=mapped,
            resolution=interval,
            _from=from_time,
            to=to_time
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
        print(f"[ERROR] Finnhub API failed for {symbol}: {e}")
        return []

def get_candles_yfinance(symbol: str, interval: str = INTERVAL, limit: int = CANDLE_LIMIT):
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
