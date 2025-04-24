# bot/engine/data_provider.py

import yfinance as yf
import finnhub
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)

def is_finnhub_time():
    now = datetime.utcnow().hour
    return 13 <= now <= 21  # Hauptzeiten (ca. 21:00 - 05:00 Bali-Zeit)

def get_candles(symbol: str, interval: str = "5", limit: int = 100):
    """
    Holt Candlestick-Daten über Finnhub oder Yahoo Finance (Fallback)
    """
    if is_finnhub_time():
        try:
            now = int(datetime.utcnow().timestamp())
            before = int((datetime.utcnow() - timedelta(minutes=int(limit)*int(interval))).timestamp())
            resolution = interval  # z. B. "5" = 5 Minuten

            res = finnhub_client.stock_candles(symbol, resolution, before, now)
            if res.get("s") != "ok":
                raise ValueError("Finnhub liefert ungültige Daten.")

            candles = []
            for i in range(len(res["t"])):
                candles.append({
                    "open": res["o"][i],
                    "high": res["h"][i],
                    "low": res["l"][i],
                    "close": res["c"][i],
                    "volume": res["v"][i]
                })
            return candles

        except Exception as e:
            print(f"[WARNUNG] Finnhub fehlgeschlagen für {symbol}: {e}")

    # Fallback zu yfinance
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period="7d", interval=f"{interval}m", actions=False)
        candles = df.tail(limit)[["Open", "High", "Low", "Close"]].rename(
            columns={"Open": "open", "High": "high", "Low": "low", "Close": "close"}
        ).to_dict(orient="records")
        return candles

    except Exception as e:
        print(f"[FEHLER] Datenabruf für {symbol} fehlgeschlagen: {e}")
        return None
