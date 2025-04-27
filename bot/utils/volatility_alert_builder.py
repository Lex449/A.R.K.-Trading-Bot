"""
A.R.K. Volatility Alert Builder – Multilingual Ultra Precision Notifications.
"""

def build_volatility_alert(symbol: str, move_data: dict, lang: str = "en") -> str:
    """
    Builds a volatility alert text based on move detection.

    Args:
        symbol (str): Trading symbol
        move_data (dict): Move and volume info
        lang (str): Language ("en" or "de")

    Returns:
        str: Structured alert message
    """
    move_percent = move_data["move_percent"]
    volume_spike = move_data["volume_spike"]
    trend = move_data["trend"]

    if lang == "de":
        return (
            f"🚨 *Starke Bewegung erkannt!*\n\n"
            f"*Symbol:* `{symbol}`\n"
            f"*Bewegung:* `{move_percent:.2f}%`\n"
            f"*Volumenanstieg:* `{volume_spike:.1f}%` über Durchschnitt\n"
            f"*Trend:* {trend}\n\n"
            f"⚡ _Bleib fokussiert. Chancen entstehen im Sturm._"
        )
    else:
        return (
            f"🚨 *Strong Move Detected!*\n\n"
            f"*Symbol:* `{symbol}`\n"
            f"*Move:* `{move_percent:.2f}%`\n"
            f"*Volume Spike:* `{volume_spike:.1f}%` above average\n"
            f"*Trend:* {trend}\n\n"
            f"⚡ _Stay sharp. Opportunities are born in volatility._"
        )
