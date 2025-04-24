# bot/utils/formatter.py

def format_signal(symbol: str, trend: str, confidence: str, pattern: str, rsi: float = None, lang: str = "en") -> str:
    """
    Formatiert das Analyseergebnis für die Telegram-Ausgabe mit Trend, Confidence-Stufe, RSI & Pattern.
    """

    trend_emojis = {
        "LONG": "🚀",
        "SHORT": "📉",
        "NEUTRAL": "⚖️"
    }

    confidence_emojis = {
        "hoch": "⭐️⭐️⭐️⭐️⭐️",
        "mittel": "⭐️⭐️⭐️",
        "niedrig": "⭐️"
    }

    pattern_emoji = "🟢" if "Bullish" in pattern else "🔴" if "Bearish" in pattern else "⚪️"
    emoji_rsi = "💹"
    trend_icon = trend_emojis.get(trend, "❓")
    confidence_icon = confidence_emojis.get(confidence, "❔")

    if lang == "de":
        rsi_text = f"• *RSI:* {rsi:.2f} {emoji_rsi}\n" if rsi is not None else ""
        return (
            f"*{symbol}* {trend_icon}\n"
            f"• *Trend:* {trend}\n"
            f"• *Vertrauen:* {confidence} {confidence_icon}\n"
            f"{rsi_text}"
            f"• *Pattern:* {pattern} {pattern_emoji}"
        )
    else:
        rsi_text = f"• *RSI:* {rsi:.2f} {emoji_rsi}\n" if rsi is not None else ""
        return (
            f"*{symbol}* {trend_icon}\n"
            f"• *Trend:* {trend}\n"
            f"• *Confidence:* {confidence} {confidence_icon}\n"
            f"{rsi_text}"
            f"• *Pattern:* {pattern} {pattern_emoji}"
        )
