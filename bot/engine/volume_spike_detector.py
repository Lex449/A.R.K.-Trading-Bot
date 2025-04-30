"""
A.R.K. Volume Spike Detector – Hyper Adaptive Intelligence 3.2
Detects Market Breakouts via Real-Time Volume Surges with Dynamic Baseline Calibration.

Made in Bali. Engineered with German Precision.
"""

import pandas as pd
from bot.utils.logger import setup_logger

logger = setup_logger(__name__)

def detect_volume_spike(df: pd.DataFrame, window: int = 30, multiplier: float = 1.3) -> dict | None:
    """
    Detects real-time volume anomalies via short-term surges over a rolling baseline.

    Args:
        df (pd.DataFrame): Candlestick DataFrame incl. 'v' (volume).
        window (int): Lookback for rolling average.
        multiplier (float): Trigger factor for spike.

    Returns:
        dict or None: Details of spike if detected.
    """
    if df is None or df.empty or "v" not in df.columns:
        logger.warning("⚠️ [VolumeSpike] Invalid DataFrame or missing volume column.")
        return None

    try:
        base_avg = df["v"].rolling(window=window, min_periods=window // 2).mean().iloc[-1]
        recent_avg = df["v"].tail(3).mean()
        recent_med = df["v"].tail(3).median()

        if base_avg <= 0 or recent_avg <= 0:
            logger.warning("⚠️ [VolumeSpike] Non-positive averages detected.")
            return None

        spike_ratio = recent_avg / base_avg
        if spike_ratio >= multiplier:
            percent = round((spike_ratio - 1) * 100, 2)
            strength = _classify_spike_strength(percent)

            logger.info(
                f"🚨 [VolumeSpike] Volume Surge Detected: +{percent:.2f}% "
                f"({int(base_avg)} → {int(recent_avg)}) → {strength}"
            )

            return {
                "volume_spike": True,
                "rolling_volume_avg": int(base_avg),
                "recent_volume_avg": int(recent_avg),
                "recent_volume_median": int(recent_med),
                "volume_increase_percent": percent,
                "spike_strength": strength
            }

        logger.info(f"🔍 [VolumeSpike] No spike detected (Ratio: {spike_ratio:.2f})")
        return None

    except Exception as e:
        logger.error(f"❌ [VolumeSpike] Critical Failure: {e}")
        return None

def _classify_spike_strength(percent: float) -> str:
    """
    Classifies volume spike magnitude for signal rating.

    Args:
        percent (float): Percent above base average.

    Returns:
        str: Descriptive spike tag.
    """
    if percent >= 200:
        return "Explosive Spike 🔥🔥"
    elif percent >= 120:
        return "Strong Spike ⚡"
    elif percent >= 60:
        return "Moderate Spike ⚠️"
    elif percent >= 30:
        return "Light Spike ⚪"
    return "Minor Uptick"
