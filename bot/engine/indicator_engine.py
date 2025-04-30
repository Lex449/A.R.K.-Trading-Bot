"""
A.R.K. Indicator Engine – Ultra Adaptive 5.5
Real-Time Momentum, Trend & RSI Fusion Scoring for Smart Signal Expansion.

Optimized for: Looser Confirmation Thresholds, More Signals, Still Stable Risk Profile.
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
        return 52.0, "Neutral ⚪"

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

        # === Scoring ===
        score = 50.0

        # Trend Bonus
        if trend == "Long 📈":
            score += 18
        elif trend == "Short 📉":
            score -= 18

        # RSI Expansion (Looser)
        if rsi < 25:
            score += 12
        elif rsi > 75:
            score -= 12
        elif 45 <= rsi <= 55:
            score += 3  # Neutral RSI is still usable

        # Micro-Bias Tuning
        if 60 < rsi < 70 and trend == "Long 📈":
            score += 6
        if 30 < rsi < 40 and trend == "Short 📉":
            score += 6

        # Trend + Neutral RSI Synergy
        if 50 < rsi < 60 and trend == "Long 📈":
            score += 4
        if 40 < rsi < 50 and trend == "Short 📉":
            score += 4

        final_score = round(np.clip(score, 0, 100), 2)
        logger.info(f"📊 [IndicatorEngine] Score: {final_score:.2f} | RSI: {rsi:.2f} | Trend: {trend}")
        return final_score, trend

    except Exception as e:
        logger.error(f"❌ [IndicatorEngine Error] {e}")
        return 50.0, "Neutral ⚪"
