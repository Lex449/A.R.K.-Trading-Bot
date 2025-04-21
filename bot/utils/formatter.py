# bot/utils/formatter.py

import random

def format_signal(symbol: str, trend: str, confidence: int, pattern: str) -> str:
    emojis = {
        "Long": "🚀",
        "Short": "📉",
        "Neutral": "⏳"
    }
    emoji = emojis.get(trend, "📊")
    stars = "⭐️" * confidence + "✩" * (5 - confidence)

    quotes = [
        "Bleib fokussiert. A.R.K. scannt weiter.",
        "Disziplin schlägt Timing. Immer.",
        "Der beste Einstieg ist manchmal Geduld.",
        "Du bist der Trader. A.R.K. dein Radar.",
        "Nicht klicken ist auch eine Entscheidung."
    ]

    message = (
        f"{emoji} *Signal für {symbol}*
"
        f"━━━━━━━━━━━━━━━━━━━━━
"
        f"📈 *Trend:* {trend}
"
        f"📊 *Muster:* {pattern}
"
        f"⭐️ *Qualität:* {stars}
"
        f"━━━━━━━━━━━━━━━━━━━━━
"
        f"🧠 _{random.choice(quotes)}_"
    )

    return message