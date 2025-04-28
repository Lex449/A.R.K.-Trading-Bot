"""
A.R.K. Signal Rater – Ultra Precision 3.0
Scores signals dynamically based on pattern strength, volatility conditions, and early trend detection.

Designed for: Flawless Signal Quality Control, Risk-Adaptive Trading, Professional Scalability.
"""

def rate_signal(patterns: list, volatility_info: dict = None, trend_info: dict = None) -> int:
    """
    Dynamically calculates a premium signal rating between 0 and 100.

    Args:
        patterns (list): List of detected patterns.
        volatility_info (dict, optional): Volatility detection output.
        trend_info (dict, optional): Early trend detection output.

    Returns:
        int: Signal quality score (0–100).
    """
    if not patterns or not isinstance(patterns, list):
        return 0

    try:
        score = 0

        # === 1. Pattern Strength Weighting ===
        for p in patterns:
            stars = p.count("⭐")
            if stars >= 5:
                score += 30
            elif stars == 4:
                score += 20
            elif stars == 3:
                score += 10
            elif stars == 2:
                score += 5

        # === 2. Volatility Bonus (High Risk-Reward Phase) ===
        if volatility_info and volatility_info.get("volatility_spike"):
            score += 20

        # === 3. Trend Alignment Bonus ===
        if trend_info:
            early_trend = trend_info.get("early_trend", "").lower()
            if early_trend in ["bullish", "bearish"]:
                score += 15

        # === 4. Dynamic Score Adjustment Rules ===
        if score >= 70:
            score += 5  # Small elite bonus for ultra-strong setups
        elif score < 30:
            score = max(score - 5, 0)  # Penalty for weak setups

        # === 5. Score Capping and Finalization ===
        final_score = min(max(score, 0), 100)

        return final_score

    except Exception as e:
        # Failsafe fallback
        from bot.utils.logger import setup_logger
        logger = setup_logger(__name__)
        logger.error(f"❌ [Signal Rater Error] {e}")
        return 0
