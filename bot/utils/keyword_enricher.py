"""
A.R.K. Keyword Enricher – Ultra Dynamic AI Seed Engine 2025
Auto-expanding financial trend detection for unmatched news impact analysis.

Designed for: Wealth Creation, Hyper-Adaptive Learning, Autonomous AI Expansion.
"""

import json
import os
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# === Static Critical Keywords (Manual Intelligence Layer) ===
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

# === Dynamic Runtime Keywords (AI-Ready Enrichment) ===
DYNAMIC_KEYWORDS = set()

# === Persistent Dynamic Storage (optional future feature) ===
KEYWORD_FILE = "dynamic_keywords.json"

# === Load dynamic keywords if file exists ===
def _load_dynamic_keywords():
    global DYNAMIC_KEYWORDS
    if os.path.exists(KEYWORD_FILE):
        try:
            with open(KEYWORD_FILE, "r", encoding="utf-8") as f:
                keywords = json.load(f)
                if isinstance(keywords, list):
                    DYNAMIC_KEYWORDS.update(k.lower() for k in keywords if isinstance(k, str))
                    logger.info(f"✅ [KeywordEnricher] Loaded {len(DYNAMIC_KEYWORDS)} dynamic keywords from storage.")
        except Exception as e:
            logger.warning(f"⚠️ [KeywordEnricher] Failed to load dynamic keywords: {e}")

# === Save dynamic keywords persistently ===
def _save_dynamic_keywords():
    try:
        with open(KEYWORD_FILE, "w", encoding="utf-8") as f:
            json.dump(list(DYNAMIC_KEYWORDS), f, indent=4)
        logger.info(f"💾 [KeywordEnricher] Dynamic keywords saved successfully.")
    except Exception as e:
        logger.error(f"❌ [KeywordEnricher] Failed to save dynamic keywords: {e}")

# === Core Enrichment Engine ===
def enrich_keywords_from_news(news_headlines: list) -> None:
    """
    Dynamically enriches the keyword database based on detected new trends from headlines.

    Args:
        news_headlines (list): List of fresh news headlines (str).
    """
    global DYNAMIC_KEYWORDS

    try:
        for headline in news_headlines:
            headline_lower = headline.lower()

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

        if DYNAMIC_KEYWORDS:
            logger.info(f"🚀 [KeywordEnricher] Detected new dynamic keywords: {list(DYNAMIC_KEYWORDS)}")
            _save_dynamic_keywords()

    except Exception as e:
        logger.error(f"❌ [KeywordEnricher] Failed to enrich keywords: {e}")

# === Fetch All Keywords (Static + Dynamic) ===
def get_all_keywords() -> list:
    """
    Returns the full current keyword set (static + dynamic).

    Returns:
        list: All relevant market-moving keywords.
    """
    all_keywords = set(STATIC_KEYWORDS).union(DYNAMIC_KEYWORDS)
    return sorted(all_keywords)

# === Initialization at module import ===
_load_dynamic_keywords()
