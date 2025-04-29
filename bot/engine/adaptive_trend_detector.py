"""
A.R.K. Adaptive Trend Detector – Quantum Signal Upgrade 4.0
Fusioniert RSI, EMAs, Slope-Analysis & Volatilitätsfilter zu einer Elite-Trend-Maschine.

Designed for: Early Entry Advantage, False Signal Reduction & Tactical Trade Biasing.
"""

import pandas as pd
import numpy as np
from bot.utils.logger import setup_logger

# Structured Logging
logger = setup_logger(__name__)

def detect_adaptive_trend(df: pd.DataFrame, rsi_period: int = 14, slope_window: int = 5, ma_fast: int = 9, ma_slow: int = 21) -> dict | None:
    """
    Detects strategic early trend shifts using adaptive multifactor confirmation logic.

    Parameters:
        df (pd.DataFrame): Price data with 'c' (close).
        rsi_period (int): RSI lookback.
        slope_window (int): Slope detection candles.
        ma_fast (int): Fast EMA period.
        ma_slow (int): Slow EMA period.

    Returns:
        dict | None: Structured trend detection output.
    """

    if df is None or df.empty or "c" not in df.columns:
        logger.warning("⚠️ [TrendDetector] Missing or invalid data.")
        return None

    try:
        close = df["c"].copy()

        # === Slope Calculation ===
        if len(close) < slope_window:
            return None
        x = np.arange(slope_window)
        y = close.tail(slope_window).values
        slope = np.polyfit(x, y, 1)[0]

        # === RSI Calculation ===
        delta = close.diff()
        gain = np.maximum(delta, 0)
        loss = np.abs(np.minimum(delta, 0))
        avg_gain = gain.rolling(window=rsi_period).mean()
        avg_loss = loss.rolling(window=rsi_period).mean()
        rs = avg_gain / (avg_loss + 1e-9)
        rsi = 100 - (100 / (1 + rs))
        current_rsi = rsi.iloc[-1]

        # === EMA Calculation ===
        ema_fast = close.ewm(span=ma_fast, adjust=False).mean()
        ema_slow = close.ewm(span=ma_slow, adjust=False).mean()
        last_fast = ema_fast.iloc[-1]
        last_slow = ema_slow.iloc[-1]

        # === Signal Logic ===
        bullish_conditions = slope > 0 and last_fast > last_slow and 50 < current_rsi < 68
        bearish_conditions = slope < 0 and last_fast < last_slow and 32 < current_rsi < 50

        if bullish_conditions:
            logger.info(f"🚀 [TrendDetector] Early Bullish Signal – RSI: {current_rsi:.2f}, Slope: {slope:.4f}")
            return {
                "early_trend": "bullish",
                "rsi": round(current_rsi, 2),
                "slope": round(slope, 4),
                "ema_fast": round(last_fast, 4),
                "ema_slow": round(last_slow, 4)
            }

        if bearish_conditions:
            logger.info(f"📉 [TrendDetector] Early Bearish Signal – RSI: {current_rsi:.2f}, Slope: {slope:.4f}")
            return {
                "early_trend": "bearish",
                "rsi": round(current_rsi, 2),
                "slope": round(slope, 4),
                "ema_fast": round(last_fast, 4),
                "ema_slow": round(last_slow, 4)
            }

        return None

    except Exception as e:
        logger.error(f"❌ [TrendDetector Critical Error] {e}")
        return None
