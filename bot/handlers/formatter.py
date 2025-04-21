def format_signal(symbol: str, trend: str, confidence: int, pattern: str) -> str:
    emojis = {
        "Long": "🚀",
        "Short": "📉",
        "Neutral": "⏳"
    }
    emoji = emojis.get(trend, "📊")

    stars = "⭐️" * confidence + "✩" * (5 - confidence)

    lines = [
        f"{emoji} *Signal für {symbol}*",
        "-----------------------------",
        f"📈 *Trend:* {trend}",
        f"📊 *Muster:* {pattern}",
        f"⭐️ *Qualität:* {stars}",
        "",
        "_Bleib fokussiert. A.R.K. scannt weiter._"
    ]

    return "\n".join(lines)