# bot/engine/signal_category_engine.py

"""
A.R.K. Signal Category Engine – Ultra Precision Classification 5.5
Transforms signal scores (0–100) into meaningful, professional-grade trading categories.

Built for: Instant Signal Understanding, Smart Risk Adjustment, and Institutional-Grade Trading Discipline.
Made in Bali. Engineered with German Precision.
"""

from bot.utils.logger import setup_logger

logger = setup_logger(__name__)

def categorize_signal(score: float) -> str:
    """
    Maps the numeric signal score (0–100) into a strategic trading category.

    Args:
        score (float): Signal quality/confidence score.

    Returns:
        str: Markdown-friendly category label with emoji.
    """
    try:
        if score >= 95:
            category = "🏆 *God Tier Setup* – _Institutional Grade_"
        elif score >= 90:
            category = "🚀 *Ultra Setup* – _Elite Opportunity_"
        elif score >= 80:
            category = "📈 *Top Setup* – _Strong Momentum_"
        elif score >= 70:
            category = "✅ *High Probability* – _Favorable Trade Zone_"
        elif score >= 60:
            category = "👀 *Moderate Setup* – _Needs Confirmation_"
        elif score >= 50:
            category = "⚠️ *Caution Zone* – _Uncertain Structure_"
        elif score >= 40:
            category = "🟡 *High Risk* – _Reactive Conditions_"
        elif score >= 30:
            category = "🔻 *Unfavorable* – _Avoid if Possible_"
        else:
            category = "❌ *Do Not Trade* – _Noise or Breakdown_"

        logger.info(f"[SignalCategoryEngine] Score {score:.1f} → Category: {category}")
        return category

    except Exception as e:
        logger.error(f"❌ [SignalCategoryEngine] Critical Error: {e}")
        return "❓ *Unknown Signal Classification*"

def classify_signal_short(score: float) -> str:
    """
    Returns only the short technical label (e.g. 'Top Setup', 'Caution', etc.)
    For internal filtering, backend logic, or JSON responses.

    Args:
        score (float): Signal quality score.

    Returns:
        str: Technical short category
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
            return "Moderate"
        elif score >= 50:
            return "Caution"
        elif score >= 40:
            return "High Risk"
        elif score >= 30:
            return "Unfavorable"
        else:
            return "Reject"

    except Exception as e:
        logger.error(f"❌ [SignalCategoryEngine - Short] Error: {e}")
        return "Unknown"
