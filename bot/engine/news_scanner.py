# bot/engine/news_scanner.py

"""
A.R.K. Breaking News Scanner – Institutional Risk Guard 2025
Monitors economic news headlines to filter dangerous trading periods.
Designed for: Crash Avoidance, Strategic Pause, News-Driven Volatility Control.
"""

import logging
import random

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# === Sample Critical Events (Expand as needed) ===
CRITICAL_EVENTS = [
    "FOMC",
    "Federal Reserve",
    "CPI",
    "Inflation Report",
    "Nonfarm Payrolls",
    "Unemployment Rate",
    "Interest Rate Decision",
    "ECB Press Conference",
    "BoE Monetary Policy",
    "GDP Release",
    "Retail Sales",
    "ISM Manufacturing",
    "PPI",
    "Initial Jobless Claims",
    "Fed Chair Speech",
    "Treasury Yields Spike",
    "Geopolitical Tensions",
    "Central Bank Announcement",
    "Debt Ceiling Talks",
]

def detect_breaking_news(latest_headlines: list) -> list:
    """
    Scans incoming news headlines for high-risk events.

    Args:
        latest_headlines (list): List of news headlines (strings)

    Returns:
        list: List of detected critical events
    """
    if not latest_headlines:
        logger.info("[NewsScanner] No headlines to scan.")
        return []

    critical_matches = []

    for headline in latest_headlines:
        normalized = headline.lower()

        for event in CRITICAL_EVENTS:
            if event.lower() in normalized:
                critical_matches.append(event)
                logger.info(f"⚠️ [NewsScanner] Critical event detected: {event}")

    return critical_matches

def format_breaking_news(events: list) -> str:
    """
    Formats the detected critical events into a premium bilingual alert.

    Args:
        events (list): List of critical events

    Returns:
        str: Formatted alert message
    """
    if not events:
        return "✅ *No critical breaking news detected. Markets stable.*"

    random.shuffle(events)
    alert_list = "\n".join([f"• {event}" for event in events])

    return (
        "⚠️ *Breaking News Detected!*\n\n"
        "High-risk market events identified:\n"
        f"{alert_list}\n\n"
        "⚡ *Caution advised for all trading activities!*"
    )
