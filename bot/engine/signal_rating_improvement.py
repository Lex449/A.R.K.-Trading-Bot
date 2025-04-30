# bot/engine/signal_rating_engine.py

"""
A.R.K. Signal Rating Engine – Ultra Adaptive Intelligence 5.0
Multi-Factor Signal Score Optimizer with Pattern Weighting, Volatility Bias, Trend Synergy & Strategic Reinforcement.

Built for: Elite Signal Validation, AI Scoring, Institutional-Grade Prioritization.
Made in Bali. Engineered with German Precision.
"""

from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

def rate_signal(patterns: list, volatility_info: dict = None, trend_info: dict = None) -> int:
    """
    Rates a signal based on:
    - Pattern Quality
    - Volatility Environment
    - Early Trend Confirmation
    - Multi-Factor Harmony

    Returns:
        int: Final score (0–100)
    """

    if not patterns or not isinstance(patterns, list):
        logger.warning("[SignalRating] No valid patterns found.")
        return 0

    try:
        score = 0

        # === 1. Pattern-Based Weighting ===
        for p in patterns:
            stars = p.get("stars", 0)
            weight = {
                5: 35,
                4: 25,
                3: 12,
                2: 5,
                1: 2,
            }.get(stars, 0)
            score += weight

        # === 2. Volatility Bias ===
        if volatility_info:
            if volatility_info.get("volatility_spike", False):
                score += 20
            else:
                score -= 5  # Flat market = less conviction

        # === 3. Trend Confirmation Bonus ===
        trend_alignment = trend_info.get("early_trend", "").lower() if trend_info else ""
        if trend_alignment in {"bullish", "bearish"}:
            score += 15

        # === 4. Multi-Factor Synergy Bonus ===
        if volatility_info and trend_info:
            score += 10  # Full alignment of trend and volatility

        # === 5. Pattern Confidence Adjustment ===
        total_stars = sum(p.get("stars", 0) for p in patterns)
        avg_stars = total_stars / len(patterns)
        if avg_stars < 3:
            score -= 10

        # === 6. Dynamic Reinforcement ===
        if score >= 85:
            score += 5  # Elite Signal Reward
        elif score <= 25:
            score = max(score - 10, 0)  # Weak Signal Penalty

        # === 7. Final Score Clamp ===
        final_score = int(min(max(score, 0), 100))

        logger.info(f"✅ [SignalRating] Final Score: {final_score} | Patterns: {len(patterns)} | Stars: {total_stars}")
        return final_score

    except Exception as e:
        logger.error(f"❌ [SignalRating] Engine Crash: {e}")
        return 0
