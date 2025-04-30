# bot/utils/notification_builder.py

"""
A.R.K. Notification Builder – Ultra Premium Signal Formatter 2.0
Delivers multilingual, psychologically-optimized signal alerts for elite execution.

Made in Bali. Engineered with German Precision.
"""

from bot.utils.i18n import get_text
from bot.utils.language import get_language

def build_trading_signal_notification(
    symbol: str,
    action: str,
    move_percent: float,
    volume_spike: float,
    trend_direction: str,
    confidence: float,
    risk_reward: str,
    chat_id: int = None
) -> str:
    """
    Builds a professional-grade, multilingual trading signal notification.

    Args:
        symbol (str): Asset symbol (e.g. US100)
        action (str): Trade direction (Long 📈 or Short 📉)
        move_percent (float): Detected price change
        volume_spike (float): Detected volume increase
        trend_direction (str): 📈 or 📉
        confidence (float): Confidence score (0–100)
        risk_reward (str): Estimated RRR (e.g. "2.1R")
        chat_id (int): Optional – for language resolution

    Returns:
        str: Fully formatted notification message
    """

    lang = get_language(chat_id) or "en"

    # === Confidence Labeling ===
    if confidence >= 90:
        confidence_label = get_text("notification_confidence_ultra", lang)
    elif confidence >= 75:
        confidence_label = get_text("notification_confidence_high", lang)
    elif confidence >= 60:
        confidence_label = get_text("notification_confidence_moderate", lang)
    else:
        confidence_label = get_text("notification_confidence_low", lang)

    # === Emoji Reinforcement ===
    headline_emoji = "🚀" if action.startswith("Long") else "🔻"
    trend_emoji = "📈" if trend_direction.lower().startswith("bull") else "📉"

    # === Assemble Message ===
    message = (
        f"{headline_emoji} *{get_text('notification_title', lang).format(action=action)}*\n\n"
        f"*{get_text('symbol', lang)}:* `{symbol}`\n"
        f"*{get_text('move', lang)}:* `{move_percent:.2f}%`\n"
        f"*{get_text('volume_spike', lang)}:* `{volume_spike:.2f}%`\n"
        f"*{get_text('trend', lang)}:* {trend_emoji} `{trend_direction}`\n"
        f"*{get_text('confidence', lang)}:* `{confidence:.1f}%`\n"
        f"*{get_text('risk_reward', lang)}:* `{risk_reward}`\n\n"
        f"{confidence_label}\n\n"
        f"{get_text('notification_footer', lang)}"
    )

    return message
