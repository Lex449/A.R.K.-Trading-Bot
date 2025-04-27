# bot/utils/signal_builder.py

"""
A.R.K. Ultra Premium Signal Builder
Fusion aus Strategie, Psychologie und Eleganz – gebaut für maximalen Impact.
"""

def build_signal_message(symbol: str, patterns: list, combined_action: str, avg_confidence: float, indicator_score: float, trend_direction: str) -> str:
    """
    Baut das ultimative Premium-Trading-Signal für Telegram.

    Args:
        symbol (str): Handelssymbol (z.B. AAPL, TSLA)
        patterns (list): Liste erkannter Pattern-Namen
        combined_action (str): Ultra Long 📈 / Ultra Short 📉 / Neutral ⚪
        avg_confidence (float): Durchschnittliche Muster-Confidence
        indicator_score (float): Gesamtscore aus RSI, EMA, Muster
        trend_direction (str): Trendrichtung basierend auf EMA (Long/Short/Neutral)

    Returns:
        str: Fertig strukturierte, elegante Nachricht
    """
    if not patterns:
        return ""

    # === Header Entscheidung basierend auf Qualität ===
    if avg_confidence >= 85 and indicator_score >= 80:
        header = "🚀 *Super Signal – Maximale Übereinstimmung!*"
    elif avg_confidence >= 70:
        header = "⚡ *Strong Signal – Hochbewertetes Setup*"
    else:
        header = "⚠️ *Moderates Signal – Zusätzliche Bestätigung empfohlen*"

    # === Sterne aus Confidence (1–5) ===
    stars = "⭐" * min(5, max(1, int(avg_confidence // 20)))

    # === Muster elegant auflisten ===
    patterns_text = "\n".join([f"• {p}" for p in patterns])

    # === Final strukturierter Nachrichtentext ===
    message = (
        f"{header}\n\n"
        f"*Symbol:* `{symbol}`\n"
        f"*Aktion:* {combined_action}\n"
        f"*Trendstruktur:* {trend_direction}\n"
        f"*Signal Qualität:* {stars} ({avg_confidence:.1f}%)\n"
        f"*Indikator Score:* `{indicator_score:.1f}%`\n\n"
        f"✨ *Gefundene Muster:*\n{patterns_text}\n\n"
        f"_🧠 Fokus schlägt Geschwindigkeit. Qualität schlägt Quantität._\n"
        f"_Kein Spam. Kein Stress. Nur echtes Mentoring._"
    )

    return message
