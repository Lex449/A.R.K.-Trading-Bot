"""
A.R.K. Performance Summary Generator
Generates multilingual performance recaps for daily reports.
Made in Bali. Engineered with German Precision.
"""

from bot.utils.i18n import get_text
from bot.utils.session_tracker import get_session_data

def get_performance_summary(lang: str = "en") -> str:
    """
    Returns a multilingual summary of today's signal statistics.
    """

    try:
        data = get_session_data()
        if not data:
            return get_text("no_data_today", lang)

        total = data.get("signals_total", 0)
        strong = data.get("strong_signals", 0)
        moderate = data.get("moderate_signals", 0)
        weak = data.get("weak_signals", 0)
        stars = round(data.get("total_confidence", 0.0), 2)

        return (
            f"{get_text('signals_total', lang)}: *{total}*\n"
            f"{get_text('strong_signals', lang)}: *{strong}*\n"
            f"{get_text('moderate_signals', lang)}: *{moderate}*\n"
            f"{get_text('weak_signals', lang)}: *{weak}*\n"
            f"{get_text('avg_confidence', lang)}: *{stars} ⭐️*"
        )

    except Exception as e:
        return f"⚠️ {get_text('summary_failed', lang)}\nError: {e}"
