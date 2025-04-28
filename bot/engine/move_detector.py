"""
A.R.K. Move Detector – Ultra Premium 3.0
Smart Intraday Move Recognition based on 1-Min Candle Analysis.

Engineered for: Precision, Safety, Scalability.
"""

import pandas as pd

def detect_move(df: pd.DataFrame, move_threshold_percent: float = 1.5) -> dict | None:
    """
    Detects strong 1-minute candle-based price moves.

    Args:
        df (pd.DataFrame): OHLCV DataFrame with 'o' (open) and 'c' (close) columns.
        move_threshold_percent (float): Minimum move % required to trigger detection (default: 1.5%).

    Returns:
        dict: {move_percent: float, direction: "long" or "short"} if move detected,
        None otherwise.
    """
    if df is None or df.empty or not all(col in df.columns for col in ["o", "c"]):
        return None

    try:
        latest_open = df["o"].iloc[-1]
        latest_close = df["c"].iloc[-1]

        if latest_open == 0:
            return None  # Guard: Prevent division by zero

        move_percent = ((latest_close - latest_open) / latest_open) * 100

        if abs(move_percent) >= move_threshold_percent:
            direction = "long" if move_percent > 0 else "short"

            return {
                "move_percent": round(move_percent, 2),
                "direction": direction
            }

        return None

    except Exception as e:
        # Critical error catch
        print(f"[MoveDetector Error] {e}")
        return None
