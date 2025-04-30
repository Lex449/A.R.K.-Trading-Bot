"""
A.R.K. Ultra Premium Signal Builder – Multilingual Master Build.
Combines strategy, psychology, and clean minimalism for maximum trading impact.
Made in Bali. Engineered with German Precision.
"""

from bot.utils.i18n import get_text
from bot.utils.language import get_language

def build_signal_message(
    symbol: str,
    patterns: list,
    combined_action: str,
    avg_confidence: float,
    indicator_score: float,
    trend_direction: str,
    chat_id: int = None
) -> str:
    """
    Builds the ultimate premium trading signal message.

    Args:
        symbol (str): Trading symbol (e.g., AAPL, TSLA)
        patterns (list): List of detected pattern names
        combined_action (str): Ultra Long 📈 / Ultra Short 📉 / Neutral ⚪
        avg_confidence (float): Average confidence of the detected patterns
        indicator_score (float): Composite score from RSI, EMA, Patterns
        trend_direction (str): Current trend direction
        chat_id (int, optional): For localized language fallback

    Returns:
        str: Ready-to-send premium structured trading signal message.
    """
    if not patterns:
        return get_text("no_patterns_found", get_language(chat_id))

    lang = get_language(chat_id) or "en"

    # === Header decision based on signal quality ===
    if avg_confidence >= 85 and indicator_score >= 80:
        header = get_text("signal_header_super", lang)
    elif avg_confidence >= 70:
        header = get_text("signal_header_strong", lang)
    else:
        header = get_text("signal_header_moderate", lang)

    # === Stars based on confidence level ===
    stars = "⭐" * min(5, max(1, int(avg_confidence // 20)))

    # === Clean pattern rendering ===
    pattern_text = "\n".join([f"• {p}" for p in patterns])

    # === Message Assembly ===
    message = (
        f"{header}\n\n"
        f"*{get_text('symbol', lang)}:* `{symbol}`\n"
        f"*{get_text('action', lang)}:* {combined_action}\n"
        f"*{get_text('trend_structure', lang)}:* {trend_direction}\n"
        f"*{get_text('signal_quality', lang)}:* {stars} ({avg_confidence:.1f}%)\n"
        f"*{get_text('indicator_score', lang)}:* `{indicator_score:.1f}%`\n\n"
        f"✨ *{get_text('detected_patterns', lang)}:*\n{pattern_text}\n\n"
        f"_{get_text('signal_footer', lang)}_"
    )

    return message
