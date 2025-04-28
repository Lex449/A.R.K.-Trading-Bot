"""
A.R.K. Deep Confidence Engine – Real-Time Confidence Booster
Adaptive Scaling and Recalibration for Maximum Signal Accuracy.
"""

from bot.config.settings import get_settings
from bot.utils.logger import setup_logger

# Setup Logger
logger = setup_logger(__name__)
config = get_settings()

def adjust_confidence(raw_confidence: float) -> float:
    """
    Adjusts the raw confidence score using scaling factors
    for smarter, AI-enhanced trading signals.

    Args:
        raw_confidence (float): Original confidence value from analysis (0–100).

    Returns:
        float: Adjusted confidence score.
    """
    if not config.get("CONFIDENCE_ADJUSTMENT_ENABLED", False):
        return raw_confidence

    scaling_factor = config.get("CONFIDENCE_SCALING_FACTOR", 1.0)
    adjusted_confidence = raw_confidence * scaling_factor

    # Limitieren auf maximal 100%
    adjusted_confidence = min(adjusted_confidence, 100.0)

    logger.info(f"🧠 [DeepConfidenceEngine] Confidence adjusted: {raw_confidence:.2f}% ➔ {adjusted_confidence:.2f}%")
    return adjusted_confidence
