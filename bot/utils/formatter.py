# bot/utils/formatter.py

def format_signal(symbol: str, trend: str, confidence: int, pattern: str) -> str:
    """Formatiert das Handelssignal für die Ausgabe im Telegram-Chat."""
    emojis = {
        "Long": "🚀",
        "Short": "📉",
        "Neutral": "⏳"
    }

    endings = [
        "_Bleib wachsam – A.R.K. scannt weiter._",
        "_A.R.K. beobachtet. Du reagierst._",
        "_Präzision ist der Schlüssel. Handle nicht blind._",
        "_Noch kein Einstieg? Geduld zahlt sich aus._"
    ]

    emoji = emojis.get(trend, "📊")
    stars = "⭐️" * confidence + "✩" * (5 - confidence)
    footer = endings[confidence % len(endings)]

    message = (
        f"{emoji} *Signal für {symbol}*\n"
        f"-----------------------------\n"
        f"📈 *Trend:* {trend}\n"
        f"📊 *Muster:* {pattern}\n"
        f"⭐️ *Qualität:* {stars}\n\n"
        f"{footer}"
    )

    return message
