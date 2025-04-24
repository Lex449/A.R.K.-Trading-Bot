# bot/utils/formatter.py

def format_signal(symbol: str, trend: str, confidence: int, pattern: str) -> str:
    """
    Formatiert das Analyse-Ergebnis für Telegram.
    """

    trend_emojis = {
        "Aufwärtstrend": "🚀",
        "Abwärtstrend": "📉",
        "Seitwärts": "⏳",
        "Neutral": "📊"
    }

    commentary = {
        5: "Top-Setup – sofortiger Blick lohnt sich.",
        4: "Solide Chance – genauer hinsehen.",
        3: "Potenzial vorhanden – aber auf Bestätigung warten.",
        2: "Wenig Klarheit – eher abwarten.",
        1: "Neutral – kein klarer Vorteil.",
    }

    emoji = trend_emojis.get(trend, "📊")
    stars = "⭐️" * confidence + "✩" * (5 - confidence)
    note = commentary.get(confidence, "Keine Bewertung.")

    message = (
        f"{emoji} *Signal für {symbol}*\n"
        f"-----------------------------\n"
        f"📈 *Trend:* {trend}\n"
        f"📊 *Muster:* {pattern}\n"
        f"⭐️ *Qualität:* {stars}\n"
        f"🧠 *Kommentar:* _{note}_"
    )

    return message
