# bot/utils/indicators.py

def calculate_rsi(closes, period=14):
    """Berechnet den Relative Strength Index (RSI)."""
    if len(closes) < period + 1:
        return []

    gains, losses = 0.0, 0.0
    for i in range(1, period + 1):
        delta = closes[i] - closes[i - 1]
        gains += max(delta, 0)
        losses += max(-delta, 0)

    avg_gain = gains / period
    avg_loss = losses / period
    rs = avg_gain / avg_loss if avg_loss != 0 else 0
    rsi = [100 - (100 / (1 + rs))]

    for i in range(period + 1, len(closes)):
        delta = closes[i] - closes[i - 1]
        gain = max(delta, 0)
        loss = max(-delta, 0)

        avg_gain = (avg_gain * (period - 1) + gain) / period
        avg_loss = (avg_loss * (period - 1) + loss) / period
        rs = avg_gain / avg_loss if avg_loss != 0 else 0
        rsi.append(100 - (100 / (1 + rs)))

    return rsi

def calculate_ema(closes, period=20):
    """Berechnet den Exponential Moving Average (EMA)."""
    if not closes or len(closes) < period:
        return []

    ema = [sum(closes[:period]) / period]  # Initial EMA als Durchschnitt
    k = 2 / (period + 1)

    for price in closes[period:]:
        ema.append(price * k + ema[-1] * (1 - k))

    return ema
