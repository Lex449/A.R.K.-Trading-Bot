"""
A.R.K. Signal Rating Engine – Ultra Adaptive Intelligence 5.2
Precision Weighting + Trend Synergy + Pattern Trust Layering.

Built for: Elite Signal Clarity, Institutional-Grade Prioritization.
Made in Bali. Engineered with German Precision.
"""

from bot.utils.logger import setup_logger

logger = setup_logger(__name__)

def rate_signal(patterns: list, volatility_info: dict = None, trend_info: dict = None) -> int:
    """
    Calculates a composite score for signal strength based on pattern quality,
    volatility context, and trend alignment.
    """
    if not patterns or not isinstance(patterns, list):
        logger.warning("⚠️ [SignalRating] No valid pattern list provided.")
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
            logger.info("🌪️ [SignalRating] Volatility spike detected → +15")

        # === 3. Trend Match Bonus ===
        trend = trend_info.get("early_trend", "").lower() if trend_info else ""
        has_bullish = any(p.get("action", "").startswith("Long") for p in patterns)
        has_bearish = any(p.get("action", "").startswith("Short") for p in patterns)

        if trend == "bullish" and has_bullish:
            score += 15
            logger.info("📈 [SignalRating] Bullish trend + long pattern match → +15")
        elif trend == "bearish" and has_bearish:
            score += 15
            logger.info("📉 [SignalRating] Bearish trend + short pattern match → +15")
        elif trend in {"bullish", "bearish"}:
            score += 5
            logger.info("📊 [SignalRating] Trend present, weak pattern alignment → +5")

        # === 4. Weak Pattern Penalty ===
        if avg_stars < 3:
            score -= 10
            logger.info("⚠️ [SignalRating] Weak pattern set detected → −10")

        # === 5. Synergy Bonus ===
        if volatility_info and trend_info and avg_stars >= 4:
            score += 10
            logger.info("🔗 [SignalRating] Pattern + Trend + Volatility synergy → +10")

        # === 6. Reinforcement Edge ===
        if score >= 90:
            score += 5
            logger.info("💎 [SignalRating] Elite score reinforcement → +5")
        elif score < 30:
            score = max(score - 10, 0)
            logger.info("🧪 [SignalRating] Low score adjustment → −10")

        # === 7. Finalization ===
        final = int(min(max(score, 0), 100))
        logger.info(f"✅ [SignalRating] Final Score: {final} | Patterns: {len(patterns)} | Stars: {total_stars}")
        return final

    except Exception as e:
        logger.error(f"❌ [SignalRating] Engine Crash: {e}")
        return 0
