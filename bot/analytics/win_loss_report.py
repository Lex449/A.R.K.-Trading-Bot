# bot/analytics/win_loss_report.py

"""
Erzeugt Win/Loss-Reports für Session Reviews.
Ultra-Masterclass Build – Bugatti meets Pagani Level.
"""

from datetime import datetime
from bot.analytics.performance_tracker import get_performance_summary
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

def generate_win_loss_report() -> str:
    """
    Erstellt einen detaillierten Win/Loss-Performance-Report.

    Returns:
        str: Formatierter Report für Session-Übersicht.
    """
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    performance = get_performance_summary()

    logger.info(f"[Win/Loss Report] Bericht generiert am {timestamp}.")

    return (
        f"📊 *Win/Loss Report*\n"
        f"🕒 *Generated:* `{timestamp}`\n\n"
        f"{performance}\n"
        f"🧠 _Stay sharp. Every trade is a lesson._"
    )
