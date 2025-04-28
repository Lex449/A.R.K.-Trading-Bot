# bot/utils/notification_builder.py

"""
A.R.K. Notification Builder – Premium Signal Formatting Engine.
Designed for ultra-clear, professional, emotionally strong trading alerts.
"""

def build_trading_signal_notification(
    symbol: str,
    action: str,
    move_percent: float,
    volume_spike: float,
    trend_direction: str,
    confidence: float,
    risk_reward: str
) -> str:
    """
    Constructs a premium trading signal notification text.

    Args:
        symbol (str): Trading symbol (e.g., AAPL)
        action (str): Trade action (Long 📈 or Short 📉)
        move_percent (float): Detected movement percentage
        volume_spike (float): Volume spike relative to normal
        trend_direction (str): 📈 or 📉 representing trend direction
        confidence (float): Signal confidence (0–100%)
        risk_reward (str): Estimated Risk/Reward ratio (e.g., "2.5R")

    Returns:
        str: Fully formatted premium trading notification.
    """

    # Dynamic confidence labels
    if confidence >= 90:
        confidence_label = "🔥 *Ultra High Confidence!*"
    elif confidence >= 75:
        confidence_label = "⚡ *High Confidence!*"
    elif confidence >= 60:
        confidence_label = "🔍 *Moderate Confidence*"
    else:
        confidence_label = "⚠️ *Low Confidence* – Caution advised!"

    # Assemble final message
    message = (
        f"🚨 *{action} Trading Opportunity Detected!*\n\n"
        f"*Symbol:* `{symbol}`\n"
        f"*Move:* `{move_percent:.2f}%`\n"
        f"*Volume Spike:* `{volume_spike:.2f}%` above average\n"
        f"*Trend:* {trend_direction}\n"
        f"*Confidence:* `{confidence:.1f}%`\n"
        f"*Risk/Reward:* `{risk_reward}`\n\n"
        f"{confidence_label}\n\n"
        f"Stay precise. Stay disciplined. 🚀"
    )

    return message
