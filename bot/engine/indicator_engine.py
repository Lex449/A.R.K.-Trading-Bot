"""
A.R.K. Indicator Engine – Ultra Adaptive 4.0
Real-Time Momentum, Trend & RSI Fusion Scoring for Elite Trade Validation.

Optimized for: Ultra-Fast Decision Trees, Volatility-Adaptive Biasing, AI-Level Scoring Systems.
"""

import pandas as pd
import numpy as np
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

def evaluate_indicators(df: pd.DataFrame) -> tuple[float, str]:
    """
    Evaluates momentum and trend bias using EMA crossovers and RSI-based fine-tuning.

    Args:
        df (pd.DataFrame): Candlestick DataFrame with 'o', 'h', 'l', 'c' columns.

    Returns:
        tuple: (Indicator Strength Score 0–100, Trend Bias)
    """

    if df is None or df.empty or len(df) < 20:
        logger.warning("⚠️ [IndicatorEngine] Insufficient data for indicator evaluation.")
        return 50.0, "Neutral ⚪"

    try:
        close = df["c"]

        # === EMAs Calculation ===
        ema_9 = close.ewm(span=9, adjust=False).mean()
        ema_21 = close.ewm(span=21, adjust=False).mean()

        last_ema9 = ema_9.iloc[-1]
        last_ema21 = ema_21.iloc[-1]
        last_close = close.iloc[-1]

        # === Basic Trend Bias ===
        if last_ema9 > last_ema21:
            trend = "Long 📈"
        elif last_ema9 < last_ema21:
            trend = "Short 📉"
        else:
            trend = "Neutral ⚪"

        # === RSI Calculation ===
        delta = close.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(window=14, min_periods=14).mean().iloc[-1]
        avg_loss = loss.rolling(window=14, min_periods=14).mean().iloc[-1]

        rsi = 100 if avg_loss == 0 else 100 - (100 / (1 + (avg_gain / avg_loss)))

        # === Indicator Score Assembly ===
        indicator_score = 50.0

        if trend == "Long 📈":
            indicator_score += 20
        elif trend == "Short 📉":
            indicator_score -= 20

        if rsi > 70:
            indicator_score -= 10  # Overbought = Risk for Longs
        elif rsi < 30:
            indicator_score += 10  # Oversold = Potential Bounce

        # Additional Minor Scoring Adjustments
        if 60 < rsi < 70 and trend == "Long 📈":
            indicator_score += 5
        if 30 < rsi < 40 and trend == "Short 📉":
            indicator_score += 5

        indicator_score = round(np.clip(indicator_score, 0, 100), 2)

        logger.info(f"📈 [IndicatorEngine] Score: {indicator_score} | Trend: {trend} | RSI: {rsi:.2f}")

        return indicator_score, trend

    except Exception as e:
        logger.error(f"❌ [IndicatorEngine Critical Error] {e}")
        return 50.0, "Neutral ⚪"
