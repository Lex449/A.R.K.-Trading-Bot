# bot/utils/formatter.py

def format_signal(symbol: str, trend: str, confidence: int, pattern: str) -> str:
    """
    Formatiert das Handelssignal für die Ausgabe im Telegram-Chat.
    """
    emojis = {
        "LONG": "🚀",
        "SHORT": "📉",
        "Neutral": "⏳",
        None: "⚪️"
    }

    footer_lines = [
        "_Bleib wachsam – A.R.K. scannt weiter._",
        "_Präzision schlägt Panik._",
        "_Noch kein Einstieg? Geduld zahlt sich aus._",
        "_Ruhige Hände, starke Entscheidungen._"
    ]

    emoji = emojis.get(trend.upper(), "⚪️")
    stars = "⭐️" * confidence + "✩" * (5 - confidence)
    footer = footer_lines[confidence % len(footer_lines)]

    return (
        f"{emoji} *Signal für {symbol}*\n"
        f"-----------------------------\n"
        f"📈 *Trend:* `{trend}`\n"
        f"📊 *Muster:* `{pattern}`\n"
        f"⭐️ *Qualität:* {stars}\n\n"
        f"{footer}"
    )
