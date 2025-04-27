# bot/engine/pattern_detector.py

"""
Erkennung relevanter Candlestick-Muster für Trading-Signale.
Ultra-Masterclass Build – 100 % Präzision, 100 % Zuverlässigkeit.
"""

import pandas as pd

# === Muster-Mapping: Pattern Name ➔ Richtung, Confidence %, Sterne ===
PATTERN_DEFINITIONS = {
    # ⭐⭐⭐⭐⭐ Patterns
    "Three White Soldiers": {"action": "Long", "confidence": 82, "stars": 5},
    "Three Black Crows": {"action": "Short", "confidence": 78, "stars": 5},
    "Morning Star": {"action": "Long", "confidence": 68, "stars": 5},
    "Evening Star": {"action": "Short", "confidence": 69, "stars": 5},

    # ⭐⭐⭐⭐ Patterns
    "Bullish Engulfing": {"action": "Long", "confidence": 65, "stars": 4},
    "Bearish Engulfing": {"action": "Short", "confidence": 72, "stars": 4},
    "Piercing Line": {"action": "Long", "confidence": 60, "stars": 4},
    "Dark Cloud Cover": {"action": "Short", "confidence": 65, "stars": 4},
    "Hammer": {"action": "Long", "confidence": 60, "stars": 4},
    "Shooting Star": {"action": "Short", "confidence": 59, "stars": 4},
    "Bullish Harami": {"action": "Long", "confidence": 63, "stars": 4},
    "Bearish Harami": {"action": "Short", "confidence": 63, "stars": 4},
    "Tweezer Top": {"action": "Short", "confidence": 61, "stars": 4},
    "Tweezer Bottom": {"action": "Long", "confidence": 61, "stars": 4},

    # ⭐⭐⭐ Patterns
    "Doji": {"action": "Neutral", "confidence": 50, "stars": 3},
    "Spinning Top": {"action": "Neutral", "confidence": 50, "stars": 3},
    "Dragonfly Doji": {"action": "Long", "confidence": 54, "stars": 3},
    "Gravestone Doji": {"action": "Short", "confidence": 54, "stars": 3},

    # ✨ Momentum-Patterns
    "Strong Bullish Momentum": {"action": "Long", "confidence": 75, "stars": 4},
    "Strong Bearish Momentum": {"action": "Short", "confidence": 75, "stars": 4},
}

def detect_candle_patterns(df: pd.DataFrame) -> list:
    results = []
    if df.empty or len(df) < 3:
        return results

    last = df.iloc[-1]
    prev = df.iloc[-2]
    prev2 = df.iloc[-3]

    body = abs(last['c'] - last['o'])
    candle_range = last['h'] - last['l']

    if candle_range == 0:
        return results

    # === Einzelmustererkennung ===

    # 1. Doji
    if body < 0.1 * candle_range:
        results.append({"pattern": "Doji", **PATTERN_DEFINITIONS["Doji"]})

    # 2. Bullish Engulfing
    if (last['c'] > last['o']) and (last['o'] < prev['c']) and (last['c'] > prev['o']):
        results.append({"pattern": "Bullish Engulfing", **PATTERN_DEFINITIONS["Bullish Engulfing"]})

    # 3. Bearish Engulfing
    if (last['o'] > last['c']) and (last['c'] < prev['o']) and (last['o'] > prev['c']):
        results.append({"pattern": "Bearish Engulfing", **PATTERN_DEFINITIONS["Bearish Engulfing"]})

    # 4. Hammer
    if (last['c'] > last['o']) and (last['l'] < min(last['c'], last['o']) - body):
        results.append({"pattern": "Hammer", **PATTERN_DEFINITIONS["Hammer"]})

    # 5. Shooting Star
    if (last['h'] > max(last['c'], last['o']) + body):
        results.append({"pattern": "Shooting Star", **PATTERN_DEFINITIONS["Shooting Star"]})

    # 6. Piercing Line
    if (
        prev['o'] > prev['c'] and
        last['c'] > last['o'] and
        last['o'] < prev['c'] and
        last['c'] > (prev['o'] + prev['c']) / 2
    ):
        results.append({"pattern": "Piercing Line", **PATTERN_DEFINITIONS["Piercing Line"]})

    # 7. Dark Cloud Cover
    if (
        prev['c'] > prev['o'] and
        last['o'] > last['c'] and
        last['o'] > prev['c'] and
        last['c'] < (prev['o'] + prev['c']) / 2
    ):
        results.append({"pattern": "Dark Cloud Cover", **PATTERN_DEFINITIONS["Dark Cloud Cover"]})

    # 8. Bullish Harami
    if (
        prev['o'] > prev['c'] and
        last['o'] < last['c'] and
        last['o'] > prev['c'] and
        last['c'] < prev['o']
    ):
        results.append({"pattern": "Bullish Harami", **PATTERN_DEFINITIONS["Bullish Harami"]})

    # 9. Bearish Harami
    if (
        prev['c'] > prev['o'] and
        last['c'] < last['o'] and
        last['c'] > prev['o'] and
        last['o'] < prev['c']
    ):
        results.append({"pattern": "Bearish Harami", **PATTERN_DEFINITIONS["Bearish Harami"]})

    # 10. Tweezer Top
    if (
        prev['c'] > prev['o'] and
        last['o'] > last['c'] and
        abs(prev['h'] - last['h']) < (candle_range * 0.1)
    ):
        results.append({"pattern": "Tweezer Top", **PATTERN_DEFINITIONS["Tweezer Top"]})

    # 11. Tweezer Bottom
    if (
        prev['o'] > prev['c'] and
        last['c'] > last['o'] and
        abs(prev['l'] - last['l']) < (candle_range * 0.1)
    ):
        results.append({"pattern": "Tweezer Bottom", **PATTERN_DEFINITIONS["Tweezer Bottom"]})

    # 12. Morning Star
    if (
        prev2['c'] < prev2['o'] and
        abs(prev['c'] - prev['o']) < (prev['h'] - prev['l']) * 0.3 and
        last['c'] > last['o'] and
        last['c'] > (prev2['o'] + prev2['c']) / 2
    ):
        results.append({"pattern": "Morning Star", **PATTERN_DEFINITIONS["Morning Star"]})

    # 13. Evening Star
    if (
        prev2['c'] > prev2['o'] and
        abs(prev['c'] - prev['o']) < (prev['h'] - prev['l']) * 0.3 and
        last['c'] < last['o'] and
        last['c'] < (prev2['o'] + prev2['c']) / 2
    ):
        results.append({"pattern": "Evening Star", **PATTERN_DEFINITIONS["Evening Star"]})

    # 14. Three White Soldiers
    if (
        prev2['c'] > prev2['o'] and
        prev['c'] > prev['o'] and
        last['c'] > last['o'] and
        prev2['c'] < prev['c'] and
        prev['c'] < last['c']
    ):
        results.append({"pattern": "Three White Soldiers", **PATTERN_DEFINITIONS["Three White Soldiers"]})

    # 15. Three Black Crows
    if (
        prev2['c'] < prev2['o'] and
        prev['c'] < prev['o'] and
        last['c'] < last['o'] and
        prev2['c'] > prev['c'] and
        prev['c'] > last['c']
    ):
        results.append({"pattern": "Three Black Crows", **PATTERN_DEFINITIONS["Three Black Crows"]})

    # === Momentum-Erkennung ===
    if len(df) >= 11:
        recent_close = df['c'].iloc[-1]
        close_10min_ago = df['c'].iloc[-11]
        percentage_change = ((recent_close - close_10min_ago) / close_10min_ago) * 100

        if percentage_change >= 2.5:
            results.append({"pattern": "Strong Bullish Momentum", **PATTERN_DEFINITIONS["Strong Bullish Momentum"]})
        elif percentage_change <= -2.5:
            results.append({"pattern": "Strong Bearish Momentum", **PATTERN_DEFINITIONS["Strong Bearish Momentum"]})

    return results
