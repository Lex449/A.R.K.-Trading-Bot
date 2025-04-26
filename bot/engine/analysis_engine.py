import os
import requests
import pandas as pd
import numpy as np

FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')
FINNHUB_BASE_URL = "https://finnhub.io/api/v1"

async def analyze_symbol(symbol: str) -> dict:
    """
    Ultra Analysis Engine for trading signals based on real-time data.
    Combines RSI, multi-timeframe trend detection, and candlestick patterns
    to deliver a powerful, rated trading opportunity.
    """

    try:
        quote_url = f"{FINNHUB_BASE_URL}/quote"
        params = {"symbol": symbol, "token": FINNHUB_API_KEY}
        quote_resp = requests.get(quote_url, params=params).json()

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

        df = pd.DataFrame({
            "t": candles_resp["t"],
            "o": candles_resp["o"],
            "h": candles_resp["h"],
            "l": candles_resp["l"],
            "c": candles_resp["c"],
            "v": candles_resp["v"]
        })

        delta = df["c"].diff()
        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)
        avg_gain = pd.Series(gain).rolling(window=14).mean()
        avg_loss = pd.Series(loss).rolling(window=14).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        latest_rsi = rsi.iloc[-1]

        short_trend = "Uptrend" if df["c"].iloc[-5:].is_monotonic_increasing else "Downtrend" if df["c"].iloc[-5:].is_monotonic_decreasing else "Sideways"
        mid_trend = "Uptrend" if df["c"].iloc[-15:].is_monotonic_increasing else "Downtrend" if df["c"].iloc[-15:].is_monotonic_decreasing else "Sideways"

        last_candle = {
            "open": df["o"].iloc[-1],
            "close": df["c"].iloc[-1],
            "high": df["h"].iloc[-1],
            "low": df["l"].iloc[-1]
        }

        candle_pattern = "No clear pattern"
        body = abs(last_candle["close"] - last_candle["open"])
        candle_range = last_candle["high"] - last_candle["low"]

        if body < 0.3 * candle_range:
            candle_pattern = "Doji"
        elif last_candle["close"] > last_candle["open"] and body > 0.6 * candle_range:
            candle_pattern = "Bullish Engulfing"
        elif last_candle["close"] < last_candle["open"] and body > 0.6 * candle_range:
            candle_pattern = "Bearish Engulfing"
        elif (last_candle["high"] - max(last_candle["close"], last_candle["open"])) > body * 2:
            candle_pattern = "Shooting Star"
        elif (min(last_candle["close"], last_candle["open"]) - last_candle["low"]) > body * 2:
            candle_pattern = "Hammer"

        signal = "Hold"
        if short_trend == "Uptrend" and latest_rsi < 70:
            signal = "Buy"
        elif short_trend == "Downtrend" and latest_rsi > 30:
            signal = "Sell"

        stars = 3
        if signal in ["Buy", "Sell"] and "Engulfing" in candle_pattern:
            stars = 5
        elif signal in ["Buy", "Sell"] and ("Hammer" in candle_pattern or "Shooting Star" in candle_pattern):
            stars = 4
        elif signal == "Hold":
            stars = 2
        else:
            stars = 1

        holding_period = "Short-Term" if short_trend == mid_trend else "Mid-Term"

        return {
            "signal": signal,
            "rsi": round(latest_rsi, 2),
            "short_term_trend": short_trend,
            "mid_term_trend": mid_trend,
            "pattern": candle_pattern,
            "candlestick": candle_pattern,
            "stars": stars,
            "suggested_holding": holding_period
        }

    except Exception as e:
        print(f"Analysis error: {str(e)}")
        return None
