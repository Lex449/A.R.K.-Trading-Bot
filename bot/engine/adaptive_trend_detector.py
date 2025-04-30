"""
A.R.K. Adaptive Trend Detector – Ultra Flexible Signal Engine 6.1
Detects Pre-Trend Bias Using RSI, EMA Cross, Slope and Volatility Dynamics.

Engineered for: Early Signal Generation, Reduced Filter Rigidity, Smarter Breakout Readiness.
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
    Detects early directional bias using smoothed slope, RSI range, EMA cross distance and recent candle dynamics.
    """

    if df is None or df.empty or "c" not in df.columns or len(df) < max(rsi_period, slope_window, ma_slow):
        logger.warning("⚠️ [AdaptiveTrend] Data invalid or insufficient.")
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

        # === EMA Crossover ===
        ema_fast = close.ewm(span=ma_fast, adjust=False).mean()
        ema_slow = close.ewm(span=ma_slow, adjust=False).mean()
        last_fast = ema_fast.iloc[-1]
        last_slow = ema_slow.iloc[-1]
        crossover_strength = abs(last_fast - last_slow) / close.iloc[-1] * 100

        # === More Adaptive Thresholds ===
        rsi_bullish_zone = 48 < current_rsi < 70
        rsi_bearish_zone = 30 < current_rsi < 52

        is_bullish = slope > 0 and last_fast > last_slow and rsi_bullish_zone
        is_bearish = slope < 0 and last_fast < last_slow and rsi_bearish_zone

        if is_bullish:
            logger.info(f"🚀 [AdaptiveTrend] Bullish → RSI: {current_rsi:.2f}, Slope: {slope:.4f}, Cross: {crossover_strength:.2f}%")
            return {
                "early_trend": "bullish",
                "rsi": round(current_rsi, 2),
                "slope": round(slope, 4),
                "ema_fast": round(last_fast, 4),
                "ema_slow": round(last_slow, 4),
                "crossover_strength": round(crossover_strength, 2)
            }

        if is_bearish:
            logger.info(f"📉 [AdaptiveTrend] Bearish → RSI: {current_rsi:.2f}, Slope: {slope:.4f}, Cross: {crossover_strength:.2f}%")
            return {
                "early_trend": "bearish",
                "rsi": round(current_rsi, 2),
                "slope": round(slope, 4),
                "ema_fast": round(last_fast, 4),
                "ema_slow": round(last_slow, 4),
                "crossover_strength": round(crossover_strength, 2)
            }

        logger.info(f"⚪ [AdaptiveTrend] No trend → RSI: {current_rsi:.2f}, Slope: {slope:.4f}")
        return None

    except Exception as e:
        logger.error(f"❌ [AdaptiveTrend] Error: {e}")
        return None
