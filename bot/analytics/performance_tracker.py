# bot/analytics/performance_tracker.py

"""
Echtzeit-Performance-Tracker für Trading-Signale.
Ultra-Masterclass Build – Bugatti meets Pagani Level.
"""

import logging
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# In-Memory Performance Metrics
performance_data = {
    "total_signals": 0,
    "strong_signals": 0,
    "weak_signals": 0,
}

def update_performance(stars: int):
    """
    Aktualisiert die Performance-Daten basierend auf der Sternebewertung des Signals.
    
    Args:
        stars (int): Anzahl der Sterne für das Handelssignal.
    """
    performance_data["total_signals"] += 1

    if stars >= 4:
        performance_data["strong_signals"] += 1
        logger.info(f"[Performance Tracker] Starkes Signal registriert ({stars}⭐).")
    else:
        performance_data["weak_signals"] += 1
        logger.info(f"[Performance Tracker] Schwaches Signal registriert ({stars}⭐).")

def get_performance_summary() -> str:
    """
    Erzeugt eine zusammengefasste Echtzeit-Performance-Übersicht.

    Returns:
        str: Formatierter Performance-Report.
    """
    total = performance_data["total_signals"]
    strong = performance_data["strong_signals"]
    weak = performance_data["weak_signals"]

    accuracy = (strong / total * 100) if total > 0 else 0

    return (
        f"📈 *Performance Overview*\n\n"
        f"*Total Signals:* `{total}`\n"
        f"*Strong Signals (4–5⭐):* `{strong}`\n"
        f"*Weak Signals (<4⭐):* `{weak}`\n"
        f"*Accuracy:* `{accuracy:.2f}%`\n\n"
        f"⚡ _Stay disciplined. Quality over quantity._"
    )
