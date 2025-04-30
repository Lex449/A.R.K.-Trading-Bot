"""
A.R.K. Confidence Optimizer – Adaptive Premium Engine 4.2
Smart Scaling + Winrate-Adaptive Boosting + Signal-Context Fusion for Maximum Confidence Precision.

Made in Bali. Engineered with German Precision.
"""

from bot.config.settings import get_settings
from bot.utils.logger import setup_logger

logger = setup_logger(__name__)
config = get_settings()

def adjust_confidence(raw_confidence: float) -> float:
    """
    Applies static scaling factor if enabled.
    """
    if not config.get("CONFIDENCE_ADJUSTMENT_ENABLED", False):
        return raw_confidence

    scaling_factor = config.get("CONFIDENCE_SCALING_FACTOR", 1.0)
    adjusted = raw_confidence * scaling_factor
    final = round(min(adjusted, 100.0), 2)

    logger.info(f"🧠 [ConfidenceOptimizer] Scaling applied: {raw_confidence:.2f} ➜ {final:.2f} (×{scaling_factor})")
    return final

def tune_by_winrate(confidence: float, stats: dict) -> float:
    """
    Adjusts confidence based on winrate (strong_signals / total_signals).
    """
    total = stats.get("signals_total", 1)
    strong = stats.get("strong_signals", 0)
    winrate = strong / total

    if winrate > 0.75:
        confidence += 6
        logger.info("📈 [ConfidenceOptimizer] Winrate >75% – Boost +6%")
    elif winrate < 0.35:
        confidence -= 5
        logger.info("📉 [ConfidenceOptimizer] Winrate <35% – Penalty −5%")

    return round(min(max(confidence, 0), 100), 2)

def boost_by_context(confidence: float, data: dict) -> float:
    """
    Boost confidence based on pattern/trend/volume context.
    """
    trend = data.get("trend_info", {}).get("early_trend", "").lower()
    patterns = data.get("patterns", [])
    volume_spike = data.get("volume_info", {}).get("spike_strength", "")
    volatility_spike = data.get("volatility_info", {}).get("volatility_spike", False)

    # Synergy boost: Bullish trend + strong long pattern
    if trend == "bullish" and any(p.get("action") == "Long 📈" and p.get("stars", 0) >= 4 for p in patterns):
        confidence += 4
        logger.info("⚡ [ConfidenceOptimizer] Trend+Pattern synergy +4%")

    # Volume spike boost
    if volume_spike == "Ultra Spike 🔥":
        confidence += 5
        logger.info("🔥 [ConfidenceOptimizer] Ultra Volume Spike +5%")

    # 5-Star pattern boost
    if any(p.get("stars", 0) == 5 for p in patterns):
        confidence += 6
        logger.info("🏆 [ConfidenceOptimizer] 5-Star Pattern +6%")

    # Volatility penalty
    if volatility_spike:
        confidence -= 4
        logger.info("🌪️ [ConfidenceOptimizer] Volatility penalty −4%")

    return round(min(max(confidence, 0), 100), 2)

def optimize_confidence(signal_data: dict, session_stats: dict) -> float:
    """
    Main entry point: combines scaling, winrate and context for final confidence score.
    """
    if not signal_data or "confidence" not in signal_data:
        return 0.0

    raw = float(signal_data.get("confidence", 0.0))
    scaled = adjust_confidence(raw)
    tuned = tune_by_winrate(scaled, session_stats)
    boosted = boost_by_context(tuned, signal_data)

    logger.info(f"✅ [ConfidenceOptimizer] Final Confidence: {boosted:.2f}% (raw: {raw:.2f}%)")
    return boosted
