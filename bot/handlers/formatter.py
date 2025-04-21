# bot/utils/formatter.py

def format_signal(symbol: str, trend: str, confidence: int, pattern: str) -> str:
    emojis = {
        "Long": "🚀",
        "Short": "📉",
        "Neutral": "⏳"
    }
    emoji = emojis.get(trend, "📊")

    stars = "⭐️" * confidence + "✩" * (5 - confidence)

    message = (
        f"{emoji} *Signal für {symbol}*\n"
        f"-----------------------------\n"
        f"📈 *Trend:* {trend}\n"
        f"📊 *Muster:* {pattern}\n"
        f"⭐️ *Qualität:* {stars}\n\n"
        f"_Bleib fokussiert. A.R.K. scannt weiter._"
    )

    return message
    
    # Updated to fix potential invisible character issue
    