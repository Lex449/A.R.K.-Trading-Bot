from datetime import datetime
from bot.analytics.performance_tracker import get_performance_summary
from bot.utils.logger import setup_logger
from bot.utils.i18n import get_text  # Multilingual support

# Setup structured logger
logger = setup_logger(__name__)

def generate_win_loss_report(lang: str = "en") -> str:
    """
    Erstellt einen detaillierten Win/Loss-Performance-Report mit Mehrsprachigkeit.

    Args:
        lang (str): Die gewünschte Sprache für den Report ("en" oder "de").

    Returns:
        str: Formatierter Report für die Session-Übersicht.
    """
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    performance = get_performance_summary(lang)

    logger.info(f"[Win/Loss Report] Bericht generiert am {timestamp}.")

    # Sprachspezifische Templates
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

    t = templates.get(lang.lower(), templates["en"])  # fallback to English if language is unknown

    return (
        f"{t['title']}\n"
        f"{t['generated']} `{timestamp}`\n\n"
        f"{performance}\n"
        f"{t['footer']}"
    )
