# bot/utils/notification_builder.py

"""
A.R.K. Notification Builder – Ultra Premium Signal Formatter.
Now fully multilingual (i18n) and production-grade clean.
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
    Constructs a multilingual premium trading signal notification.

    Args:
        symbol (str): Trading symbol (e.g., AAPL)
        action (str): Trade action (Long 📈 or Short 📉)
        move_percent (float): Detected movement percentage
        volume_spike (float): Volume spike relative to normal
        trend_direction (str): 📈 or 📉 trend symbol
        confidence (float): Signal confidence (0–100%)
        risk_reward (str): Estimated Risk/Reward (e.g., "2.5R")
        chat_id (int, optional): For language detection.

    Returns:
        str: Fully formatted multilingual trading notification.
    """
    lang = get_language(chat_id) or "en"

    # Dynamic confidence labels
    if confidence >= 90:
        confidence_label = get_text("notification_confidence_ultra", lang)
    elif confidence >= 75:
        confidence_label = get_text("notification_confidence_high", lang)
    elif confidence >= 60:
        confidence_label = get_text("notification_confidence_moderate", lang)
    else:
        confidence_label = get_text("notification_confidence_low", lang)

    # Assemble final message
    message = (
        f"🚨 *{get_text('notification_title', lang).format(action=action)}*\n\n"
        f"*{get_text('symbol', lang)}:* `{symbol}`\n"
        f"*{get_text('move', lang)}:* `{move_percent:.2f}%`\n"
        f"*{get_text('volume_spike', lang)}:* `{volume_spike:.2f}%`\n"
        f"*{get_text('trend', lang)}:* {trend_direction}\n"
        f"*{get_text('confidence', lang)}:* `{confidence:.1f}%`\n"
        f"*{get_text('risk_reward', lang)}:* `{risk_reward}`\n\n"
        f"{confidence_label}\n\n"
        f"{get_text('notification_footer', lang)}"
    )

    return message
