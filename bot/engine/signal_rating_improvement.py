"""
A.R.K. Signal Rating Engine – Ultra Adaptive Intelligence 5.1
Precision Weighting + Trend Synergy + Pattern Trust Layering.

Built for: Elite Signal Clarity, Institutional-Grade Prioritization.
Made in Bali. Engineered with German Precision.
"""

from bot.utils.logger import setup_logger

logger = setup_logger(__name__)

def rate_signal(patterns: list, volatility_info: dict = None, trend_info: dict = None) -> int:
    if not patterns or not isinstance(patterns, list):
        logger.warning("[SignalRating] No valid patterns found.")
        return 0

    try:
        score = 0
        total_stars = sum(p.get("stars", 0) for p in patterns)
        avg_stars = total_stars / len(patterns)

        # === 1. Pattern-Based Weighting ===
        for p in patterns:
            stars = p.get("stars", 0)
            pattern_weight = {
                5: 50,
                4: 30,
                3: 15,
                2: 6,
                1: 3,
            }.get(stars, 0)
            score += pattern_weight

        # === 2. Volatility Bonus ===
        if volatility_info and volatility_info.get("volatility_spike", False):
            score += 15

        # === 3. Trend Match Bonus ===
        trend = trend_info.get("early_trend", "").lower() if trend_info else ""
        has_bullish = any(p.get("action", "").startswith("Long") for p in patterns)
        has_bearish = any(p.get("action", "").startswith("Short") for p in patterns)

        if (trend == "bullish" and has_bullish) or (trend == "bearish" and has_bearish):
            score += 15
        elif trend in {"bullish", "bearish"}:
            score += 5  # Trend erkennbar, aber schwache Pattern-Kombi

        # === 4. Weak Pattern Penalty ===
        if avg_stars < 3:
            score -= 10

        # === 5. Synergy Bonus (alle Module aktiv) ===
        if volatility_info and trend_info and avg_stars >= 4:
            score += 10

        # === 6. Reinforcement Edge ===
        if score >= 90:
            score += 5
        elif score < 30:
            score = max(score - 10, 0)

        # === 7. Clamp & Log ===
        final = int(min(max(score, 0), 100))
        logger.info(f"✅ [SignalRating] Final Score: {final} | Patterns: {len(patterns)} | Stars: {total_stars}")
        return final

    except Exception as e:
        logger.error(f"❌ [SignalRating] Engine Crash: {e}")
        return 0
