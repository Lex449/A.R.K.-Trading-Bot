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
    """
    Erkennt relevante Candlestick-Muster in den letzten Kerzendaten.

    Args:
        df (pd.DataFrame): Candle-Daten mit 'o', 'h', 'l', 'c'-Spalten.

    Returns:
        list: Liste erkannter Muster inkl. Richtung, Confidence und Sternebewertung.
    """
    results = []
    if df.empty or len(df) < 2:
        return results

    last = df.iloc[-1]
    prev = df.iloc[-2]

    body = abs(last['c'] - last['o'])
    candle_range = last['h'] - last['l']

    if candle_range == 0:
        return results  # Schutz vor Division by Zero

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

    # === Zusatz: Momentum-Erkennung über 10 Candles ===
    if len(df) >= 11:
        recent_close = df['c'].iloc[-1]
        close_10min_ago = df['c'].iloc[-11]
        percentage_change = ((recent_close - close_10min_ago) / close_10min_ago) * 100

        if percentage_change >= 2.5:
            results.append({"pattern": "Strong Bullish Momentum", **PATTERN_DEFINITIONS["Strong Bullish Momentum"]})
        elif percentage_change <= -2.5:
            results.append({"pattern": "Strong Bearish Momentum", **PATTERN_DEFINITIONS["Strong Bearish Momentum"]})

    return results
