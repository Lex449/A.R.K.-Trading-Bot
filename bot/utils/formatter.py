# bot/utils/formatter.py

def format_signal(symbol: str, trend: str, confidence: float, pattern: str, rsi: float = None, lang: str = "en") -> str:
    """
    Formatiert das Analyseergebnis für die Telegram-Ausgabe auf Mentor-Niveau – inkl. Emojis, Klartext und RSI.
    """
    emojis = {
        "trend_up": "🚀",
        "trend_down": "📉",
        "bullish": "🟢",
        "bearish": "🔴",
        "neutral": "⚪️",
        "rsi": "💹"
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

    confidence_stars = "⭐️" * min(int(confidence // 5), 5)
    rsi_line = f"• *RSI:* {rsi:.2f} {emojis['rsi']}\n" if rsi is not None else ""

    if lang == "de":
        return (
            f"*{symbol}* {emojis['trend_up'] if trend == 'up' else emojis['trend_down']}\n"
            f"• *Trend:* {trend_text['de']}\n"
            f"• *Vertrauen:* {confidence:.2f}% {confidence_stars}\n"
            f"{rsi_line}"
            f"• *Pattern:* {pattern} {pattern_emoji}"
        )
    else:
        return (
            f"*{symbol}* {emojis['trend_up'] if trend == 'up' else emojis['trend_down']}\n"
            f"• *Trend:* {trend_text['en']}\n"
            f"• *Confidence:* {confidence:.2f}% {confidence_stars}\n"
            f"{rsi_line}"
            f"• *Pattern:* {pattern} {pattern_emoji}"
        )
