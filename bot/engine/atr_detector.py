"""
A.R.K. ATR Detector – Detects significant True Range breakout candles.
Ultra Premium Build – für smartere Volatilitäts- und Risikoerkennung.
"""

import pandas as pd

def detect_atr_breakout(df: pd.DataFrame, atr_multiplier: float = 1.5) -> dict:
    """
    Detects ATR-based breakouts indicating high volatility.

    Args:
        df (pd.DataFrame): OHLCV DataFrame with 'high', 'low', 'close' columns.
        atr_multiplier (float): Multiplier threshold for breakout detection.

    Returns:
        dict or None: Breakout details if detected, else None.
    """
    if df is None or df.empty or not {"high", "low", "close"}.issubset(df.columns):
        return None

    try:
        # Calculate True Range (TR)
        df["tr"] = df[["high", "close"]].max(axis=1) - df[["low", "close"]].min(axis=1)

        # Calculate 14-period ATR (Average True Range)
        atr = df["tr"].rolling(window=14, min_periods=1).mean().iloc[-1]
        latest_tr = df["tr"].iloc[-1]

        # Detect breakout
        if latest_tr >= atr * atr_multiplier:
            return {
                "atr_breakout": True,
                "atr_ratio_percent": round((latest_tr / atr) * 100, 2),
                "atr_value": round(atr, 4)
            }
        else:
            return None

    except Exception:
        return None
