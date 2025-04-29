"""
A.R.K. Pattern & Indicator Engine – Strategic Fusion Build 4.0
Combines advanced candlestick pattern detection and smart indicator scoring.

Optimiert für: Sofortsignale, Ultra-Scoring, Trend-Validierung & Multilingual Output.
"""

import pandas as pd
import numpy as np
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# === Pattern Definitions (Optimiert & Klassifiziert) ===
PATTERN_DEFINITIONS = {
    "Three White Soldiers": {"action": "Long 📈", "confidence": 82, "stars": 5},
    "Three Black Crows": {"action": "Short 📉", "confidence": 80, "stars": 5},
    "Morning Star": {"action": "Long 📈", "confidence": 75, "stars": 5},
    "Evening Star": {"action": "Short 📉", "confidence": 74, "stars": 5},
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
    "Doji": {"action": "Neutral ⚪", "confidence": 52, "stars": 3},
    "Dragonfly Doji": {"action": "Long 📈", "confidence": 54, "stars": 3},
    "Gravestone Doji": {"action": "Short 📉", "confidence": 54, "stars": 3},
    "Spinning Top": {"action": "Neutral ⚪", "confidence": 50, "stars": 3},
    "Strong Bullish Momentum": {"action": "Long 📈", "confidence": 77, "stars": 4},
    "Strong Bearish Momentum": {"action": "Short 📉", "confidence": 77, "stars": 4},
}

def detect_patterns(df: pd.DataFrame, min_confidence: int = 55) -> list:
    """
    Detects candlestick patterns and filters by confidence.

    Returns:
        list: Qualified patterns with metadata.
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
            return results

        # One- & Two-Candle Patterns
        if body < 0.1 * candle_range:
            results.append({"pattern": "Doji", **PATTERN_DEFINITIONS["Doji"]})
        if last["c"] > last["o"] and last["o"] < prev["c"] and last["c"] > prev["o"]:
            results.append({"pattern": "Bullish Engulfing", **PATTERN_DEFINITIONS["Bullish Engulfing"]})
        if last["o"] > last["c"] and last["c"] < prev["o"] and last["o"] > prev["c"]:
            results.append({"pattern": "Bearish Engulfing", **PATTERN_DEFINITIONS["Bearish Engulfing"]})
        if last["c"] > last["o"] and last["l"] < min(last["c"], last["o"]) - body:
            results.append({"pattern": "Hammer", **PATTERN_DEFINITIONS["Hammer"]})
        if last["h"] > max(last["c"], last["o"]) + body:
            results.append({"pattern": "Shooting Star", **PATTERN_DEFINITIONS["Shooting Star"]})

        # Three-Candle Patterns
        if prev2["c"] < prev2["o"] and abs(prev["c"] - prev["o"]) < (prev["h"] - prev["l"]) * 0.3 and last["c"] > last["o"] and last["c"] > (prev2["o"] + prev2["c"]) / 2:
            results.append({"pattern": "Morning Star", **PATTERN_DEFINITIONS["Morning Star"]})
        if prev2["c"] > prev2["o"] and abs(prev["c"] - prev["o"]) < (prev["h"] - prev["l"]) * 0.3 and last["c"] < last["o"] and last["c"] < (prev2["o"] + prev2["c"]) / 2:
            results.append({"pattern": "Evening Star", **PATTERN_DEFINITIONS["Evening Star"]})

        # Momentum Trend
        if len(df) >= 11:
            change_pct = ((df["c"].iloc[-1] - df["c"].iloc[-11]) / df["c"].iloc[-11]) * 100
            if change_pct >= 2.5:
                results.append({"pattern": "Strong Bullish Momentum", **PATTERN_DEFINITIONS["Strong Bullish Momentum"]})
            elif change_pct <= -2.5:
                results.append({"pattern": "Strong Bearish Momentum", **PATTERN_DEFINITIONS["Strong Bearish Momentum"]})

        qualified = [p for p in results if p["confidence"] >= min_confidence]
        logger.info(f"[PatternEngine] Detected {len(qualified)} strong patterns.")
        return qualified

    except Exception as e:
        logger.error(f"[PatternEngine Critical Error] {e}")
        return []


def evaluate_indicators(df: pd.DataFrame) -> tuple:
    """
    Evaluates market momentum using EMA and RSI.

    Returns:
        (score: float, trend: str)
    """
    if df is None or df.empty or len(df) < 20:
        return 50.0, "Neutral ⚪"

    try:
        df["EMA_9"] = df["c"].ewm(span=9, adjust=False).mean()
        df["EMA_21"] = df["c"].ewm(span=21, adjust=False).mean()

        last_ema9 = df["EMA_9"].iloc[-1]
        last_ema21 = df["EMA_21"].iloc[-1]
        trend = "Long 📈" if last_ema9 > last_ema21 else "Short 📉" if last_ema9 < last_ema21 else "Neutral ⚪"

        delta = df["c"].diff()
        gain = np.maximum(delta, 0)
        loss = np.abs(np.minimum(delta, 0))

        avg_gain = pd.Series(gain).rolling(window=14).mean().iloc[-1]
        avg_loss = pd.Series(loss).rolling(window=14).mean().iloc[-1]
        rsi = 100.0 if avg_loss == 0 else 100 - (100 / (1 + (avg_gain / avg_loss)))

        score = 50
        score += 20 if trend == "Long 📈" else -20 if trend == "Short 📉" else 0
        score += 10 if rsi < 30 else -10 if rsi > 70 else 0

        return round(max(0, min(score, 100)), 2), trend

    except Exception as e:
        logger.error(f"[IndicatorEngine Error] {e}")
        return 50.0, "Neutral ⚪"
