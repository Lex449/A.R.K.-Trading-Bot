# bot/engine/confidence_optimizer.py

"""
A.R.K. Confidence Optimizer – Ultra Premium Master Engine 4.0
Dynamic Confidence Adjustment + Smart Performance Tuning + Scaling Fusion.

Built for: Adaptive Learning, Ultra-Accurate Signals, Institutional-Grade Trading.

Made in Bali. Engineered with German Precision.
"""

from bot.config.settings import get_settings
from bot.utils.logger import setup_logger

# Setup logger and config
logger = setup_logger(__name__)
config = get_settings()

def adjust_confidence(raw_confidence: float) -> float:
    """
    Static adjustment via global scaling factor (if enabled).

    Args:
        raw_confidence (float)

    Returns:
        float
    """
    if not config.get("CONFIDENCE_ADJUSTMENT_ENABLED", False):
        return raw_confidence

    scaling_factor = config.get("CONFIDENCE_SCALING_FACTOR", 1.0)
    adjusted = raw_confidence * scaling_factor
    final = round(min(adjusted, 100.0), 2)
    logger.info(f"🧠 [ConfidenceOptimizer] Static scaling: {raw_confidence:.2f} ➔ {final:.2f}")
    return final

def tune_by_winrate(confidence: float, session_stats: dict) -> float:
    """
    Adjusts based on session win-rate only.

    Args:
        confidence (float)
        session_stats (dict)

    Returns:
        float
    """
    total = session_stats.get("signals_total", 1)
    strong = session_stats.get("strong_signals", 0)
    win_rate = strong / total

    if win_rate > 0.75:
        confidence += 5
        logger.info("📈 Win-rate boost (+5%)")
    elif win_rate < 0.4:
        confidence -= 7
        logger.info("📉 Win-rate penalty (−7%)")

    return round(min(max(confidence, 0), 100), 2)

def boost_by_context(confidence: float, signal_data: dict) -> float:
    """
    Context-based signal quality booster.

    Trigger:
    - Bullish trend + bullish pattern = +3%
    - Ultra Volume Spike = +4%
    - Strong pattern (5⭐) = +5%
    - High volatility = -6%

    Returns:
        float
    """
    trend = signal_data.get("trend_info", {}).get("trend", "").lower()
    patterns = signal_data.get("patterns", [])
    volume = signal_data.get("volume_info", {}).get("spike_strength", "")
    volatility = signal_data.get("volatility_info", {}).get("volatility_spike", False)

    # Trend + pattern boost
    if trend == "bullish" and any(p.get("action", "").startswith("Long") and p.get("stars", 0) == 5 for p in patterns):
        confidence += 3
        logger.info("⚡ Trend + Pattern Match Boost (+3%)")

    if volume == "Ultra Spike 🔥":
        confidence += 4
        logger.info("🔥 Ultra Volume Boost (+4%)")

    if any(p.get("stars", 0) == 5 for p in patterns):
        confidence += 5
        logger.info("🏆 5-Star Pattern Boost (+5%)")

    if volatility is True:
        confidence -= 6
        logger.info("🌪️ Volatility Penalty (−6%)")

    return round(min(max(confidence, 0), 100), 2)

def optimize_confidence(signal_data: dict, session_stats: dict) -> float:
    """
    Applies all optimization layers: static, winrate, contextual.

    Returns:
        float: Final confidence
    """
    if not signal_data or "confidence" not in signal_data:
        return 0.0

    base = float(signal_data.get("confidence", 0.0))

    # 1. Static Scaling
    static = adjust_confidence(base)

    # 2. Session Performance
    tuned = tune_by_winrate(static, session_stats)

    # 3. Signal-Specific Booster
    boosted = boost_by_context(tuned, signal_data)

    logger.info(f"🚀 [ConfidenceOptimizer] Final Confidence: {boosted:.2f}% (from raw {base:.2f}%)")
    return boosted
