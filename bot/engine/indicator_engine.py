# bot/engine/indicator_engine.py

"""
A.R.K. Indicator Engine – Ultra Adaptive 5.0
Real-Time Momentum, Trend & RSI Fusion Scoring for Elite Trade Validation.

Optimized for: Ultra-Fast Decision Trees, Volatility-Adaptive Biasing, AI-Level Scoring Systems.
Made in Bali. Engineered with German Precision.
"""

import pandas as pd
import numpy as np
from bot.utils.logger import setup_logger

logger = setup_logger(__name__)

def evaluate_indicators(df: pd.DataFrame) -> tuple[float, str]:
    """
    Evaluates EMA trend, RSI conditions and bias-adjusted score for signal validation.

    Returns:
        tuple: (indicator_score: float 0–100, trend_bias: str)
    """

    if df is None or df.empty or len(df) < 20:
        logger.warning("⚠️ [IndicatorEngine] Insufficient candles for indicator analysis.")
        return 50.0, "Neutral ⚪"

    try:
        close = df["c"]

        # === EMA 9/21 Trend ===
        ema_9 = close.ewm(span=9, adjust=False).mean()
        ema_21 = close.ewm(span=21, adjust=False).mean()

        last_ema9 = ema_9.iloc[-1]
        last_ema21 = ema_21.iloc[-1]

        if last_ema9 > last_ema21:
            trend = "Long 📈"
        elif last_ema9 < last_ema21:
            trend = "Short 📉"
        else:
            trend = "Neutral ⚪"

        # === RSI 14 ===
        delta = close.diff()
        gain = np.maximum(delta, 0)
        loss = np.abs(np.minimum(delta, 0))

        avg_gain = pd.Series(gain).rolling(window=14, min_periods=14).mean().iloc[-1]
        avg_loss = pd.Series(loss).rolling(window=14, min_periods=14).mean().iloc[-1]

        rsi = 100 if avg_loss == 0 else 100 - (100 / (1 + (avg_gain / avg_loss)))

        # === Scoring System ===
        score = 50.0

        if trend == "Long 📈":
            score += 20
        elif trend == "Short 📉":
            score -= 20

        if rsi < 30:
            score += 10
        elif rsi > 70:
            score -= 10

        # Micro-Bias Scoring
        if 60 < rsi < 70 and trend == "Long 📈":
            score += 5
        if 30 < rsi < 40 and trend == "Short 📉":
            score += 5

        # Normalize score
        final_score = round(np.clip(score, 0, 100), 2)

        logger.info(f"📊 [IndicatorEngine] Score: {final_score:.2f} | RSI: {rsi:.2f} | Trend: {trend}")
        return final_score, trend

    except Exception as e:
        logger.error(f"❌ [IndicatorEngine Error] {e}")
        return 50.0, "Neutral ⚪"
