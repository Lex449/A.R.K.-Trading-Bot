"""
A.R.K. Move Alert Engine – Ultra Real-Time Movement Analysis.
Monitors strong market moves on 1-minute intervals.
"""

import pandas as pd

async def detect_move_alert(df: pd.DataFrame) -> dict:
    """
    Analyzes recent candles for sudden market moves.

    Args:
        df (pd.DataFrame): Candle data with columns ['o', 'h', 'l', 'c'].

    Returns:
        dict or None: Move alert details or None if no significant move detected.
    """
    if df is None or df.empty or len(df) < 2:
        return None

    try:
        last_close = df.iloc[-1]["c"]
        prev_close = df.iloc[-2]["c"]

        if prev_close == 0:
            return None  # Prevent division by zero

        move_percent = ((last_close - prev_close) / prev_close) * 100

        if abs(move_percent) >= 2.5:
            # Strong move detected
            return {
                "type": "full",
                "move_percent": round(move_percent, 2),
            }
        elif abs(move_percent) >= 2.0:
            # Early warning detected
            return {
                "type": "warning",
                "move_percent": round(move_percent, 2),
            }
        else:
            return None

    except Exception:
        return None
