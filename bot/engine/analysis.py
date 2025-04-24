# bot/engine/analysis.py

import pandas as pd
from bot.engine.data_provider import get_market_data
from bot.engine.indicator import calculate_rsi, calculate_ema, detect_candlestick_pattern
from bot.config.settings import get_settings

settings = get_settings()

def analyze_symbol(symbol: str):
    df = get_market_data(symbol, settings["INTERVAL"])
    if df is None or len(df) < 2:
        return None

    closes = df["close"].tolist()
    rsi_series = calculate_rsi(closes, settings["RSI_PERIOD"])
    ema_short = calculate_ema(closes, settings["EMA_SHORT_PERIOD"])
    ema_long = calculate_ema(closes, settings["EMA_LONG_PERIOD"])
    pattern = detect_candlestick_pattern(df)

    if not rsi_series or not ema_short or not ema_long:
        return None

    rsi = rsi_series[-1]
    ema_s = ema_short[-1]
    ema_l = ema_long[-1]

    trend = "Uptrend" if ema_s > ema_l else "Downtrend"
    signal = None

    # Kombination aus RSI + Pattern + EMA-Cross
    if rsi < 30 and pattern in ["Hammer", "Bullish Engulfing"]:
        signal = "LONG"
    elif rsi > 70 and pattern in ["Shooting Star", "Bearish Engulfing"]:
        signal = "SHORT"
    elif ema_short[-2] <= ema_long[-2] and ema_s > ema_l:
        signal = "LONG"
    elif ema_short[-2] >= ema_long[-2] and ema_s < ema_l:
        signal = "SHORT"

    confidence = 3
    if signal == "LONG" and rsi < 25:
        confidence = 5
    elif signal == "SHORT" and rsi > 75:
        confidence = 5

    return {
        "symbol": symbol,
        "price": df["close"].iloc[-1],
        "rsi": rsi,
        "trend": trend,
        "pattern": pattern,
        "signal": signal,
        "confidence": confidence
    }
