import logging
from bot.utils.logger import setup_logger
from bot.utils.i18n import get_text  # Für Multilingualität

# Setup structured logger
logger = setup_logger(__name__)

# In-Memory Performance Metrics
performance_data = {
    "total_signals": 0,
    "strong_signals": 0,
    "weak_signals": 0,
    "total_confidence": 0.0,  # Neu hinzugefügt für Confidence Tracking
}

def update_performance(stars: int, confidence: float, lang: str = "en"):
    """
    Aktualisiert die Performance-Daten basierend auf der Sternebewertung des Signals und der Confidence.
    
    Args:
        stars (int): Anzahl der Sterne für das Handelssignal.
        confidence (float): Confidence-Wert des Signals.
        lang (str): Sprache ("en" oder "de").
    """
    performance_data["total_signals"] += 1
    performance_data["total_confidence"] += confidence

    # Signal Qualität basierend auf Sternen und Confidence
    if stars >= 4 and confidence >= 70:
        performance_data["strong_signals"] += 1
        logger.info(f"[Performance Tracker] Starkes Signal registriert ({stars}⭐), Confidence: {confidence}%")
    else:
        performance_data["weak_signals"] += 1
        logger.info(f"[Performance Tracker] Schwaches Signal registriert ({stars}⭐), Confidence: {confidence}%")

def get_performance_summary(lang: str = "en") -> str:
    """
    Erzeugt eine zusammengefasste Echtzeit-Performance-Übersicht.

    Args:
        lang (str): Sprache für die Rückgabe der Übersichts-Meldung.

    Returns:
        str: Formatierter Performance-Report in der gewünschten Sprache.
    """
    total = performance_data["total_signals"]
    strong = performance_data["strong_signals"]
    weak = performance_data["weak_signals"]
    avg_confidence = performance_data["total_confidence"] / total if total > 0 else 0
    accuracy = (strong / total * 100) if total > 0 else 0

    # Sprachspezifische Templates
    templates = {
        "en": {
            "title": "📈 *Performance Overview*",
            "total_signals": "*Total Signals:*",
            "strong_signals": "*Strong Signals (4–5⭐):*",
            "weak_signals": "*Weak Signals (<4⭐):*",
            "accuracy": "*Accuracy:*",
            "confidence": "*Average Confidence:*",
            "footer": "⚡ _Stay disciplined. Quality over quantity._"
        },
        "de": {
            "title": "📈 *Performance-Übersicht*",
            "total_signals": "*Gesamtzahl der Signale:*",
            "strong_signals": "*Starke Signale (4–5⭐):*",
            "weak_signals": "*Schwache Signale (<4⭐):*",
            "accuracy": "*Genauigkeit:*",
            "confidence": "*Durchschnittliche Confidence:*",
            "footer": "⚡ _Bleib diszipliniert. Qualität über Quantität._"
        }
    }

    t = templates.get(lang.lower(), templates["en"])

    return (
        f"{t['title']}\n\n"
        f"{t['total_signals']} `{total}`\n"
        f"{t['strong_signals']} `{strong}`\n"
        f"{t['weak_signals']} `{weak}`\n"
        f"{t['accuracy']} `{accuracy:.2f}%`\n"
        f"{t['confidence']} `{avg_confidence:.2f}%`\n\n"
        f"{t['footer']}"
    )
