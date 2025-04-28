"""
A.R.K. Keyword Enricher – Dynamic Learning System.
Auto-extends critical market keywords based on detected news trends.
"""

from bot.utils.logger import setup_logger

# Setup Logger
logger = setup_logger(__name__)

# Static keywords (initial important triggers)
BASE_KEYWORDS = [
    "inflation", "rate hike", "recession", "crash", "bankruptcy",
    "fed", "defaults", "market turmoil", "collapse", "fomc",
    "interest rates", "layoffs", "job cuts", "ceo resigns",
    "data breach", "regulatory probe", "chip shortage", "ai boom",
    "electric vehicles", "earnings miss", "earnings beat", "guidance cut", "guidance lowered",
    "solar subsidy", "battery fire", "acquisition", "merger", "takeover", "spinoff"
]

# Dynamic list (new keywords detected at runtime)
dynamic_keywords = set()

def enrich_keywords_from_news(news_headlines: list) -> None:
    """
    Dynamically enriches the keyword database based on incoming news headlines.

    Args:
        news_headlines (list): List of latest news headlines.
    """
    global dynamic_keywords
    try:
        for headline in news_headlines:
            headline_lower = headline.lower()

            # Detect possible new trends
            if "layoffs" in headline_lower and "massive" in headline_lower:
                dynamic_keywords.add("mass layoffs")
            if "ai" in headline_lower and ("revolution" in headline_lower or "explosion" in headline_lower):
                dynamic_keywords.add("ai revolution")
            if "restructuring" in headline_lower:
                dynamic_keywords.add("corporate restructuring")
            if "sec probe" in headline_lower or "regulatory crackdown" in headline_lower:
                dynamic_keywords.add("sec crackdown")
            if "bank failure" in headline_lower or "bank crisis" in headline_lower:
                dynamic_keywords.add("bank crisis")

        if dynamic_keywords:
            logger.info(f"[Keyword Enricher] New dynamic keywords detected: {dynamic_keywords}")

    except Exception as e:
        logger.error(f"[Keyword Enricher] Failed to enrich keywords: {e}")

def get_all_keywords() -> list:
    """
    Returns the full enriched keyword set.

    Returns:
        list: Combined static + dynamic keywords.
    """
    return list(set(BASE_KEYWORDS).union(dynamic_keywords))
