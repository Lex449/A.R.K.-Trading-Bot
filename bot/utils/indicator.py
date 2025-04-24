import pandas as pd

def calculate_rsi(closes: list, period: int = 14) -> list:
    if len(closes) < period + 1:
        return []

    rsi_values = []
    gains = 0.0
    losses = 0.0

    for i in range(1, period + 1):
        delta = closes[i] - closes[i - 1]
        gains += max(delta, 0)
        losses += max(-delta, 0)

    avg_gain = gains / period
    avg_loss = losses / period
    rs = avg_gain / avg_loss if avg_loss != 0 else 0
    rsi_values.append(100 - (100 / (1 + rs)))

    for i in range(period + 1, len(closes)):
        delta = closes[i] - closes[i - 1]
        gain = max(delta, 0)
        loss = max(-delta, 0)

        avg_gain = (avg_gain * (period - 1) + gain) / period
        avg_loss = (avg_loss * (period - 1) + loss) / period
        rs = avg_gain / avg_loss if avg_loss != 0 else 0
        rsi = 100 - (100 / (1 + rs))
        rsi_values.append(rsi)

    return rsi_values

def calculate_ema(closes: list, period: int) -> list:
    if not closes or period <= 0:
        return []

    ema = [closes[0]]
    multiplier = 2 / (period + 1)

    for price in closes[1:]:
        next_value = (price - ema[-1]) * multiplier + ema[-1]
        ema.append(next_value)

    return ema

def detect_candlestick_pattern(df: pd.DataFrame) -> str:
    if len(df) < 2:
        return "Neutral"

    prev = df.iloc[-2]
    last = df.iloc[-1]

    prev_body = prev["close"] - prev["open"]
    last_body = last["close"] - last["open"]

    # Engulfing
    if prev_body < 0 < last_body and last["close"] > prev["open"] and last["open"] < prev["close"]:
        return "Bullish Engulfing"
    elif prev_body > 0 > last_body and last["close"] < prev["open"] and last["open"] > prev["close"]:
        return "Bearish Engulfing"

    # Hammer / Shooting Star
    body = abs(last["close"] - last["open"])
    candle_range = last["high"] - last["low"]
    upper_shadow = last["high"] - max(last["close"], last["open"])
    lower_shadow = min(last["close"], last["open"]) - last["low"]

    if candle_range > 0:
        if body < candle_range * 0.3 and lower_shadow > body * 2 and upper_shadow < body * 0.5:
            return "Hammer"
        elif body < candle_range * 0.3 and upper_shadow > body * 2 and lower_shadow < body * 0.5:
            return "Shooting Star"

    return "Neutral"
