"""
A.R.K. Breaking News Filter – Ultra Impact Detection + Adaptive Dynamic Scoring System 5.0
Smart detection of market-moving headlines with multilingual support and weighted criticality scoring.

Built for: Lightning-Fast Filtering, Real AI Readiness, Maximum Signal Quality.
Made in Bali. Engineered with German Precision.
"""

from bot.utils.logger import setup_logger
from bot.utils.keyword_enricher import get_all_keywords

# Setup structured logger
logger = setup_logger(__name__)

# === Static High-Impact Keywords ===
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

# === Weighted Dynamic Score Keywords ===
BASE_KEYWORD_SCORES = {
    "recession": 7, "crash": 7, "bankruptcy": 7, "collapse": 7, "inflation": 6,
    "rate hike": 6, "defaults": 6, "fed": 5, "fomc": 5, "layoffs": 5,
    "geopolitical": 5, "interest rates": 5, "market turmoil": 5, "earnings warning": 5,
    "data breach": 5, "sec investigation": 6, "ceo resigns": 5, "mass layoffs": 6,
    "chip shortage": 4, "ai revolution": 4, "guidance cut": 5, "guidance lowered": 5,
    "bank crisis": 7
}

# === Thresholds ===
SIMPLE_IMPACT_MATCH = True
SMART_SCORE_THRESHOLD = 6

def is_breaking_news(headline: str, lang: str = "en") -> bool:
    """
    Determines whether the headline qualifies as breaking news.

    Args:
        headline (str): The news headline text.
        lang (str): Language code ("en" or "de").

    Returns:
        bool: True if headline is impactful enough for alert.
    """
    if not headline:
        return False

    headline_lower = headline.lower()
    total_score = 0

    try:
        # Phase 1: High-Impact Keyword Match
        static_keywords = HIGH_IMPACT_KEYWORDS.get(lang.lower(), HIGH_IMPACT_KEYWORDS["en"])
        for kw in static_keywords:
            if kw in headline_lower:
                logger.info(f"🚨 [NewsFilter] Fast Match Detected → '{kw}' in: {headline}")
                return True

        # Phase 2: Dynamic Weighted Scoring
        all_keywords = set(BASE_KEYWORD_SCORES.keys()).union(get_all_keywords())
        for keyword in all_keywords:
            if keyword in headline_lower:
                keyword_score = BASE_KEYWORD_SCORES.get(keyword, 4)
                total_score += keyword_score
                logger.debug(f"[NewsFilter] Keyword Hit: '{keyword}' (+{keyword_score})")

        if total_score >= SMART_SCORE_THRESHOLD:
            logger.info(f"🚨 [NewsFilter] Weighted Score {total_score} => Breaking News: {headline}")
            return True
        else:
            logger.debug(f"[NewsFilter] Score {total_score} too low → Skipped: {headline}")

    except Exception as e:
        logger.error(f"❌ [NewsFilter Error] Critical failure during headline evaluation: {e}")

    return False
