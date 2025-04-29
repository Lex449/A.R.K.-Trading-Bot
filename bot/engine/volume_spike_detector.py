"""
A.R.K. Volume Spike Detector – Ultra Adaptive Intelligence 3.0
Precision Detection of Dynamic Volume Surges for Elite Signal Enhancement.

Built for: Instant Breakout Warning, Scalable Use Across Assets, Multilingual Ultra Stability.
"""

import pandas as pd
from bot.utils.logger import setup_logger

# === Setup structured logger ===
logger = setup_logger(__name__)

def detect_volume_spike(df: pd.DataFrame, window: int = 30, multiplier: float = 1.5) -> dict | None:
    """
    Detects highly dynamic volume spikes based on rolling averages and short-term surges.

    Args:
        df (pd.DataFrame): DataFrame containing 'v' (volume) column.
        window (int): Rolling window size for base volume (default: 30 candles).
        multiplier (float): Threshold multiplier for surge detection (default: 1.5x).

    Returns:
        dict or None: Spike event data or None if no event detected.
    """
    if df is None or df.empty or "v" not in df.columns:
        logger.warning("⚠️ [Volume Spike Detector] DataFrame invalid: missing volume column.")
        return None

    try:
        # === Rolling Average (Base Volume) ===
        rolling_avg_volume = df["v"].rolling(window=window, min_periods=max(10, window//2)).mean().iloc[-1]
        recent_volumes = df["v"].tail(3)
        recent_avg_volume = recent_volumes.mean()

        # === Spike Detection Logic ===
        if rolling_avg_volume <= 0:
            logger.warning("⚠️ [Volume Spike Detector] Rolling average volume zero. Spike detection aborted.")
            return None

        spike_factor = recent_avg_volume / rolling_avg_volume

        if spike_factor >= multiplier:
            spike_strength = round((spike_factor - 1) * 100, 2)

            logger.info(f"🚀 [Volume Spike Detector] Spike detected: +{spike_strength:.2f}% over rolling average.")

            return {
                "volume_spike": True,
                "recent_volume_avg": int(recent_avg_volume),
                "rolling_volume_avg": int(rolling_avg_volume),
                "volume_increase_percent": spike_strength,
                "spike_strength": _classify_spike_strength(spike_strength)
            }

        return None

    except Exception as e:
        logger.error(f"❌ [Volume Spike Detector] Critical failure: {e}")
        return None

# === Internal Spike Classifier ===
def _classify_spike_strength(percent: float) -> str:
    """
    Classifies the strength of the detected volume spike.

    Args:
        percent (float): Percent increase over the average.

    Returns:
        str: Classification label.
    """
    if percent >= 150:
        return "Ultra Spike 🔥"
    elif percent >= 100:
        return "Strong Spike ⚡"
    elif percent >= 50:
        return "Moderate Spike ⚡"
    else:
        return "Mild Spike ⚪"
