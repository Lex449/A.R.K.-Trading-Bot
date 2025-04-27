"""
A.R.K. Volume Spike Detector – Detects abnormal volume activity.
"""

def detect_volume_spike(df, volume_multiplier=1.5):
    """
    Detects abnormal volume spikes.
    Args:
        df (DataFrame): Market data.
        volume_multiplier (float): Factor over average volume to trigger.

    Returns:
        dict or None
    """
    if df is None or df.empty or "volume" not in df.columns:
        return None

    avg_volume = df["volume"].iloc[-20:].mean()
    latest_volume = df["volume"].iloc[-1]

    if latest_volume >= avg_volume * volume_multiplier:
        return {
            "volume_percent": (latest_volume / avg_volume) * 100
        }

    return None
