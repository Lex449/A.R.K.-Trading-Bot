"""
A.R.K. Adaptive Trend Detector – Frühwarnsystem für Trendwechsel
Detects early trend shifts using multi-timeframe RSI and price slope analysis.
"""

import pandas as pd
import numpy as np
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

def detect_trend_shift(df: pd.DataFrame, rsi_period: int = 14, slope_window: int = 5) -> dict:
    """
    Detects potential early trend changes using RSI and price slope.

    Args:
        df (pd.DataFrame): DataFrame with 'c' (close price) column.
        rsi_period (int): RSI calculation period (default 14).
        slope_window (int): Price slope window (default 5 candles).

    Returns:
        dict or None
    """
    if df is None or df.empty or "c" not in df.columns:
        logger.warning("⚠️ [Trend Detector] Invalid or missing DataFrame input.")
        return None

    try:
        # === Calculate RSI ===
        delta = df["c"].diff()
        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)

        avg_gain = pd.Series(gain).rolling(window=rsi_period, min_periods=1).mean()
        avg_loss = pd.Series(loss).rolling(window=rsi_period, min_periods=1).mean()

        rs = avg_gain / (avg_loss + 1e-9)  # avoid division by zero
        rsi = 100 - (100 / (1 + rs))

        # === Calculate Price Slope ===
        y = df["c"].tail(slope_window)
        x = np.arange(len(y))
        slope = np.polyfit(x, y, 1)[0]  # first degree polynomial slope

        current_rsi = rsi.iloc[-1]

        # === Early Trend Change Conditions ===
        if slope > 0 and current_rsi > 50 and current_rsi < 65:
            return {
                "early_trend": "bullish",
                "rsi": round(current_rsi, 2),
                "slope": round(slope, 5)
            }
        elif slope < 0 and current_rsi < 50 and current_rsi > 35:
            return {
                "early_trend": "bearish",
                "rsi": round(current_rsi, 2),
                "slope": round(slope, 5)
            }

        return None

    except Exception as e:
        logger.error(f"❌ [Trend Detector] Critical detection error: {e}")
        return None
