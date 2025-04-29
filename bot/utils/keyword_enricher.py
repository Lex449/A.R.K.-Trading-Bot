"""
A.R.K. Keyword Enricher – Dynamic Ultra Power Engine 2025
Builds Adaptive Market Intelligence through Keyword Enrichment and Power Ranking.

Mission: Predict Trends Before Wall Street Notices.
"""

import json
import os
from collections import defaultdict
from bot.utils.logger import setup_logger

# === Setup ===
logger = setup_logger(__name__)

# === Static Critical Keywords (Elite Intelligence Set) ===
STATIC_KEYWORDS = [
    "inflation", "rate hike", "recession", "crash", "bankruptcy",
    "fed", "defaults", "market turmoil", "collapse", "fomc",
    "interest rates", "layoffs", "job cuts", "ceo resigns",
    "data breach", "regulatory probe", "chip shortage", "ai boom",
    "electric vehicles", "earnings miss", "earnings beat", "guidance cut", "guidance lowered",
    "solar subsidy", "battery fire", "acquisition", "merger", "takeover", "spinoff",
    "bank failure", "mass layoffs", "sec investigation", "geopolitical tensions",
    "liquidity crisis", "bond yield spike", "downgrade warning", "ipo delay",
    "market manipulation", "credit downgrade", "crypto meltdown", "sovereign debt default"
]

# === Dynamic Runtime Keywords (AI Expansion) ===
DYNAMIC_KEYWORDS = set()

# === Persistent Storage ===
KEYWORD_FILE = "dynamic_keywords.json"
POWER_FILE = "keyword_power.json"

# === Keyword Power Tracking ===
keyword_power = defaultdict(int)  # Counts how often keywords appear

# === Load Dynamic Keywords ===
def _load_dynamic_keywords():
    global DYNAMIC_KEYWORDS
    if os.path.exists(KEYWORD_FILE):
        try:
            with open(KEYWORD_FILE, "r", encoding="utf-8") as f:
                keywords = json.load(f)
                if isinstance(keywords, list):
                    DYNAMIC_KEYWORDS.update(k.lower() for k in keywords if isinstance(k, str))
                    logger.info(f"✅ [KeywordEnricher] Loaded {len(DYNAMIC_KEYWORDS)} dynamic keywords.")
        except Exception as e:
            logger.warning(f"⚠️ [KeywordEnricher] Could not load dynamic keywords: {e}")

# === Load Power Data ===
def _load_keyword_power():
    global keyword_power
    if os.path.exists(POWER_FILE):
        try:
            with open(POWER_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                keyword_power.update(data)
                logger.info(f"✅ [KeywordEnricher] Loaded keyword power data.")
        except Exception as e:
            logger.warning(f"⚠️ [KeywordEnricher] Could not load keyword power data: {e}")

# === Save Dynamic Keywords & Power ===
def _save_dynamic_data():
    try:
        with open(KEYWORD_FILE, "w", encoding="utf-8") as f:
            json.dump(list(DYNAMIC_KEYWORDS), f, indent=4)
        with open(POWER_FILE, "w", encoding="utf-8") as f:
            json.dump(dict(keyword_power), f, indent=4)
        logger.info(f"💾 [KeywordEnricher] Dynamic data saved successfully.")
    except Exception as e:
        logger.error(f"❌ [KeywordEnricher] Failed to save dynamic data: {e}")

# === Enrichment Engine ===
def enrich_keywords_from_news(news_headlines: list) -> None:
    """
    Enriches keywords and updates power scores based on incoming news.

    Args:
        news_headlines (list): List of fresh news headlines (str).
    """
    global DYNAMIC_KEYWORDS

    try:
        for headline in news_headlines:
            headline_lower = headline.lower()

            # === Trend Discovery ===
            if "mass layoffs" in headline_lower or ("layoffs" in headline_lower and "massive" in headline_lower):
                DYNAMIC_KEYWORDS.add("mass layoffs")
            if "ai" in headline_lower and ("revolution" in headline_lower or "explosion" in headline_lower):
                DYNAMIC_KEYWORDS.add("ai revolution")
            if "restructuring" in headline_lower:
                DYNAMIC_KEYWORDS.add("corporate restructuring")
            if "sec probe" in headline_lower or "regulatory crackdown" in headline_lower:
                DYNAMIC_KEYWORDS.add("sec crackdown")
            if "bank failure" in headline_lower or "bank crisis" in headline_lower:
                DYNAMIC_KEYWORDS.add("bank crisis")
            if "interest rate shock" in headline_lower or "unexpected hike" in headline_lower:
                DYNAMIC_KEYWORDS.add("unexpected rate hike")
            if "supply chain disruption" in headline_lower:
                DYNAMIC_KEYWORDS.add("supply chain crisis")
            if "cyber attack" in headline_lower:
                DYNAMIC_KEYWORDS.add("cybersecurity breach")

            # === Power Ranking (Dynamic Boost) ===
            for keyword in get_all_keywords():
                if keyword in headline_lower:
                    keyword_power[keyword] += 1

        logger.info(f"🚀 [KeywordEnricher] Dynamic keywords updated: {list(DYNAMIC_KEYWORDS)}")
        logger.info(f"📈 [KeywordEnricher] Keyword power ranking updated.")

        _save_dynamic_data()

    except Exception as e:
        logger.error(f"❌ [KeywordEnricher] Failed to enrich keywords: {e}")

# === Fetch All Keywords ===
def get_all_keywords() -> list:
    """
    Returns the full active keyword set (static + dynamic).
    """
    all_keywords = set(STATIC_KEYWORDS).union(DYNAMIC_KEYWORDS)
    return sorted(all_keywords)

# === Fetch Keyword Power Scores ===
def get_keyword_power() -> dict:
    """
    Returns the current keyword power scores.

    Returns:
        dict: {keyword: occurrence_count}
    """
    return dict(keyword_power)

# === Initialization ===
_load_dynamic_keywords()
_load_keyword_power()
