"""
A.R.K. Volatility Guard – Ultra Adaptive Smart Filtering Engine 3.0
Dynamic Signal Adjustment based on Live Volatility.
"""

import statistics

def is_market_high_volatility(candles: list[dict]) -> bool:
    """
    Detects if the market is experiencing a high-volatility phase.

    Args:
        candles (list[dict]): List of recent candles with 'high' and 'low' values.

    Returns:
        bool: True if high volatility is detected, otherwise False.
    """

    if not candles or len(candles) < 10:
        return False  # Not enough data to determine

    try:
        ranges = [
            ((candle["high"] - candle["low"]) / candle["low"]) * 100
            for candle in candles[-10:]
            if candle.get("high") and candle.get("low") and candle["high"] > candle["low"]
        ]

        if not ranges:
            return False

        avg_volatility = statistics.mean(ranges)
        std_dev_volatility = statistics.stdev(ranges) if len(ranges) > 1 else 0

        # Smart threshold logic: if average or volatility deviation is high
        return avg_volatility > 1.2 or std_dev_volatility > 0.6

    except Exception:
        return False

def adjust_signal_quality(confidence: float, high_volatility: bool) -> float:
    """
    Adjusts the confidence score dynamically based on market volatility.

    Args:
        confidence (float): Original confidence value.
        high_volatility (bool): True if the market is volatile.

    Returns:
        float: Adjusted confidence score, bounded between 0 and 100.
    """

    try:
        if high_volatility:
            adjusted = confidence * 0.85  # Reduce in high-risk phases
        else:
            adjusted = confidence * 1.07  # Boost slightly in stable phases

        return round(max(0.0, min(adjusted, 100.0)), 2)

    except Exception:
        return confidence
