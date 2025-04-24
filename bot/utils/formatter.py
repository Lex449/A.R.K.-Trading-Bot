def format_signal(symbol: str, trend: str, confidence: float, pattern: str, rsi: float = None, lang: str = "en") -> str:
    """
    Formatiert das Analyseergebnis für die Telegram-Ausgabe auf Mentor-Niveau – mit präzisem Ton, starken Emojis und Motivationsfaktor.
    """
    emojis = {
        "trend_up": "🚀",
        "trend_down": "📉",
        "bullish": "🟢",
        "bearish": "🔴",
        "neutral": "⚪️",
        "rsi": "📊",
        "confidence": "⭐️",
        "fire": "🔥",
        "chart": "📈",
        "bot": "🤖",
    }

    trend_text = {
        "de": "Aufwärtstrend" if trend == "up" else "Abwärtstrend",
        "en": "Uptrend" if trend == "up" else "Downtrend"
    }

    pattern_emoji = (
        emojis["bullish"] if "Bullish" in pattern else
        emojis["bearish"] if "Bearish" in pattern else
        emojis["neutral"]
    )

    # Max 5 Sterne, basierend auf Vertrauen (z. B. 87 % = 4 Sterne)
    confidence_stars = emojis["confidence"] * min(int(confidence / 20), 5)

    # RSI nur anzeigen, wenn vorhanden
    rsi_line = f"• *RSI:* {rsi:.2f} {emojis['rsi']}\n" if rsi is not None else ""

    if lang == "de":
        return (
            f"{emojis['chart']} *{symbol}* – A.R.K. Analyse\n"
            f"• *Trend:* {trend_text['de']} {emojis['trend_up'] if trend == 'up' else emojis['trend_down']}\n"
            f"• *Vertrauen:* {confidence:.2f}% {confidence_stars}\n"
            f"{rsi_line}"
            f"• *Pattern:* {pattern} {pattern_emoji}\n\n"
            f"{emojis['bot']} _Bleib fokussiert – A.R.K. beobachtet den Markt für dich._"
        )
    else:
        return (
            f"{emojis['chart']} *{symbol}* – A.R.K. Analysis\n"
            f"• *Trend:* {trend_text['en']} {emojis['trend_up'] if trend == 'up' else emojis['trend_down']}\n"
            f"• *Confidence:* {confidence:.2f}% {confidence_stars}\n"
            f"{rsi_line}"
            f"• *Pattern:* {pattern} {pattern_emoji}\n\n"
            f"{emojis['bot']} _Stay sharp – A.R.K. is watching the market for you._"
        )
