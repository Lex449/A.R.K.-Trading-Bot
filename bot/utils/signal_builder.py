# bot/utils/signal_builder.py

"""
A.R.K. Ultra Premium Signal Builder
Fusion der besten Designs – für echte CEO-Gelddruckmaschine.
"""

def build_signal_message(symbol: str, patterns: list, combined_action: str, avg_confidence: float, indicator_score: float, trend_direction: str) -> str:
    """
    Baut das ultimative Premium-Signal für Telegram.

    Args:
        symbol (str): Handelssymbol (z.B. AAPL, TSLA)
        patterns (list): Liste erkannter Muster als Strings
        combined_action (str): Ultra Long 📈 / Ultra Short 📉 / Neutral ⚪
        avg_confidence (float): Durchschnittliche Pattern-Confidence
        indicator_score (float): Indikator-Score (RSI/EMA kombi)
        trend_direction (str): Trendrichtung anhand EMA (Long/Short/Neutral)

    Returns:
        str: Final formatierte Premium-Nachricht
    """
    if not patterns:
        return ""

    # Signalstärke bewerten
    if avg_confidence >= 85 and indicator_score >= 80:
        header = "🚀 *Super Signal – Maximale Übereinstimmung!*"
    elif avg_confidence >= 70:
        header = "⚡ *Strong Signal – Hochbewertetes Setup*"
    else:
        header = "⚠️ *Moderates Signal – Zusätzliche Bestätigung empfohlen*"

    # Sterne aus Confidence
    stars = "⭐" * max(1, min(5, int(avg_confidence // 20)))

    # Muster schön auflisten
    patterns_text = "\n".join([f"• {p}" for p in patterns])

    # Finaler Nachrichtentext
    message = (
        f"{header}\n\n"
        f"*Symbol:* `{symbol}`\n"
        f"*Aktion:* {combined_action}\n"
        f"*Trendrichtung:* {trend_direction}\n"
        f"*Signal Rating:* {stars} ({avg_confidence:.1f}%)\n"
        f"*Indikator Score:* {indicator_score:.1f}%\n\n"
        f"*Erkannte Muster:*\n{patterns_text}\n\n"
        f"_🧠 Qualität vor Quantität. Diszipliniertes Risikomanagement entscheidet._"
    )

    return message
