"""
A.R.K. Signal Category Engine – Masterclass v5.6
Maps confidence scores (0–100) to ultra-clear signal categories with strategic clarity.

Made in Bali. Engineered with German Precision.
"""

from bot.utils.logger import setup_logger

logger = setup_logger(__name__)

def categorize_signal(score: float) -> str:
    """
    Converts a signal score into a Markdown-formatted category label.

    Args:
        score (float): Signal quality/confidence score (0–100)

    Returns:
        str: Markdown string with emoji label.
    """
    try:
        if score >= 95:
            category = "🏆 *God Tier Setup* – _Institutional Grade Entry_"
        elif score >= 90:
            category = "🚀 *Ultra Setup* – _Elite Momentum Detected_"
        elif score >= 80:
            category = "📈 *Top Setup* – _High Confidence Pattern_"
        elif score >= 70:
            category = "✅ *High Probability* – _Favorable Signal Cluster_"
        elif score >= 60:
            category = "☑️ *Confirmed Opportunity* – _Slight Risk Present_"
        elif score >= 50:
            category = "⚠️ *Caution Setup* – _Possible Entry, Needs Context_"
        elif score >= 40:
            category = "🟡 *High Risk Zone* – _Structure Weak or Incomplete_"
        elif score >= 30:
            category = "🔻 *Unfavorable* – _Likely Noise_"
        else:
            category = "❌ *No Trade* – _Insufficient Quality_"

        logger.info(f"[SignalCategoryEngine] Score {score:.1f} → {category}")
        return category

    except Exception as e:
        logger.error(f"❌ [SignalCategoryEngine] Critical Error: {e}")
        return "❓ *Unknown Classification*"

def classify_signal_short(score: float) -> str:
    """
    Internal tech label for logic or analytics.
    """
    try:
        if score >= 95:
            return "God Tier"
        elif score >= 90:
            return "Ultra"
        elif score >= 80:
            return "Top"
        elif score >= 70:
            return "High"
        elif score >= 60:
            return "Confirmed"
        elif score >= 50:
            return "Caution"
        elif score >= 40:
            return "Risk"
        elif score >= 30:
            return "Weak"
        else:
            return "Reject"

    except Exception as e:
        logger.error(f"❌ [SignalCategoryEngine - Short] Error: {e}")
        return "Unknown"
