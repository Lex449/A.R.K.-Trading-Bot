# bot/utils/breaking_news_filter.py

"""
A.R.K. Breaking News Filter – Ultra Impact Scoring System.
Assigns weighted points to news headlines based on critical keywords.
"""

# Punkte-Logik
KEYWORD_SCORES = {
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
}

THRESHOLD_POINTS = 6  # Nur News mit 6+ Punkten werden gesendet

def evaluate_headline(headline: str) -> int:
    """
    Evaluates a headline based on keyword points.

    Args:
        headline (str): The news headline.

    Returns:
        int: Total score based on matched keywords.
    """
    score = 0
    headline_lower = headline.lower()

    for keyword, points in KEYWORD_SCORES.items():
        if keyword in headline_lower:
            score += points

    return score

def is_breaking_news(headline: str) -> bool:
    """
    Determines if a headline qualifies as breaking news.

    Args:
        headline (str): The news headline.

    Returns:
        bool: True if score exceeds threshold.
    """
    return evaluate_headline(headline) >= THRESHOLD_POINTS
