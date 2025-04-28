"""
A.R.K. Signal Rating Improvement – Scoring and Quality Control System.
Rates trading signals dynamically based on pattern quality, volatility, and momentum.
"""

def rate_signal(patterns: list, volatility_info: dict, trend_info: dict = None) -> int:
    """
    Calculates a dynamic signal rating between 0 and 100.

    Args:
        patterns (list): Detected patterns.
        volatility_info (dict): Volatility analysis result.
        trend_info (dict, optional): Early trend detection result.

    Returns:
        int: Signal rating score.
    """
    if not patterns:
        return 0

    try:
        score = 0

        # === Pattern Strength ===
        for p in patterns:
            if "⭐⭐⭐⭐⭐" in p:
                score += 30
            elif "⭐⭐⭐⭐" in p:
                score += 20
            elif "⭐⭐⭐" in p:
                score += 10

        # === Volatility Bonus ===
        if volatility_info and volatility_info.get("volatility_spike"):
            score += 20

        # === Trend Bonus ===
        if trend_info:
            if trend_info.get("early_trend") == "bullish":
                score += 15
            elif trend_info.get("early_trend") == "bearish":
                score += 15

        # === Score Capping ===
        score = min(score, 100)

        return score

    except Exception:
        return 0
