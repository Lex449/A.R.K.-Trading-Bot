# bot/engine/adaptive_trend_detector.py

"""
A.R.K. Adaptive Trend Detector – Elite Signal Intelligence 6.0
Multi-Factor Trend Recognition Engine with RSI Banding, EMA Crossover Strength, and Slope-Momentum Fusion.

Designed for: Early Entry Advantage, Fakeout Filtering, Smart Signal Pre-Bias.
Made in Bali. Engineered with German Precision.
"""

import pandas as pd
import numpy as np
from bot.utils.logger import setup_logger

logger = setup_logger(__name__)

def detect_adaptive_trend(
    df: pd.DataFrame,
    rsi_period: int = 14,
    slope_window: int = 5,
    ma_fast: int = 9,
    ma_slow: int = 21
) -> dict | None:
    """
    Detects early trend conditions using RSI, EMA crossovers, slope momentum and volatility filtering.

    Args:
        df (pd.DataFrame): DataFrame with 'c' (close) prices.
        rsi_period (int): RSI period.
        slope_window (int): Number of candles for slope calculation.
        ma_fast (int): Fast EMA.
        ma_slow (int): Slow EMA.

    Returns:
        dict | None
    """

    if df is None or df.empty or "c" not in df.columns or len(df) < max(rsi_period, slope_window, ma_slow):
        logger.warning("⚠️ [AdaptiveTrend] Insufficient or invalid data for trend analysis.")
        return None

    try:
        close = df["c"].copy()

        # === Slope Detection ===
        x = np.arange(slope_window)
        y = close.tail(slope_window).values
        slope = np.polyfit(x, y, 1)[0]

        # === RSI Calculation ===
        delta = close.diff()
        gain = np.maximum(delta, 0)
        loss = -np.minimum(delta, 0)
        avg_gain = gain.rolling(window=rsi_period).mean()
        avg_loss = loss.rolling(window=rsi_period).mean()
        rs = avg_gain / (avg_loss + 1e-9)
        rsi = 100 - (100 / (1 + rs))
        current_rsi = rsi.iloc[-1]

        # === EMA Cross Calculation ===
        ema_fast = close.ewm(span=ma_fast, adjust=False).mean()
        ema_slow = close.ewm(span=ma_slow, adjust=False).mean()
        last_fast = ema_fast.iloc[-1]
        last_slow = ema_slow.iloc[-1]
        crossover_strength = abs(last_fast - last_slow) / close.iloc[-1] * 100

        # === Bullish Logic ===
        if slope > 0 and last_fast > last_slow and 50 < current_rsi < 68:
            logger.info(f"🚀 [AdaptiveTrend] Early Bullish → RSI: {current_rsi:.2f}, Slope: {slope:.4f}, Crossover Strength: {crossover_strength:.2f}%")
            return {
                "early_trend": "bullish",
                "rsi": round(current_rsi, 2),
                "slope": round(slope, 4),
                "ema_fast": round(last_fast, 4),
                "ema_slow": round(last_slow, 4),
                "crossover_strength": round(crossover_strength, 2)
            }

        # === Bearish Logic ===
        if slope < 0 and last_fast < last_slow and 32 < current_rsi < 50:
            logger.info(f"📉 [AdaptiveTrend] Early Bearish → RSI: {current_rsi:.2f}, Slope: {slope:.4f}, Crossover Strength: {crossover_strength:.2f}%")
            return {
                "early_trend": "bearish",
                "rsi": round(current_rsi, 2),
                "slope": round(slope, 4),
                "ema_fast": round(last_fast, 4),
                "ema_slow": round(last_slow, 4),
                "crossover_strength": round(crossover_strength, 2)
            }

        # === Neutral Output ===
        logger.info(f"⚪ [AdaptiveTrend] No clear early trend detected → RSI: {current_rsi:.2f}, Slope: {slope:.4f}")
        return None

    except Exception as e:
        logger.error(f"❌ [AdaptiveTrend Critical Error]: {e}")
        return None
