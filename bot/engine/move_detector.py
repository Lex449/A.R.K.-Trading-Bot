"""
A.R.K. Move Detector – Detects strong price movements.
"""

def detect_move(df, move_threshold_percent=1.5):
    """
    Detects strong moves based on 1-Minute candles.
    Args:
        df (DataFrame): Market data.
        move_threshold_percent (float): Minimum move % to trigger.

    Returns:
        dict or None
    """
    if df is None or df.empty:
        return None

    latest = df.iloc[-1]
    move = (latest["close"] - latest["open"]) / latest["open"] * 100

    if abs(move) >= move_threshold_percent:
        return {
            "move_percent": move,
            "direction": "long" if move > 0 else "short"
        }

    return None
