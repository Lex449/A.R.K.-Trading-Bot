"""
A.R.K. Keyword Enricher – Dynamic Ultra Power Engine 2025
Builds Adaptive Market Intelligence through Keyword Enrichment and Power Ranking.

Mission: Predict Trends Before Wall Street Notices.
"""

import json
import os
from collections import defaultdict
from bot.utils.logger import setup_logger

# === Setup Logger ===
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

# === Dynamic Runtime Keywords ===
DYNAMIC_KEYWORDS = set()

# === Persistent Storage Paths ===
KEYWORD_FILE = "dynamic_keywords.json"
POWER_FILE = "keyword_power.json"

# === Keyword Power Score Tracking ===
keyword_power = defaultdict(int)

# === Initialization ===
def _load_dynamic_keywords():
    if os.path.exists(KEYWORD_FILE):
        try:
            with open(KEYWORD_FILE, "r", encoding="utf-8") as f:
                raw_keywords = json.load(f)
                DYNAMIC_KEYWORDS.update(k.lower() for k in raw_keywords if isinstance(k, str))
                logger.info(f"✅ [KeywordEnricher] Loaded {len(DYNAMIC_KEYWORDS)} dynamic keywords.")
        except Exception as e:
            logger.warning(f"⚠️ [KeywordEnricher] Failed to load dynamic keywords: {e}")

def _load_keyword_power():
    if os.path.exists(POWER_FILE):
        try:
            with open(POWER_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                keyword_power.update(data)
                logger.info("✅ [KeywordEnricher] Loaded keyword power data.")
        except Exception as e:
            logger.warning(f"⚠️ [KeywordEnricher] Failed to load power data: {e}")

def _save_dynamic_data():
    try:
        with open(KEYWORD_FILE, "w", encoding="utf-8") as f:
            json.dump(sorted(DYNAMIC_KEYWORDS), f, indent=4)
        with open(POWER_FILE, "w", encoding="utf-8") as f:
            json.dump(dict(keyword_power), f, indent=4)
        logger.info("💾 [KeywordEnricher] Dynamic data saved.")
    except Exception as e:
        logger.error(f"❌ [KeywordEnricher] Failed to save dynamic data: {e}")

# === Enrichment Core ===
def enrich_keywords_from_news(news_headlines: list) -> None:
    """
    Analyzes news headlines and enriches dynamic keywords + power scores.

    Args:
        news_headlines (list): List of headline strings.
    """
    try:
        for headline in news_headlines:
            text = headline.lower()

            # === Discoverable Trends ===
            if "mass layoffs" in text or ("layoffs" in text and "massive" in text):
                DYNAMIC_KEYWORDS.add("mass layoffs")
            if "ai" in text and ("revolution" in text or "explosion" in text):
                DYNAMIC_KEYWORDS.add("ai revolution")
            if "restructuring" in text:
                DYNAMIC_KEYWORDS.add("corporate restructuring")
            if "sec probe" in text or "regulatory crackdown" in text:
                DYNAMIC_KEYWORDS.add("sec crackdown")
            if "bank failure" in text or "bank crisis" in text:
                DYNAMIC_KEYWORDS.add("bank crisis")
            if "interest rate shock" in text or "unexpected hike" in text:
                DYNAMIC_KEYWORDS.add("unexpected rate hike")
            if "supply chain disruption" in text:
                DYNAMIC_KEYWORDS.add("supply chain crisis")
            if "cyber attack" in text:
                DYNAMIC_KEYWORDS.add("cybersecurity breach")

            # === Power Scoring ===
            for keyword in get_all_keywords():
                if keyword in text:
                    keyword_power[keyword] += 1

        logger.info(f"🚀 [KeywordEnricher] Keywords enriched. Power updated.")
        _save_dynamic_data()

    except Exception as e:
        logger.error(f"❌ [KeywordEnricher] Enrichment failed: {e}")

# === API: Get Keyword Data ===
def get_all_keywords() -> list:
    """Returns static + dynamic keyword list."""
    return sorted(set(STATIC_KEYWORDS).union(DYNAMIC_KEYWORDS))

def get_keyword_power() -> dict:
    """Returns current keyword frequency scores."""
    return dict(keyword_power)

# === Load at startup ===
_load_dynamic_keywords()
_load_keyword_power()
