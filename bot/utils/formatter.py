# bot/utils/formatter.py

def format_signal(symbol: str, trend: str, confidence: float, pattern: str, rsi: float = None, lang: str = "en") -> str:
    """
    Formatiert das Analyseergebnis für die Telegram-Ausgabe mit Emoji-Level, RSI und Pattern.
    """

    emoji_trend = "🚀" if trend == "up" else "📉"
    emoji_conf = "⭐️" * min(int(confidence // 5), 5)
    emoji_pattern = "🟢" if "Bullish" in pattern else "🔴" if "Bearish" in pattern else "⚪️"
    emoji_rsi = "💹"

    if lang == "de":
        rsi_text = f"• *RSI:* {rsi:.2f} {emoji_rsi}\n" if rsi is not None else ""
        return (
            f"*{symbol}* {emoji_trend}\n"
            f"• *Trend:* {'Aufwärtstrend' if trend == 'up' else 'Abwärtstrend'}\n"
            f"• *Vertrauen:* {confidence:.2f}% {emoji_conf}\n"
            f"{rsi_text}"
            f"• *Pattern:* {pattern} {emoji_pattern}"
        )
    else:
        rsi_text = f"• *RSI:* {rsi:.2f} {emoji_rsi}\n" if rsi is not None else ""
        return (
            f"*{symbol}* {emoji_trend}\n"
            f"• *Trend:* {'Uptrend' if trend == 'up' else 'Downtrend'}\n"
            f"• *Confidence:* {confidence:.2f}% {emoji_conf}\n"
            f"{rsi_text}"
            f"• *Pattern:* {pattern} {emoji_pattern}"
        )
