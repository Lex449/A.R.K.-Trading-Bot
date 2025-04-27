# bot/utils/notification_builder.py

"""
A.R.K. Notification Builder – Premium Signal Formatting Engine.
Designed for ultra-clear, professional, emotionally strong trading alerts.
"""

def build_trading_signal_notification(symbol, action, move_percent, volume_spike, trend_direction, confidence, risk_reward):
    """
    Constructs a premium trading signal notification text.

    Args:
        symbol (str): Symbol name (e.g., AAPL)
        action (str): Long 📈 or Short 📉
        move_percent (float): Detected movement percentage
        volume_spike (float): Volume spike relative to normal
        trend_direction (str): 📈 or 📉 emoji for trend
        confidence (float): Signal confidence (0-100%)
        risk_reward (str): Estimated Risk/Reward e.g., 2.5R

    Returns:
        str: Perfectly formatted notification text
    """

    # Dynamische Farben / Emojis je nach Confidence
    if confidence >= 90:
        confidence_label = "🔥 *Ultra High Confidence!*"
    elif confidence >= 75:
        confidence_label = "⚡ *High Confidence!*"
    elif confidence >= 60:
        confidence_label = "🔍 *Moderate Confidence*"
    else:
        confidence_label = "⚠️ *Low Confidence* – Caution!"

    # Zusammenbau
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
