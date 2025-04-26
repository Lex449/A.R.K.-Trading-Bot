import os
import requests
import pandas as pd
import numpy as np
from bot.engine.pattern_detector import detect_candle_patterns

FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')
FINNHUB_BASE_URL = "https://finnhub.io/api/v1"

async def analyze_symbol(symbol: str) -> dict:
    """
    Ultra Analysis Engine für Trading-Signale auf Basis von Realtime-Daten.
    Kombination aus RSI, Trendanalyse und Candle Pattern Detection.
    """

    try:
        # Quote-Daten abrufen
        quote_url = f"{FINNHUB_BASE_URL}/quote"
        params = {"symbol": symbol, "token": FINNHUB_API_KEY}
        quote_resp = requests.get(quote_url, params=params).json()

        # Candle-Daten abrufen
        candles_url = f"{FINNHUB_BASE_URL}/stock/candle"
        params = {
            "symbol": symbol,
            "resolution": "1",
            "count": 30,
            "token": FINNHUB_API_KEY
        }
        candles_resp = requests.get(candles_url, params=params).json()

        if candles_resp.get("s") != "ok":
            return None

        # DataFrame bauen
        df = pd.DataFrame({
            "t": candles_resp["t"],
            "o": candles_resp["o"],
            "h": candles_resp["h"],
            "l": candles_resp["l"],
            "c": candles_resp["c"],
            "v": candles_resp["v"]
        })

        # RSI Berechnung
        delta = df["c"].diff()
        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)
        avg_gain = pd.Series(gain).rolling(window=14).mean()
        avg_loss = pd.Series(loss).rolling(window=14).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        latest_rsi = rsi.iloc[-1]

        # Trend-Erkennung
        short_trend = "Uptrend" if df["c"].iloc[-5:].is_monotonic_increasing else "Downtrend" if df["c"].iloc[-5:].is_monotonic_decreasing else "Sideways"
        mid_trend = "Uptrend" if df["c"].iloc[-15:].is_monotonic_increasing else "Downtrend" if df["c"].iloc[-15:].is_monotonic_decreasing else "Sideways"

        # Candle Pattern Detection
        detected_pattern = detect_candle_patterns(df)

        # Signal Generierung
        signal = "Hold"
        if short_trend == "Uptrend" and latest_rsi < 70:
            signal = "Buy"
        elif short_trend == "Downtrend" and latest_rsi > 30:
            signal = "Sell"

        # Sterne-Rating
        stars = 3
        if signal in ["Buy", "Sell"] and ("Engulfing" in detected_pattern):
            stars = 5
        elif signal in ["Buy", "Sell"] and (detected_pattern in ["Hammer", "Shooting Star"]):
            stars = 4
        elif signal == "Hold":
            stars = 2
        else:
            stars = 1

        # Halteempfehlung
        holding_period = "Short-Term" if short_trend == mid_trend else "Mid-Term"

        return {
            "signal": signal,
            "rsi": round(latest_rsi, 2),
            "short_term_trend": short_trend,
            "mid_term_trend": mid_trend,
            "pattern": detected_pattern,
            "candlestick": detected_pattern,
            "stars": stars,
            "suggested_holding": holding_period
        }

    except Exception as e:
        print(f"Analysis error: {str(e)}")
        return None
