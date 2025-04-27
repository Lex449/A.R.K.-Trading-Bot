"""
A.R.K. Volume Spike Detector – Ultra Precision Build.
Detects real-time volume surges with intelligent safety checks.
"""

import pandas as pd

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
        return None

    try:
        # Calculate rolling average volume (last 20 candles)
        avg_volume = df["v"].rolling(window=20, min_periods=1).mean().iloc[-1]
        current_volume = df["v"].iloc[-1]

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
        # Fail silently and clean
        return None
