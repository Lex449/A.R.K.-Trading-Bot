"""
A.R.K. Confidence Optimizer – Adaptive Premium Engine 4.1
Smart Scaling + Winrate-Adaptive Boosting + Signal-Context Fusion for Maximum Confidence Precision.

Made in Bali. Engineered with German Precision.
"""

from bot.config.settings import get_settings
from bot.utils.logger import setup_logger

logger = setup_logger(__name__)
config = get_settings()

def adjust_confidence(raw_confidence: float) -> float:
    """Applies global static multiplier if enabled."""
    if not config.get("CONFIDENCE_ADJUSTMENT_ENABLED", False):
        return raw_confidence

    scaling = config.get("CONFIDENCE_SCALING_FACTOR", 1.0)
    adjusted = raw_confidence * scaling
    final = round(min(adjusted, 100.0), 2)
    logger.info(f"🧠 [ConfidenceOptimizer] Static Scaling: {raw_confidence:.2f} ➔ {final:.2f}")
    return final

def tune_by_winrate(confidence: float, session_stats: dict) -> float:
    """Adjusts confidence based on bot session win-rate (strong signals / total)."""
    total = session_stats.get("signals_total", 1)
    strong = session_stats.get("strong_signals", 0)
    win_rate = strong / total

    if win_rate > 0.75:
        confidence += 6
        logger.info("📈 High Winrate Boost (+6%)")
    elif win_rate < 0.35:
        confidence -= 5
        logger.info("📉 Low Winrate Penalty (−5%)")

    return round(min(max(confidence, 0), 100), 2)

def boost_by_context(confidence: float, signal_data: dict) -> float:
    """Boosts confidence based on live signal strength factors like pattern + trend + volume."""
    trend = signal_data.get("trend_info", {}).get("early_trend", "").lower()
    patterns = signal_data.get("patterns", [])
    volume_spike = signal_data.get("volume_info", {}).get("spike_strength", "")
    volatility = signal_data.get("volatility_info", {}).get("volatility_spike", False)

    # Boost: Bullish Trend + Long Pattern (strong)
    if trend == "bullish" and any(p.get("action", "").startswith("Long") and p.get("stars", 0) >= 4 for p in patterns):
        confidence += 4
        logger.info("⚡ Trend + Pattern Synergy (+4%)")

    # Boost: Ultra Volume Spike
    if volume_spike == "Ultra Spike 🔥":
        confidence += 5
        logger.info("🔥 Ultra Volume Spike Boost (+5%)")

    # Boost: Any 5-Star Pattern
    if any(p.get("stars", 0) == 5 for p in patterns):
        confidence += 6
        logger.info("🏆 5-Star Pattern Boost (+6%)")

    # Penalty: Volatility Spike Detected
    if volatility:
        confidence -= 4  # vorher −6%
        logger.info("🌪️ Volatility Penalty (−4%)")

    return round(min(max(confidence, 0), 100), 2)

def optimize_confidence(signal_data: dict, session_stats: dict) -> float:
    """Combines static scaling, winrate bias and context-based boosters."""
    if not signal_data or "confidence" not in signal_data:
        return 0.0

    raw = float(signal_data.get("confidence", 0.0))
    scaled = adjust_confidence(raw)
    tuned = tune_by_winrate(scaled, session_stats)
    boosted = boost_by_context(tuned, signal_data)

    logger.info(f"🚀 [ConfidenceOptimizer] Final: {boosted:.2f}% (raw: {raw:.2f}%)")
    return boosted
