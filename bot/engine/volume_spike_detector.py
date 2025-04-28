"""
A.R.K. Volume Spike Detector – Ultra Masterclass Build.
Detects real-time smart volume surges with adaptive thresholding.
"""

import pandas as pd
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

def detect_volume_spike(df: pd.DataFrame, window: int = 30, multiplier: float = 1.4) -> dict:
    """
    Detects meaningful volume spikes based on dynamic average.

    Args:
        df (pd.DataFrame): DataFrame with 'v' (volume) column.
        window (int): Rolling window size (default 30 candles).
        multiplier (float): Spike multiplier threshold (default 1.4x).

    Returns:
        dict or None
    """
    if df is None or df.empty or "v" not in df.columns:
        logger.warning("⚠️ [Volume Spike] Invalid or missing DataFrame input.")
        return None

    try:
        avg_volume = df["v"].rolling(window=window, min_periods=10).mean().iloc[-1]
        recent_volumes = df["v"].tail(3)

        if avg_volume == 0:
            logger.warning("⚠️ [Volume Spike] Zero average volume, skipping detection.")
            return None

        # New logic: compare last 3 candles' average to rolling average
        recent_avg = recent_volumes.mean()

        if recent_avg >= avg_volume * multiplier:
            volume_percent = (recent_avg / avg_volume) * 100

            return {
                "volume_spike": True,
                "recent_volume_avg": int(recent_avg),
                "rolling_volume_avg": int(avg_volume),
                "volume_percent": round(volume_percent, 2)
            }

        return None

    except Exception as e:
        logger.error(f"❌ [Volume Spike] Critical detection error: {e}")
        return None
