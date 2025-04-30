"""
A.R.K. Indicator Engine – Ultra Adaptive 6.0
Real-Time Momentum, Trend & RSI Fusion Scoring for Smart Signal Expansion.

Optimized for: Looser Confirmation Thresholds, Expanded Signal Frequency, Stable Risk Profile.
Made in Bali. Engineered with German Precision.
"""

import pandas as pd
import numpy as np
from bot.utils.logger import setup_logger

logger = setup_logger(__name__)

def evaluate_indicators(df: pd.DataFrame) -> tuple[float, str]:
    """
    Evaluates EMA trend, RSI conditions and combined signal score.

    Returns:
        tuple: (score: 0–100, trend: str)
    """

    if df is None or df.empty or len(df) < 20 or "c" not in df.columns:
        logger.warning("⚠️ [IndicatorEngine] Not enough data or missing columns.")
        return 52.0, "Neutral ⚪"

    try:
        close = df["c"]

        # === EMA-Trend-Erkennung ===
        ema_9 = close.ewm(span=9, adjust=False).mean()
        ema_21 = close.ewm(span=21, adjust=False).mean()
        last_ema9 = ema_9.iloc[-1]
        last_ema21 = ema_21.iloc[-1]

        trend = (
            "Long 📈" if last_ema9 > last_ema21 else
            "Short 📉" if last_ema9 < last_ema21 else
            "Neutral ⚪"
        )

        # === RSI-Berechnung ===
        delta = close.diff()
        gain = np.maximum(delta, 0)
        loss = np.abs(np.minimum(delta, 0))
        avg_gain = pd.Series(gain).rolling(window=14, min_periods=14).mean().iloc[-1]
        avg_loss = pd.Series(loss).rolling(window=14, min_periods=14).mean().iloc[-1]
        rsi = 100 if avg_loss == 0 else 100 - (100 / (1 + avg_gain / (avg_loss + 1e-9)))

        # === Scoring Logik ===
        score = 50.0

        # Trend-Bonus
        score += 18 if trend == "Long 📈" else -18 if trend == "Short 📉" else 0

        # RSI-Zonen
        if rsi < 25:
            score += 12
        elif rsi > 75:
            score -= 12
        elif 45 <= rsi <= 55:
            score += 3

        # Micro-Tuning bei bestätigtem Trend
        if trend == "Long 📈":
            if 60 < rsi < 70:
                score += 6
            if 50 < rsi < 60:
                score += 4
        elif trend == "Short 📉":
            if 30 < rsi < 40:
                score += 6
            if 40 < rsi < 50:
                score += 4

        final_score = round(np.clip(score, 0, 100), 2)

        logger.info(f"📊 [IndicatorEngine] Final Score: {final_score:.2f} | RSI: {rsi:.2f} | Trend: {trend}")
        return final_score, trend

    except Exception as e:
        logger.error(f"❌ [IndicatorEngine] Critical Error: {e}")
        return 50.0, "Neutral ⚪"
