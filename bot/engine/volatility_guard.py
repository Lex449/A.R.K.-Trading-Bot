"""
A.R.K. Volatility Guard – Smart Signal Filtering based on Live Market Conditions.
Improves signal quality by dynamically adapting sensitivity.
"""

import statistics

def is_market_high_volatility(candles: list) -> bool:
    """
    Detects if the market is currently in a high volatility phase.

    Args:
        candles (list): List of recent candle dictionaries with 'high', 'low' keys.

    Returns:
        bool: True if high volatility detected, else False.
    """
    if len(candles) < 10:
        return False  # Not enough data to judge volatility

    # Calculate % range for each candle
    ranges = []
    for candle in candles[-10:]:  # Last 10 candles
        high = candle.get("high")
        low = candle.get("low")
        if high and low and high > low:
            range_percent = ((high - low) / low) * 100
            ranges.append(range_percent)

    # Check average volatility
    if not ranges:
        return False

    avg_volatility = statistics.mean(ranges)

    # Threshold: If >1.2% on average → high volatility
    return avg_volatility > 1.2

def adjust_signal_quality(confidence: float, high_volatility: bool) -> float:
    """
    Dynamically adjusts signal confidence based on volatility.

    Args:
        confidence (float): Original confidence score.
        high_volatility (bool): Whether market is volatile.

    Returns:
        float: Adjusted confidence score.
    """
    if high_volatility:
        return confidence * 0.85  # Decrease quality slightly (riskier environment)
    else:
        return confidence * 1.05  # Boost slighty (calmer market)
