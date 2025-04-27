"""
A.R.K. Volatility Detector – Detects High Volatility Events in Real-Time.
Core component for smarter trading signals and risk assessment.
"""

import pandas as pd
import numpy as np

def detect_volatility_spike(df: pd.DataFrame, threshold: float = 1.8) -> dict:
    """
    Detects significant volatility spikes based on ATR and standard deviation.

    Args:
        df (pd.DataFrame): OHLCV DataFrame.
        threshold (float): Multiplier for what counts as "high volatility".

    Returns:
        dict or None: Volatility event details or None if no spike detected.
    """
    if df is None or df.empty:
        return None

    try:
        # Calculate True Range
        df["high_low"] = df["h"] - df["l"]
        df["high_close"] = np.abs(df["h"] - df["c"].shift())
        df["low_close"] = np.abs(df["l"] - df["c"].shift())
        df["true_range"] = df[["high_low", "high_close", "low_close"]].max(axis=1)

        # Calculate ATR (14 periods)
        df["atr"] = df["true_range"].rolling(window=14, min_periods=1).mean()

        # Calculate percentage movement per candle
        df["pct_change"] = df["c"].pct_change().abs() * 100

        # Calculate average move size
        avg_move = df["pct_change"].rolling(window=14, min_periods=1).mean().iloc[-1]
        current_move = df["pct_change"].iloc[-1]

        # Calculate volatility spike
        if current_move > avg_move * threshold:
            return {
                "volatility_spike": True,
                "current_move": current_move,
                "average_move": avg_move,
                "atr": df["atr"].iloc[-1]
            }

        return None

    except Exception as e:
        return None
