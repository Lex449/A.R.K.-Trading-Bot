"""
A.R.K. Performance Tracker – Ultra Premium Live Monitoring
Tracks quality, confidence, and accuracy of all generated signals.
"""

import logging
from bot.utils.logger import setup_logger
from bot.utils.i18n import get_text  # Für Multilingualität

# Setup structured logger
logger = setup_logger(__name__)

# In-Memory Performance Metrics
performance_data = {
    "total_signals": 0,
    "strong_signals": 0,
    "moderate_signals": 0,
    "weak_signals": 0,
    "total_confidence": 0.0,
}

def update_performance(stars: int, confidence: float, lang: str = "en"):
    """
    Updates the live performance statistics based on star rating and confidence.
    """

    performance_data["total_signals"] += 1
    performance_data["total_confidence"] += confidence

    if stars >= 5:
        performance_data["strong_signals"] += 1
        logger.info(f"✅ [Performance Tracker] 5⭐ Elite Signal | Confidence: {confidence:.2f}%")
    elif stars == 4:
        performance_data["moderate_signals"] += 1
        logger.info(f"⚡ [Performance Tracker] 4⭐ Good Signal | Confidence: {confidence:.2f}%")
    else:
        performance_data["weak_signals"] += 1
        logger.info(f"⚠️ [Performance Tracker] Weak Signal ({stars}⭐) | Confidence: {confidence:.2f}%")

def get_performance_summary(lang: str = "en") -> str:
    """
    Returns a detailed real-time performance report.
    """

    total = performance_data["total_signals"]
    strong = performance_data["strong_signals"]
    moderate = performance_data["moderate_signals"]
    weak = performance_data["weak_signals"]
    avg_confidence = (performance_data["total_confidence"] / total) if total else 0.0
    accuracy = (strong / total * 100) if total else 0.0

    # Templates
    templates = {
        "en": {
            "title": "📈 *Performance Overview*",
            "total_signals": "*Total Signals:*",
            "strong_signals": "*Strong (5⭐):*",
            "moderate_signals": "*Moderate (4⭐):*",
            "weak_signals": "*Weak (<4⭐):*",
            "accuracy": "*Strong Accuracy:*",
            "confidence": "*Average Confidence:*",
            "footer": "⚡ _Mastery is built signal by signal._"
        },
        "de": {
            "title": "📈 *Performance-Übersicht*",
            "total_signals": "*Gesamtzahl Signale:*",
            "strong_signals": "*Stark (5⭐):*",
            "moderate_signals": "*Mittel (4⭐):*",
            "weak_signals": "*Schwach (<4⭐):*",
            "accuracy": "*Starke Trefferquote:*",
            "confidence": "*Durchschnittliche Confidence:*",
            "footer": "⚡ _Meisterschaft entsteht Signal für Signal._"
        }
    }

    t = templates.get(lang.lower(), templates["en"])

    return (
        f"{t['title']}\n\n"
        f"{t['total_signals']} `{total}`\n"
        f"{t['strong_signals']} `{strong}`\n"
        f"{t['moderate_signals']} `{moderate}`\n"
        f"{t['weak_signals']} `{weak}`\n"
        f"{t['accuracy']} `{accuracy:.2f}%`\n"
        f"{t['confidence']} `{avg_confidence:.2f}%`\n\n"
        f"{t['footer']}"
    )
