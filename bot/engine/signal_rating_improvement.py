"""
A.R.K. Signal Rating Engine – Ultra Adaptive Intelligence 5.0
Multi-Factor Signal Score Optimizer with Pattern Weighting, Volatility Bias, Trend Synergy & Strategic Reinforcement.

Built for: Elite Signal Validation, AI Scoring, Institutional-Grade Prioritization.
Made in Bali. Engineered with German Precision.
"""

from bot.utils.logger import setup_logger

# Structured logger setup
logger = setup_logger(__name__)

def rate_signal(patterns: list, volatility_info: dict = None, trend_info: dict = None) -> int:
    """
    Rates a signal based on:
    - Pattern Quality
    - Volatility Environment
    - Early Trend Confirmation
    - Multi-Factor Synergy

    Args:
        patterns (list): List of detected patterns with 'stars' attribute.
        volatility_info (dict): Volatility detection output.
        trend_info (dict): Early trend detection output.

    Returns:
        int: Final signal score between 0–100.
    """

    if not patterns or not isinstance(patterns, list):
        logger.warning("[SignalRating] No valid patterns found.")
        return 0

    try:
        score = 0

        # === 1. Pattern-Based Weighting ===
        for pattern in patterns:
            stars = pattern.get("stars", 0)
            weight = {
                5: 35,
                4: 25,
                3: 12,
                2: 5,
                1: 2,
            }.get(stars, 0)
            score += weight

        # === 2. Volatility Bonus ===
        if volatility_info:
            if volatility_info.get("volatility_spike", False):
                score += 20
            else:
                score -= 5  # Low-vol environment = lower conviction

        # === 3. Trend Confirmation ===
        trend = trend_info.get("early_trend", "").lower() if trend_info else ""
        if trend in {"bullish", "bearish"}:
            score += 15

        # === 4. Synergy Bonus ===
        if volatility_info and trend_info:
            score += 10  # All components align

        # === 5. Confidence Check ===
        total_stars = sum(p.get("stars", 0) for p in patterns)
        avg_stars = total_stars / len(patterns)
        if avg_stars < 3:
            score -= 10

        # === 6. Reinforcement Rules ===
        if score >= 85:
            score += 5  # Elite confirmation
        elif score <= 25:
            score = max(score - 10, 0)  # Weak signal adjustment

        # === 7. Clamp to 0–100 ===
        final_score = int(min(max(score, 0), 100))

        logger.info(f"✅ [SignalRating] Final Score: {final_score} | Patterns: {len(patterns)} | Stars: {total_stars}")
        return final_score

    except Exception as e:
        logger.error(f"❌ [SignalRating] Engine Crash: {e}")
        return 0
