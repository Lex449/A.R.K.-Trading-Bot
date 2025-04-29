"""
A.R.K. Signal Rating Engine – Ultra Adaptive Intelligence 3.0
Scores signals dynamically based on pattern strength, volatility, trend confirmation, and multi-factor harmony.

Built for: Flawless Signal Validation, Elite Trade Prioritization, Scalable Risk Management.
"""

from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

def rate_signal(patterns: list, volatility_info: dict = None, trend_info: dict = None) -> int:
    """
    Calculates a premium signal rating between 0 and 100 based on real-world trading conditions.

    Args:
        patterns (list): List of detected patterns (must contain stars field).
        volatility_info (dict, optional): Output from VolatilityDetector.
        trend_info (dict, optional): Output from Multifactor Trend Detector.

    Returns:
        int: Signal quality score (0–100).
    """
    if not patterns or not isinstance(patterns, list):
        return 0

    try:
        score = 0

        # === 1. Pattern Quality Weighting ===
        for pattern in patterns:
            stars = pattern.get("stars", 0)

            if stars >= 5:
                score += 35
            elif stars == 4:
                score += 25
            elif stars == 3:
                score += 12
            elif stars == 2:
                score += 5

        # === 2. Volatility Environment Impact ===
        if volatility_info and volatility_info.get("volatility_spike", False):
            score += 20  # High potential setups when volatility spikes
        else:
            score -= 5  # Lower opportunity in flat markets

        # === 3. Early Trend Alignment Bonus ===
        if trend_info:
            early_trend = trend_info.get("early_trend", "").lower()
            if early_trend == "bullish" or early_trend == "bearish":
                score += 15

        # === 4. Reward Consistency Factors (If Both Detected) ===
        if volatility_info and trend_info:
            score += 10  # Rare full-market alignment → strong confirmation

        # === 5. Final Dynamic Tuning ===
        if score >= 80:
            score += 5  # Elite setups extra reward
        elif score <= 25:
            score = max(score - 10, 0)  # Penalize weak setups even further

        # === 6. Clamp Score to 0–100 Range ===
        final_score = min(max(score, 0), 100)

        logger.info(f"✅ [Signal Rating Engine] Final Score: {final_score}")
        return final_score

    except Exception as e:
        logger.error(f"❌ [Signal Rating Engine] Critical Error: {e}")
        return 0
