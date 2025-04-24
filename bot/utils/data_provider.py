# bot/utils/data_provider.py

import os
import requests
import pandas as pd
import yfinance as yf
import time
from datetime import datetime
from bot.config.settings import get_settings

settings = get_settings()

FINNHUB_API_KEY = settings["FINNHUB_API_KEY"]
INTERVAL = settings["INTERVAL"]
USE_YFINANCE = settings.get("USE_YFINANCE", False)

# === Finnhub nutzt Unix-Zeitfenster, daher Umstellung auf von/bis ===
def fetch_finnhub_data(symbol: str):
    resolution = convert_interval(INTERVAL)
    now = int(time.time())
    past = now - (int(resolution) * 60 * 100)  # letzte 100 Kerzen

    url = "https://finnhub.io/api/v1/stock/candle"
    params = {
        "symbol": symbol,
        "resolution": resolution,
        "from": past,
        "to": now,
        "token": FINNHUB_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get("s") != "ok":
            print(f"[Finnhub] Fehler bei {symbol}: {data}")
            return None

        df = pd.DataFrame({
            "datetime": pd.to_datetime(data["t"], unit="s"),
            "open": data["o"],
            "high": data["h"],
            "low": data["l"],
            "close": data["c"]
        })
        return df

    except Exception as e:
        print(f"[Finnhub] API-Error für {symbol}: {e}")
        return None

# === Fallback via yfinance (nachts in UTC-Zeit) ===
def fetch_yfinance_data(symbol: str):
    try:
        df = yf.download(tickers=symbol, period="2d", interval=INTERVAL, progress=False)
        df.reset_index(inplace=True)
        df.rename(columns={"Open": "open", "High": "high", "Low": "low", "Close": "close", "Date": "datetime"}, inplace=True)
        df = df[["datetime", "open", "high", "low", "close"]]
        return df
    except Exception as e:
        print(f"[yfinance] Fehler bei {symbol}: {e}")
        return None

# === Uhrzeitbasierter Provider-Switch ===
def should_use_yfinance():
    hour = datetime.utcnow().hour
    return hour < 6 or hour > 20

# === Automatischer Dataprovider ===
def fetch_market_data(symbol: str):
    if USE_YFINANCE and should_use_yfinance():
        return fetch_yfinance_data(symbol)
    return fetch_finnhub_data(symbol)

# === Intervall-Mapping für Finnhub (nur für Minutenintervalle notwendig) ===
def convert_interval(interval_str: str) -> str:
    mapping = {
        "1": "1",
        "1m": "1",
        "5m": "5",
        "15m": "15",
        "30m": "30",
        "60m": "60",
        "1h": "60",
        "1d": "D"
    }
    return mapping.get(interval_str, "1")
