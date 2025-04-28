"""
A.R.K. Win/Loss Report Generator – Detailed Session Snapshots
Generates time-stamped reports of trading performance.
"""

from datetime import datetime
from bot.analytics.performance_tracker import get_performance_summary
from bot.utils.logger import setup_logger
from bot.utils.i18n import get_text  # Multilingual support

# Setup structured logger
logger = setup_logger(__name__)

def generate_win_loss_report(lang: str = "en") -> str:
    """
    Generates a detailed Win/Loss Report including timestamps and performance snapshot.
    """

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    performance = get_performance_summary(lang)

    logger.info(f"[Win/Loss Report] Report generated at {timestamp}.")

    templates = {
        "en": {
            "title": "📊 *Win/Loss Report*",
            "generated": "🕒 *Generated:*",
            "footer": "🧠 _Stay sharp. Every trade is a lesson._"
        },
        "de": {
            "title": "📊 *Win/Loss Bericht*",
            "generated": "🕒 *Erstellt:*",
            "footer": "🧠 _Bleib fokussiert. Jeder Trade ist eine Lektion._"
        }
    }

    t = templates.get(lang.lower(), templates["en"])

    return (
        f"{t['title']}\n"
        f"{t['generated']} `{timestamp}`\n\n"
        f"{performance}\n"
        f"{t['footer']}"
    )
