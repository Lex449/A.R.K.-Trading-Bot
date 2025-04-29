"""
A.R.K. Signal Category Engine – Ultra Precision Classification 5.0
Transforms signal scores (0–100) into meaningful, professional-grade trading categories.

Built for: Instant Signal Understanding, Smart Risk Adjustment, and Institutional-Grade Trading Discipline.
"""

from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

def categorize_signal(score: int) -> str:
    """
    Maps the numeric signal score into a strategic trading category.

    Args:
        score (int): Signal quality score (0–100).

    Returns:
        str: Descriptive trading category.
    """
    try:
        if score >= 85:
            category = "🚀 Ultra Setup – Elite Trade Opportunity"
        elif 70 <= score < 85:
            category = "📈 Strong Opportunity – High Confidence"
        elif 55 <= score < 70:
            category = "👀 Potential Trade – Watchlist Candidate"
        elif 40 <= score < 55:
            category = "⚠️ Caution Only – Risky Environment"
        else:
            category = "❌ Avoid Trade – Low Probability Setup"

        logger.info(f"✅ [Signal Category Engine] Score {score} → Category: {category}")
        return category

    except Exception as e:
        logger.error(f"❌ [Signal Category Engine] Critical Error: {e}")
        return "❓ Unknown Signal Classification"
