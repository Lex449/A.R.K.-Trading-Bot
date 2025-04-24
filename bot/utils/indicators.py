# bot/utils/indicator.py

import pandas as pd

def calculate_rsi(closes: list, period: int = 14):
    if len(closes) < period + 1:
        return []

    rsi_values = []
    gains = 0.0
    losses = 0.0

    for i in range(1, period + 1):
        change = closes[i] - closes[i - 1]
        gains += max(change, 0)
        losses += max(-change, 0)

    avg_gain = gains / period
    avg_loss = losses / period

    rs = avg_gain / avg_loss if avg_loss != 0 else 0
    rsi = 100 - (100 / (1 + rs))
    rsi_values.append(rsi)

    for i in range(period + 1, len(closes)):
        change = closes[i] - closes[i - 1]
        gain = max(change, 0)
        loss = max(-change, 0)

        avg_gain = (avg_gain * (period - 1) + gain) / period
        avg_loss = (avg_loss * (period - 1) + loss) / period

        rs = avg_gain / avg_loss if avg_loss != 0 else 0
        rsi = 100 - (100 / (1 + rs))
        rsi_values.append(rsi)

    return rsi_values

def calculate_ema(closes: list, period: int):
    if not closes or period <= 0:
        return []

    ema = []
    multiplier = 2 / (period + 1)
    ema.append(closes[0])

    for price in closes[1:]:
        next_ema = (price - ema[-1]) * multiplier + ema[-1]
        ema.append(next_ema)

    return ema

def detect_candlestick_pattern(df: pd.DataFrame):
    pattern = "Neutral"
    if len(df) < 2:
        return pattern

    prev = df.iloc[-2]
    last = df.iloc[-1]

    prev_body = prev["close"] - prev["open"]
    last_body = last["close"] - last["open"]

    # Engulfing Pattern
    if prev_body < 0 < last_body and last["close"] > prev["open"] and last["open"] < prev["close"]:
        return "Bullish Engulfing"
    elif prev_body > 0 > last_body and last["close"] < prev["open"] and last["open"] > prev["close"]:
        return "Bearish Engulfing"

    # Hammer / Shooting Star
    body = abs(last["close"] - last["open"])
    range_total = last["high"] - last["low"]
    upper_shadow = last["high"] - max(last["close"], last["open"])
    lower_shadow = min(last["close"], last["open"]) - last["low"]

    if range_total > 0:
        if body < range_total * 0.3 and lower_shadow > body * 2 and upper_shadow < body * 0.5:
            return "Hammer"
        elif body < range_total * 0.3 and upper_shadow > body * 2 and lower_shadow < body * 0.5:
            return "Shooting Star"

    return pattern
