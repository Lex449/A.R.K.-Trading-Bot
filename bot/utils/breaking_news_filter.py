"""
A.R.K. Breaking News Filter – Dynamic Ultra Impact Scoring System.
Assigns smart, weighted scores to news headlines based on critical and adaptive keywords.
"""

from bot.utils.keyword_enricher import get_all_keywords
from bot.utils.logger import setup_logger

# Setup Logger
logger = setup_logger(__name__)

# Static base keyword scores (critical impact words)
BASE_KEYWORD_SCORES = {
    "recession": 7,
    "crash": 7,
    "bankruptcy": 7,
    "collapse": 7,
    "inflation": 6,
    "rate hike": 6,
    "defaults": 6,
    "fed": 5,
    "fomc": 5,
    "layoffs": 5,
    "geopolitical": 5,
    "interest rates": 5,
    "market turmoil": 5,
    "earnings warning": 5,
    "data breach": 5,
    "sec investigation": 6,
    "ceo resigns": 5,
    "mass layoffs": 6,
    "chip shortage": 4,
    "ai revolution": 4,
    "guidance cut": 5,
    "guidance lowered": 5,
    "bank crisis": 7,
}

THRESHOLD_POINTS = 6  # Minimum points needed to be considered breaking news

def evaluate_headline(headline: str) -> int:
    """
    Dynamically evaluates a news headline for critical impact.

    Args:
        headline (str): The news headline.

    Returns:
        int: Total weighted score based on matched keywords.
    """
    score = 0
    headline_lower = headline.lower()

    # Load all keywords dynamically (base + enriched)
    keywords = set(BASE_KEYWORD_SCORES.keys()).union(get_all_keywords())

    for keyword in keywords:
        if keyword in headline_lower:
            score += BASE_KEYWORD_SCORES.get(keyword, 4)  # Default unknown keyword weight = 4

    if score > 0:
        logger.info(f"[Breaking News Filter] Headline scored {score} points: {headline}")

    return score

def is_breaking_news(headline: str) -> bool:
    """
    Determines if a news headline is considered breaking news.

    Args:
        headline (str): The news headline.

    Returns:
        bool: True if headline exceeds impact threshold.
    """
    return evaluate_headline(headline) >= THRESHOLD_POINTS
