"""
A.R.K. Pattern & Indicator Engine – Hyper Premium 6.1
Reworked for realistic Signal Detection. Flexible, Robust, Market-Proven.
Made in Bali. Engineered with German Precision.
"""

import pandas as pd
import numpy as np
from bot.utils.logger import setup_logger

logger = setup_logger(__name__)

PATTERN_DEFINITIONS = {
    "Three White Soldiers": {"action": "Long 📈", "confidence": 85, "stars": 5},
    "Three Black Crows": {"action": "Short 📉", "confidence": 85, "stars": 5},
    "Morning Star": {"action": "Long 📈", "confidence": 80, "stars": 5},
    "Evening Star": {"action": "Short 📉", "confidence": 80, "stars": 5},
    "Bullish Engulfing": {"action": "Long 📈", "confidence": 75, "stars": 4},
    "Bearish Engulfing": {"action": "Short 📉", "confidence": 75, "stars": 4},
    "Hammer": {"action": "Long 📈", "confidence": 70, "stars": 4},
    "Shooting Star": {"action": "Short 📉", "confidence": 70, "stars": 4},
    "Doji": {"action": "Neutral ⚪", "confidence": 55, "stars": 3},
    "Strong Bullish Momentum": {"action": "Long 📈", "confidence": 78, "stars": 4},
    "Strong Bearish Momentum": {"action": "Short 📉", "confidence": 78, "stars": 4},
}

def detect_patterns(df: pd.DataFrame, min_confidence: int = 55) -> list:
    results = []
    if df is None or df.empty or len(df) < 3:
        return results

    try:
        last, prev, prev2 = df.iloc[-1], df.iloc[-2], df.iloc[-3]
        body = abs(last["c"] - last["o"])
        candle_range = last["h"] - last["l"]
        if candle_range == 0 or body == 0:
            return results

        # 1–2 Candle Patterns
        if body < 0.1 * candle_range:
            results.append({"pattern": "Doji", **PATTERN_DEFINITIONS["Doji"]})
        if last["c"] > last["o"] and prev["c"] < prev["o"] and last["o"] < prev["c"] and last["c"] > prev["o"]:
            results.append({"pattern": "Bullish Engulfing", **PATTERN_DEFINITIONS["Bullish Engulfing"]})
        if last["o"] > last["c"] and prev["o"] < prev["c"] and last["c"] < prev["o"] and last["o"] > prev["c"]:
            results.append({"pattern": "Bearish Engulfing", **PATTERN_DEFINITIONS["Bearish Engulfing"]})
        if last["c"] > last["o"] and (last["l"] < last["o"] - body * 0.5):
            results.append({"pattern": "Hammer", **PATTERN_DEFINITIONS["Hammer"]})
        if last["o"] > last["c"] and (last["h"] > last["o"] + body * 0.5):
            results.append({"pattern": "Shooting Star", **PATTERN_DEFINITIONS["Shooting Star"]})

        # 3-Candle Reversal Patterns
        if prev2["c"] < prev2["o"] and prev["c"] > prev["o"] and last["c"] > last["o"] and last["c"] > prev2["o"]:
            results.append({"pattern": "Morning Star", **PATTERN_DEFINITIONS["Morning Star"]})
        if prev2["c"] > prev2["o"] and prev["c"] < prev["o"] and last["c"] < last["o"] and last["c"] < prev2["o"]:
            results.append({"pattern": "Evening Star", **PATTERN_DEFINITIONS["Evening Star"]})

        # Momentum Patterns
        if len(df) >= 11:
            change_pct = ((df["c"].iloc[-1] - df["c"].iloc[-11]) / df["c"].iloc[-11]) * 100
            if change_pct >= 2.0:
                results.append({"pattern": "Strong Bullish Momentum", **PATTERN_DEFINITIONS["Strong Bullish Momentum"]})
            elif change_pct <= -2.0:
                results.append({"pattern": "Strong Bearish Momentum", **PATTERN_DEFINITIONS["Strong Bearish Momentum"]})

        qualified = [p for p in results if p["confidence"] >= min_confidence]
        logger.info(f"[PatternAnalysisEngine] {len(qualified)} pattern(s) qualified.")
        return qualified

    except Exception as e:
        logger.error(f"❌ [PatternDetection] Critical Error: {e}")
        return []

def evaluate_indicators(df: pd.DataFrame) -> tuple:
    if df is None or df.empty or len(df) < 20:
        return 50.0, "Neutral ⚪"
    try:
        df["EMA_9"] = df["c"].ewm(span=9).mean()
        df["EMA_21"] = df["c"].ewm(span=21).mean()
        last_ema9, last_ema21 = df["EMA_9"].iloc[-1], df["EMA_21"].iloc[-1]
        trend = "Long 📈" if last_ema9 > last_ema21 else "Short 📉" if last_ema9 < last_ema21 else "Neutral ⚪"

        delta = df["c"].diff()
        gain = np.maximum(delta, 0)
        loss = np.abs(np.minimum(delta, 0))
        avg_gain = pd.Series(gain).rolling(14).mean().iloc[-1]
        avg_loss = pd.Series(loss).rolling(14).mean().iloc[-1]
        rsi = 100.0 if avg_loss == 0 else 100 - (100 / (1 + (avg_gain / avg_loss)))

        score = 50 + (15 if trend == "Long 📈" else -15 if trend == "Short 📉" else 0)
        score += 10 if rsi < 30 else -10 if rsi > 70 else 0
        return round(np.clip(score, 0, 100), 2), trend

    except Exception as e:
        logger.error(f"❌ [IndicatorEvaluator Error]: {e}")
        return 50.0, "Neutral ⚪"
