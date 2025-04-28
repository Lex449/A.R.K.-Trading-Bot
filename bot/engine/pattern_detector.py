"""
A.R.K. Pattern Detector – Ultra Money Machine Build.
Detects premium-grade candlestick patterns with adaptive confidence filtering.
"""

import pandas as pd
from bot.utils.logger import setup_logger

# Setup Logger
logger = setup_logger(__name__)

# === Pattern Definitions (Fully Enhanced) ===
PATTERN_DEFINITIONS = {
    # ⭐⭐⭐⭐⭐ Premium Patterns
    "Three White Soldiers": {"action": "Long 📈", "confidence": 82, "stars": 5},
    "Three Black Crows": {"action": "Short 📉", "confidence": 80, "stars": 5},
    "Morning Star": {"action": "Long 📈", "confidence": 75, "stars": 5},
    "Evening Star": {"action": "Short 📉", "confidence": 74, "stars": 5},

    # ⭐⭐⭐⭐ Strong Patterns
    "Bullish Engulfing": {"action": "Long 📈", "confidence": 68, "stars": 4},
    "Bearish Engulfing": {"action": "Short 📉", "confidence": 70, "stars": 4},
    "Piercing Line": {"action": "Long 📈", "confidence": 65, "stars": 4},
    "Dark Cloud Cover": {"action": "Short 📉", "confidence": 65, "stars": 4},
    "Hammer": {"action": "Long 📈", "confidence": 63, "stars": 4},
    "Shooting Star": {"action": "Short 📉", "confidence": 62, "stars": 4},
    "Bullish Harami": {"action": "Long 📈", "confidence": 64, "stars": 4},
    "Bearish Harami": {"action": "Short 📉", "confidence": 64, "stars": 4},
    "Tweezer Top": {"action": "Short 📉", "confidence": 63, "stars": 4},
    "Tweezer Bottom": {"action": "Long 📈", "confidence": 63, "stars": 4},

    # ⭐⭐⭐ Mid Patterns
    "Doji": {"action": "Neutral ⚪", "confidence": 52, "stars": 3},
    "Dragonfly Doji": {"action": "Long 📈", "confidence": 54, "stars": 3},
    "Gravestone Doji": {"action": "Short 📉", "confidence": 54, "stars": 3},
    "Spinning Top": {"action": "Neutral ⚪", "confidence": 50, "stars": 3},

    # ⭐⭐⭐ Momentum Patterns
    "Strong Bullish Momentum": {"action": "Long 📈", "confidence": 77, "stars": 4},
    "Strong Bearish Momentum": {"action": "Short 📉", "confidence": 77, "stars": 4},
}

# === Ultra Pattern Detector ===
def detect_patterns(df: pd.DataFrame, min_confidence: int = 55) -> list:
    """
    Detects premium candlestick patterns with dynamic confidence filtering.

    Args:
        df (pd.DataFrame): OHLCV DataFrame.
        min_confidence (int): Minimum confidence to accept patterns.

    Returns:
        list: List of qualified patterns.
    """
    results = []

    if df is None or df.empty or len(df) < 3:
        return results

    try:
        last = df.iloc[-1]
        prev = df.iloc[-2]
        prev2 = df.iloc[-3]

        body = abs(last["c"] - last["o"])
        candle_range = last["h"] - last["l"]

        if candle_range == 0:
            return results  # Protect against division by zero

        # === Single Candle Patterns ===
        if body < 0.1 * candle_range:
            results.append({"pattern": "Doji", **PATTERN_DEFINITIONS["Doji"]})

        if last["c"] > last["o"] and last["o"] < prev["c"] and last["c"] > prev["o"]:
            results.append({"pattern": "Bullish Engulfing", **PATTERN_DEFINITIONS["Bullish Engulfing"]})

        if last["o"] > last["c"] and last["c"] < prev["o"] and last["o"] > prev["c"]:
            results.append({"pattern": "Bearish Engulfing", **PATTERN_DEFINITIONS["Bearish Engulfing"]})

        if last["c"] > last["o"] and (last["l"] < min(last["c"], last["o"]) - body):
            results.append({"pattern": "Hammer", **PATTERN_DEFINITIONS["Hammer"]})

        if last["h"] > max(last["c"], last["o"]) + body:
            results.append({"pattern": "Shooting Star", **PATTERN_DEFINITIONS["Shooting Star"]})

        # === Two Candle Patterns ===
        if (
            prev["o"] > prev["c"] and
            last["c"] > last["o"] and
            last["o"] < prev["c"] and
            last["c"] > (prev["o"] + prev["c"]) / 2
        ):
            results.append({"pattern": "Piercing Line", **PATTERN_DEFINITIONS["Piercing Line"]})

        if (
            prev["c"] > prev["o"] and
            last["o"] > last["c"] and
            last["o"] > prev["c"] and
            last["c"] < (prev["o"] + prev["c"]) / 2
        ):
            results.append({"pattern": "Dark Cloud Cover", **PATTERN_DEFINITIONS["Dark Cloud Cover"]})

        if (
            prev["o"] > prev["c"] and
            last["o"] < last["c"] and
            last["o"] > prev["c"] and
            last["c"] < prev["o"]
        ):
            results.append({"pattern": "Bullish Harami", **PATTERN_DEFINITIONS["Bullish Harami"]})

        if (
            prev["c"] > prev["o"] and
            last["c"] < last["o"] and
            last["c"] > prev["o"] and
            last["o"] < prev["c"]
        ):
            results.append({"pattern": "Bearish Harami", **PATTERN_DEFINITIONS["Bearish Harami"]})

        # === Three Candle Patterns ===
        if (
            prev2["c"] < prev2["o"] and
            abs(prev["c"] - prev["o"]) < (prev["h"] - prev["l"]) * 0.3 and
            last["c"] > last["o"] and
            last["c"] > (prev2["o"] + prev2["c"]) / 2
        ):
            results.append({"pattern": "Morning Star", **PATTERN_DEFINITIONS["Morning Star"]})

        if (
            prev2["c"] > prev2["o"] and
            abs(prev["c"] - prev["o"]) < (prev["h"] - prev["l"]) * 0.3 and
            last["c"] < last["o"] and
            last["c"] < (prev2["o"] + prev2["c"]) / 2
        ):
            results.append({"pattern": "Evening Star", **PATTERN_DEFINITIONS["Evening Star"]})

        # === Trend Momentum 10 Candle Lookback ===
        if len(df) >= 11:
            close_now = df["c"].iloc[-1]
            close_back = df["c"].iloc[-11]
            change_pct = ((close_now - close_back) / close_back) * 100

            if change_pct >= 2.5:
                results.append({"pattern": "Strong Bullish Momentum", **PATTERN_DEFINITIONS["Strong Bullish Momentum"]})
            elif change_pct <= -2.5:
                results.append({"pattern": "Strong Bearish Momentum", **PATTERN_DEFINITIONS["Strong Bearish Momentum"]})

        # === Filter Patterns by Confidence ===
        qualified_patterns = [p for p in results if p["confidence"] >= min_confidence]

        logger.info(f"[Pattern Detector] {len(qualified_patterns)} premium patterns detected.")

        return qualified_patterns

    except Exception as e:
        logger.error(f"❌ [Pattern Detector] Critical error: {e}")
        return []
