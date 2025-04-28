# bot/utils/volatility_alert_builder.py

"""
A.R.K. Volatility Alert Builder – Multilingual Ultra Precision Notifications.
"""

from bot.utils.i18n import get_text

def build_volatility_alert(symbol: str, move_data: dict, lang: str = "en") -> str:
    """
    Builds a multilingual volatility alert based on movement detection.

    Args:
        symbol (str): Trading symbol (e.g., AAPL)
        move_data (dict): Movement data containing "move_percent", "volume_spike", "trend"
        lang (str): "en" (default) or "de"

    Returns:
        str: Structured volatility alert message.
    """
    try:
        move_percent = move_data["move_percent"]
        volume_spike = move_data["volume_spike"]
        trend = move_data["trend"]
    except KeyError as e:
        # Critical fallback if move_data is incomplete
        raise ValueError(f"[Volatility Alert Builder] Missing key in move_data: {e}")

    # === Build Message Dynamically via i18n ===
    header = get_text("volatility_alert_header", lang)
    move_label = get_text("volatility_alert_move", lang)
    volume_label = get_text("volatility_alert_volume", lang)
    trend_label = get_text("volatility_alert_trend", lang)
    footer = get_text("volatility_alert_footer", lang)

    message = (
        f"{header}\n\n"
        f"*Symbol:* `{symbol}`\n"
        f"*{move_label}:* `{move_percent:.2f}%`\n"
        f"*{volume_label}:* `{volume_spike:.1f}%`\n"
        f"*{trend_label}:* {trend}\n\n"
        f"{footer}"
    )

    return message
