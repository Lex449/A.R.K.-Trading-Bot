import pandas as pd

def detect_candle_patterns(df: pd.DataFrame) -> str:
    """
    Erkenne klassische Candlestick-Muster für Short-/Long-Setups.
    Unterstützt Hammer, Shooting Star, Bullish Engulfing, Bearish Engulfing und Doji.
    """
    last = df.iloc[-1]
    body = abs(last['c'] - last['o'])
    candle_range = last['h'] - last['l']

    if candle_range == 0:
        return "No Pattern"

    # Doji (unsichere Märkte)
    if body < 0.1 * candle_range:
        return "Doji"

    # Bullish Engulfing (potentieller Long)
    if (last['c'] > last['o']) and (body > 0.6 * candle_range):
        return "Bullish Engulfing"

    # Bearish Engulfing (potentieller Short)
    if (last['o'] > last['c']) and (body > 0.6 * candle_range):
        return "Bearish Engulfing"

    # Hammer (Long-Setup bei Bodenbildung)
    if (last['c'] > last['o']) and (last['l'] < min(last['c'], last['o']) - body):
        return "Hammer"

    # Shooting Star (Short-Setup bei Topbildung)
    if (last['h'] > max(last['c'], last['o']) + body):
        return "Shooting Star"

    return "No Pattern"
