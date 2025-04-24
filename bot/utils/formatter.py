# bot/utils/formatter.py

def format_signal(symbol: str, trend: str, confidence: float, pattern: str, lang: str = "en") -> str:
    """
    Formatiert das Analyseergebnis für die Telegram-Ausgabe.
    """

    # Emojis für Stimmung
    emoji_trend = "📈" if trend == "up" else "📉"
    emoji_conf = "⭐" * min(int(confidence // 5), 5)
    emoji_pattern = "🟢" if "Bullish" in pattern else "🔴" if "Bearish" in pattern else "⚪️"

    if lang == "de":
        return (
            f"*{symbol}* {emoji_trend}\n"
            f"• *Trend:* {'Aufwärts' if trend == 'up' else 'Abwärts'}\n"
            f"• *Vertrauen:* {confidence:.2f}% {emoji_conf}\n"
            f"• *Pattern:* {pattern} {emoji_pattern}"
        )
    else:
        return (
            f"*{symbol}* {emoji_trend}\n"
            f"• *Trend:* {'Uptrend' if trend == 'up' else 'Downtrend'}\n"
            f"• *Confidence:* {confidence:.2f}% {emoji_conf}\n"
            f"• *Pattern:* {pattern} {emoji_pattern}"
        )
