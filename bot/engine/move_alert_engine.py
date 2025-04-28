"""
A.R.K. Move Alert Engine – Ultra Precision 3.0
Real-Time Monitoring of Micro and Macro Market Movements.

Built for: Extreme Speed, Fault Tolerance, and High-Accuracy Volatility Detection.
"""

import pandas as pd

async def detect_move_alert(df: pd.DataFrame) -> dict | None:
    """
    Detects sudden market moves based on 1-minute candle changes.

    Args:
        df (pd.DataFrame): DataFrame with columns ['o', 'h', 'l', 'c'] (open, high, low, close).

    Returns:
        dict or None: Move alert details if threshold exceeded, otherwise None.
    """

    if df is None or df.empty or len(df) < 2:
        return None  # Not enough data to detect move

    try:
        last_close = df["c"].iloc[-1]
        prev_close = df["c"].iloc[-2]

        if prev_close == 0:
            return None  # Protect against division by zero

        move_percent = round(((last_close - prev_close) / prev_close) * 100, 2)

        if abs(move_percent) >= 2.5:
            # Full Move Detected (Strong Breakout)
            return {
                "type": "full",
                "move_percent": move_percent,
            }
        elif abs(move_percent) >= 2.0:
            # Early Move Warning (Watchlist Candidate)
            return {
                "type": "warning",
                "move_percent": move_percent,
            }
        else:
            return None  # No meaningful movement detected

    except Exception:
        # Safe fallback in case of data error
        return None
