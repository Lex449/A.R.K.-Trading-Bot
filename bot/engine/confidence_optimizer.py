"""
A.R.K. Confidence Optimizer – Ultra Premium Master Engine 3.0
Dynamic Confidence Adjustment + Smart Performance Tuning + Scaling Fusion.

Built for: Adaptive Learning, Ultra-Accurate Signals, Institutional-Grade Trading.

Made in Bali. Engineered with German Precision.
"""

from bot.config.settings import get_settings
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)
config = get_settings()

def adjust_confidence(raw_confidence: float) -> float:
    """
    Adjusts the raw confidence score based on static scaling factors.

    Args:
        raw_confidence (float): Original confidence (0–100).

    Returns:
        float: Scaled confidence (max 100%).
    """
    if not config.get("CONFIDENCE_ADJUSTMENT_ENABLED", False):
        return raw_confidence

    scaling_factor = config.get("CONFIDENCE_SCALING_FACTOR", 1.0)
    adjusted = raw_confidence * scaling_factor
    final_adjusted = round(min(adjusted, 100.0), 2)

    logger.info(f"🧠 [ConfidenceOptimizer] Static scaling: {raw_confidence:.2f}% ➔ {final_adjusted:.2f}%")
    return final_adjusted

def tune_confidence(signal_data: dict, session_stats: dict) -> dict:
    """
    Fine-tunes the confidence score dynamically based on session win-rate.

    Args:
        signal_data (dict): Signal data with 'confidence' field.
        session_stats (dict): Performance data with 'signals_total' and 'strong_signals'.

    Returns:
        dict: Updated signal data.
    """
    original_confidence = signal_data.get("confidence", 0.5)

    total_signals = session_stats.get("signals_total", 1)  # Avoid division by zero
    strong_signals = session_stats.get("strong_signals", 0)

    win_rate = strong_signals / total_signals

    # Dynamic tuning logic
    if win_rate > 0.7:
        adjustment = 0.1
    elif win_rate < 0.4:
        adjustment = -0.1
    else:
        adjustment = 0.0

    tuned_confidence = original_confidence + adjustment
    tuned_confidence = round(max(0.1, min(0.9, tuned_confidence)), 2)

    logger.info(f"🎯 [ConfidenceOptimizer] Tuned confidence: {original_confidence:.2f} ➔ {tuned_confidence:.2f} (Win-Rate: {win_rate:.2f})")

    signal_data["confidence"] = tuned_confidence
    return signal_data

def optimize_confidence(signal_data: dict, session_stats: dict) -> dict:
    """
    Full optimization: Scaling + Adaptive Tuning combined.

    Args:
        signal_data (dict): Signal data including 'confidence'.
        session_stats (dict): Session statistics.

    Returns:
        dict: Fully optimized signal.
    """
    if not signal_data or "confidence" not in signal_data:
        return signal_data

    # Static adjustment first
    raw_confidence = signal_data["confidence"]
    scaled_confidence = adjust_confidence(raw_confidence)
    signal_data["confidence"] = scaled_confidence

    # Then adaptive tuning
    signal_data = tune_confidence(signal_data, session_stats)

    logger.info(f"🚀 [ConfidenceOptimizer] Final optimized confidence: {signal_data['confidence']:.2f}")
    return signal_data
