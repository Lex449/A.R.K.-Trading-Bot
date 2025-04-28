# bot/engine/volume_spike_detector.py

"""
A.R.K. Volume Spike Detector – Ultra Precision Build.
Detects real-time volume surges with intelligent safety checks.
"""

import pandas as pd
import logging
from bot.utils.logger import setup_logger

# Setup Logger
logger = setup_logger(__name__)

def detect_volume_spike(df: pd.DataFrame, multiplier: float = 1.5) -> dict:
    """
    Detects a volume spike if current volume significantly exceeds rolling average.

    Args:
        df (pd.DataFrame): Market OHLCV data (must include 'v' column for volume).
        multiplier (float): How much above average volume triggers a spike (default 1.5x).

    Returns:
        dict or None: Spike details or None if no spike.
    """
    if df is None or df.empty or "v" not in df.columns:
        logger.warning("⚠️ [Volume Spike Detector] Missing or invalid DataFrame input.")
        return None

    try:
        # Calculate rolling average volume (last 20 candles)
        avg_volume = df["v"].rolling(window=20, min_periods=1).mean().iloc[-1]
        current_volume = df["v"].iloc[-1]

        if avg_volume == 0:
            logger.warning("⚠️ [Volume Spike Detector] Average volume is zero. Skipping detection.")
            return None

        # Check for spike
        if current_volume >= avg_volume * multiplier:
            volume_percent = (current_volume / avg_volume) * 100
            return {
                "volume_spike": True,
                "current_volume": int(current_volume),
                "average_volume": int(avg_volume),
                "volume_percent": round(volume_percent, 2)
            }

        return None

    except Exception as e:
        logger.error(f"❌ [Volume Spike Detector] Unexpected error: {e}")
        return None
