"""
A.R.K. Volume Spike Detector – Ultra Precision 3.0
Smart, Adaptive Volume Surge Recognition for Elite Trading.

Engineered for: Real-Time Detection, Dynamic Environments, Multilingual Safety Logging.
"""

import pandas as pd
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

def detect_volume_spike(df: pd.DataFrame, window: int = 30, multiplier: float = 1.4) -> dict | None:
    """
    Detects significant volume spikes based on dynamic rolling averages.

    Args:
        df (pd.DataFrame): DataFrame containing 'v' (volume) column.
        window (int): Rolling window size for average calculation (default: 30 candles).
        multiplier (float): Threshold multiplier to define a spike (default: 1.4x).

    Returns:
        dict or None: Detailed spike information or None if no spike detected.
    """

    if df is None or df.empty or "v" not in df.columns:
        logger.warning("⚠️ [VolumeSpikeDetector] Invalid DataFrame input – volume column missing.")
        return None

    try:
        # === Rolling Average Volume ===
        avg_volume = df["v"].rolling(window=window, min_periods=10).mean().iloc[-1]
        recent_volumes = df["v"].tail(3)
        recent_avg_volume = recent_volumes.mean()

        if avg_volume == 0:
            logger.warning("⚠️ [VolumeSpikeDetector] Zero average volume detected. Spike detection skipped.")
            return None

        # === Spike Detection Logic ===
        if recent_avg_volume >= avg_volume * multiplier:
            volume_spike_percent = (recent_avg_volume / avg_volume) * 100

            logger.info(f"✅ [VolumeSpikeDetector] Volume spike detected: {volume_spike_percent:.2f}% over average.")

            return {
                "volume_spike": True,
                "recent_volume_avg": int(recent_avg_volume),
                "rolling_volume_avg": int(avg_volume),
                "volume_percent": round(volume_spike_percent, 2)
            }

        return None

    except Exception as e:
        logger.error(f"❌ [VolumeSpikeDetector Critical Error] {e}")
        return None
