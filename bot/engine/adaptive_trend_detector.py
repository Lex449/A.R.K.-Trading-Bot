"""
A.R.K. Adaptive Trend Detector – Ultra Premium Early Reversal Scanner
Detects micro-trend shifts using RSI dynamics and short-term slope analysis.
Engineered for: Precision Trend Forecasting & Front-Running Major Moves.
"""

import pandas as pd
import numpy as np
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

def detect_trend_shift(df: pd.DataFrame, rsi_period: int = 14, slope_window: int = 5) -> dict:
    """
    Detects early signals of a trend reversal based on RSI momentum and slope dynamics.

    Args:
        df (pd.DataFrame): DataFrame with 'c' (close price) column.
        rsi_period (int): Lookback period for RSI (default 14).
        slope_window (int): Candles to calculate price slope (default 5).

    Returns:
        dict or None: Early trend information if detected.
    """
    if df is None or df.empty or "c" not in df.columns:
        logger.warning("⚠️ [Adaptive Trend Detector] Missing or invalid candle data.")
        return None

    try:
        # === Calculate RSI ===
        close_delta = df["c"].diff()
        gain = np.where(close_delta > 0, close_delta, 0)
        loss = np.where(close_delta < 0, -close_delta, 0)

        avg_gain = pd.Series(gain).rolling(window=rsi_period, min_periods=1).mean()
        avg_loss = pd.Series(loss).rolling(window=rsi_period, min_periods=1).mean()

        rs = avg_gain / (avg_loss + 1e-9)  # Prevent division by zero
        rsi = 100 - (100 / (1 + rs))

        # === Calculate Price Slope ===
        recent_prices = df["c"].tail(slope_window)
        x = np.arange(len(recent_prices))
        slope = np.polyfit(x, recent_prices, 1)[0]

        current_rsi = rsi.iloc[-1]

        # === Define Early Reversal Conditions ===
        if slope > 0 and 50 < current_rsi < 65:
            logger.info(f"📈 [Trend Detector] Bullish reversal signal detected: RSI {current_rsi:.2f}, Slope {slope:.5f}")
            return {
                "early_trend": "bullish",
                "rsi": round(current_rsi, 2),
                "slope": round(slope, 5)
            }
        elif slope < 0 and 35 < current_rsi < 50:
            logger.info(f"📉 [Trend Detector] Bearish reversal signal detected: RSI {current_rsi:.2f}, Slope {slope:.5f}")
            return {
                "early_trend": "bearish",
                "rsi": round(current_rsi, 2),
                "slope": round(slope, 5)
            }

        return None

    except Exception as e:
        logger.error(f"❌ [Adaptive Trend Detector] Fatal error during detection: {e}")
        return None
