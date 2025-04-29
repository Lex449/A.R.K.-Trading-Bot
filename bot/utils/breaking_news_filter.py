"""
A.R.K. Breaking News Filter – Ultra Impact Detection + Adaptive Dynamic Scoring System 5.0
Smart detection of market-moving headlines with multilingual support and weighted criticality scoring.

Built for: Lightning-fast Filtering, Real AI Readiness, Maximum Signal Quality.
"""

from bot.utils.logger import setup_logger
from bot.utils.keyword_enricher import get_all_keywords

# Setup structured logger
logger = setup_logger(__name__)

# === Static High-Impact Keywords (English + German) ===
HIGH_IMPACT_KEYWORDS = {
    "en": [
        "earnings beat", "profit warning", "merger", "acquisition", "lawsuit", "bankruptcy",
        "buyback", "sec investigation", "resignation", "layoffs", "guidance raise", "guidance cut",
        "rating upgrade", "rating downgrade", "dividend increase", "dividend cut",
        "split", "reverse split", "partnership", "strategic review", "data breach", "product recall"
    ],
    "de": [
        "gewinnausblick", "übernahme", "fusion", "klage", "insolvenz", "aktienrückkauf",
        "rücktritt", "entlassungen", "gewinnwarnung", "prognoseanhebung", "prognosesenkung",
        "rating upgrade", "rating downgrade", "dividendenkürzung", "dividendenanhebung",
        "aktienteilung", "umgekehrte aktienteilung", "partnerschaft", "datenleck", "rückrufaktion"
    ]
}

# === Dynamic Weighted Scoring System (Base Score Map) ===
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

# === Thresholds ===
SIMPLE_IMPACT_MATCH = True  # Fast keyword detection for instant signals
SMART_SCORE_THRESHOLD = 6   # Weighted score minimum for true "breaking" news

def is_breaking_news(headline: str, lang: str = "en") -> bool:
    """
    Determines if a headline is breaking news based on high-impact keyword match or weighted score.

    Args:
        headline (str): Headline text.
        lang (str): "en" or "de" for language.

    Returns:
        bool: True if important enough to trigger alert.
    """
    if not headline:
        return False

    headline_lower = headline.lower()

    try:
        # === Phase 1: Fast Impact Keywords Match ===
        keywords = HIGH_IMPACT_KEYWORDS.get(lang.lower(), HIGH_IMPACT_KEYWORDS["en"])
        if any(keyword in headline_lower for keyword in keywords):
            logger.info(f"[Breaking News Filter] Fast Match Detected: {headline}")
            return True

        # === Phase 2: Dynamic Weighted Impact Scoring ===
        score = 0
        enriched_keywords = set(BASE_KEYWORD_SCORES.keys()).union(get_all_keywords())

        for keyword in enriched_keywords:
            if keyword in headline_lower:
                score += BASE_KEYWORD_SCORES.get(keyword, 4)  # Unknown keywords get base 4 points

        if score >= SMART_SCORE_THRESHOLD:
            logger.info(f"[Breaking News Filter] Weighted Score {score} => Breaking News: {headline}")
            return True

    except Exception as e:
        logger.error(f"[Breaking News Filter Critical Error] {e}")

    return False
