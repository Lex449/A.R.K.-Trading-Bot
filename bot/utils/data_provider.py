# bot/utils/data_provider.py

import os
import requests
import pandas as pd
import yfinance as yf
from datetime import datetime
from bot.config.settings import get_settings

settings = get_settings()

FINNHUB_API_KEY = settings["FINNHUB_API_KEY"]
USE_YFINANCE = settings["USE_YFINANCE"]
INTERVAL = settings["INTERVAL"]

# === Uhrzeitbasierter Switch (Finnhub tagsüber, yfinance nachts) ===
def should_use_yfinance():
    now = datetime.utcnow().hour
    return now < 6 or now > 20  # Off-Times = vor 6 Uhr und nach 20 Uhr UTC

# === Finnhub Abruf ===
def fetch_finnhub_data(symbol: str):
    url = f"https://finnhub.io/api/v1/stock/candle"
    params = {
        "symbol": symbol,
        "resolution": convert_interval(INTERVAL),
        "count": 100,
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

# === yfinance Abruf ===
def fetch_yfinance_data(symbol: str):
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period="2d", interval=INTERVAL)
        df = df.reset_index()
        df.rename(columns={"Open": "open", "High": "high", "Low": "low", "Close": "close", "Date": "datetime"}, inplace=True)
        df = df[["datetime", "open", "high", "low", "close"]]
        return df
    except Exception as e:
        print(f"[yfinance] Fehler bei {symbol}: {e}")
        return None

# === Automatischer Provider-Wechsel ===
def fetch_market_data(symbol: str):
    if USE_YFINANCE and should_use_yfinance():
        return fetch_yfinance_data(symbol)
    else:
        return fetch_finnhub_data(symbol)

# === Zeitintervall-Mapping für Finnhub ===
def convert_interval(interval_str: str) -> str:
    mapping = {
        "1min": "1",
        "5min": "5",
        "15min": "15",
        "30min": "30",
        "60min": "60",
        "1h": "60",
        "1d": "D"
    }
    return mapping.get(interval_str, "5")
