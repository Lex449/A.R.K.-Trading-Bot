# bot/utils/formatter.py

import random

def format_signal(symbol: str, trend: str, confidence: int, pattern: str) -> str:
    emojis = {
        "Long": "🚀",
        "Short": "📉",
        "Neutral": "⏳"
    }
    trends_text = {
        "Long": "Aufwärtstrend erkannt",
        "Short": "Abwärtstrend erkannt",
        "Neutral": "Seitwärtsphase"
    }
    endings = [
        "_Bleib wachsam – A.R.K. scannt weiter._",
        "_A.R.K. beobachtet. Du reagierst._",
        "_Präzision ist der Schlüssel. Handle nicht blind._",
        "_Noch kein Einstieg? Geduld zahlt sich aus._"
    ]

    emoji = emojis.get(trend, "📊")
    trend_text = trends_text.get(trend, "Unklarer Trend")
    stars = "⭐️" * confidence + "✩" * (5 - confidence)
    footer = random.choice(endings)

    message = (
        f"{emoji} *Signal für {symbol}*\n"
        f"-----------------------------\n"
        f"📈 *Trend:* {trend_text}\n"
        f"📊 *Muster:* {pattern}\n"
        f"⭐️ *Qualität:* {stars}\n\n"
        f"{footer}"
    )

    return message
