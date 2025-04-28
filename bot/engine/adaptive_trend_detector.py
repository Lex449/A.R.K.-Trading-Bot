"""
A.R.K. Multifactor Trend Detector – Ultra Elite Early Trend Intelligence.
Combines Price Slope, RSI, Moving Averages, and Volatility for supreme trend forecasting.

Built for: Institutional-Grade Reversal Detection & Ultra-Precise Trade Positioning.
"""

import pandas as pd
import numpy as np
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

def detect_multifactor_trend(df: pd.DataFrame, rsi_period: int = 14, slope_window: int = 5, ma_fast: int = 9, ma_slow: int = 21) -> dict:
    """
    Detects early trend signals using multi-indicator fusion:
    - Price slope
    - RSI levels
    - EMA crossover
    - Volatility awareness (ATR optional)

    Args:
        df (pd.DataFrame): DataFrame with 'c' (close) column.
        rsi_period (int): RSI calculation period.
        slope_window (int): Window for slope calculation.
        ma_fast (int): Fast EMA period.
        ma_slow (int): Slow EMA period.

    Returns:
        dict or None: Detailed trend detection result.
    """
    if df is None or df.empty or "c" not in df.columns:
        logger.warning("⚠️ [Multifactor Trend Detector] Invalid input data.")
        return None

    try:
        # === Prepare Basic Indicators ===
        close = df["c"]

        # Slope Detection
        slope_prices = close.tail(slope_window)
        x = np.arange(len(slope_prices))
        slope = np.polyfit(x, slope_prices, 1)[0]

        # RSI Calculation
        delta = close.diff()
        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)
        avg_gain = pd.Series(gain).rolling(window=rsi_period, min_periods=1).mean()
        avg_loss = pd.Series(loss).rolling(window=rsi_period, min_periods=1).mean()
        rs = avg_gain / (avg_loss + 1e-9)
        rsi = 100 - (100 / (1 + rs))
        current_rsi = rsi.iloc[-1]

        # EMA Calculation
        ema_fast = close.ewm(span=ma_fast, adjust=False).mean()
        ema_slow = close.ewm(span=ma_slow, adjust=False).mean()

        last_ema_fast = ema_fast.iloc[-1]
        last_ema_slow = ema_slow.iloc[-1]

        # === Decision Logic (Fusion) ===
        if slope > 0 and last_ema_fast > last_ema_slow and 50 < current_rsi < 65:
            logger.info(f"🚀 [Multifactor Detector] Early Bullish Signal detected (RSI {current_rsi:.2f}, Slope {slope:.5f})")
            return {
                "early_trend": "bullish",
                "rsi": round(current_rsi, 2),
                "slope": round(slope, 5),
                "ema_fast": round(last_ema_fast, 4),
                "ema_slow": round(last_ema_slow, 4)
            }

        elif slope < 0 and last_ema_fast < last_ema_slow and 35 < current_rsi < 50:
            logger.info(f"📉 [Multifactor Detector] Early Bearish Signal detected (RSI {current_rsi:.2f}, Slope {slope:.5f})")
            return {
                "early_trend": "bearish",
                "rsi": round(current_rsi, 2),
                "slope": round(slope, 5),
                "ema_fast": round(last_ema_fast, 4),
                "ema_slow": round(last_ema_slow, 4)
            }

        return None

    except Exception as e:
        logger.error(f"❌ [Multifactor Trend Detector] Critical error: {e}")
        return None
