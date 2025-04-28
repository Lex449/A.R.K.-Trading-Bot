"""
A.R.K. Move Detector – Premium Ultra Build.
Detects strong price movements based on 1-Minute candles.
"""

import pandas as pd

def detect_move(df: pd.DataFrame, move_threshold_percent: float = 1.5) -> dict:
    """
    Detects strong intraday moves based on candle body movement.

    Args:
        df (pd.DataFrame): Market OHLCV data.
        move_threshold_percent (float): Minimum move % to trigger (default: 1.5%).

    Returns:
        dict or None: Move detection result or None if no strong move detected.
    """

    if df is None or df.empty or not all(col in df.columns for col in ['o', 'c']):
        return None

    try:
        latest_open = df['o'].iloc[-1]
        latest_close = df['c'].iloc[-1]

        if latest_open == 0:
            return None  # Safety check

        move_percent = ((latest_close - latest_open) / latest_open) * 100

        if abs(move_percent) >= move_threshold_percent:
            return {
                "move_percent": round(move_percent, 2),
                "direction": "long" if move_percent > 0 else "short"
            }

        return None

    except Exception:
        return None
