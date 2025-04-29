"""
A.R.K. Win/Loss Report Generator – Tactical Debrief Master Engine 2025.
Generates timestamped performance snapshots in multiple languages for deep trading insights.
"""

from datetime import datetime
from bot.analytics.performance_tracker import get_performance_summary
from bot.utils.logger import setup_logger
from bot.utils.i18n import get_text

# Setup structured logger
logger = setup_logger(__name__)

def generate_win_loss_report(lang: str = "en") -> str:
    """
    Generates a detailed Win/Loss Report including timestamp and trading session performance.
    
    Args:
        lang (str): Language code ("en" or "de").
    
    Returns:
        str: Formatted report text.
    """

    try:
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
        performance_summary = get_performance_summary(lang)

        templates = {
            "en": {
                "title": "📊 *Win/Loss Tactical Report*",
                "generated": "🕒 *Generated:*",
                "footer": "🧠 _Stay sharp. Every trade builds your legacy._"
            },
            "de": {
                "title": "📊 *Gewinn/Verlust Taktikbericht*",
                "generated": "🕒 *Erstellt:*",
                "footer": "🧠 _Bleib scharf. Jeder Trade baut dein Vermächtnis auf._"
            }
        }

        t = templates.get(lang.lower(), templates["en"])

        report = (
            f"{t['title']}\n"
            f"{t['generated']} `{timestamp}`\n\n"
            f"{performance_summary}\n"
            f"{t['footer']}"
        )

        logger.info(f"✅ [WinLossReport] Report generated successfully at {timestamp}")
        return report

    except Exception as e:
        logger.error(f"❌ [WinLossReport] Failed to generate report: {e}")
        return f"⚠️ Error generating Win/Loss Report: {e}"
