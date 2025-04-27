# bot/utils/signal_builder.py

"""
A.R.K. Ultra Premium Signal Builder
Fusion aus Strategie, Psychologie und Eleganz – gebaut für maximalen Impact.
"""

def build_signal_message(symbol: str, patterns: list, combined_action: str, avg_confidence: float, indicator_score: float, trend_direction: str) -> str:
    """
    Baut das ultimative Premium-Trading-Signal für Telegram.

    Args:
        symbol (str): Handelssymbol (z.B. AAPL, SPY)
        patterns (list): Liste erkannter Pattern-Namen
        combined_action (str): Ultra Long 📈 / Ultra Short 📉 / Neutral ⚪
        avg_confidence (float): Durchschnittliche Pattern-Confidence
        indicator_score (float): Gesamtscore aus RSI, EMA, Muster
        trend_direction (str): Trendrichtung (Long/Short/Neutral)

    Returns:
        str: Final strukturierte, elegante Premium-Nachricht
    """
    if not patterns:
        return ""

    # === Header basierend auf Qualität ===
    if avg_confidence >= 85 and indicator_score >= 80:
        header = "🚀 *Super Signal – Maximum Alignment!*"
    elif avg_confidence >= 70:
        header = "⚡ *Strong Signal – High Potential Setup*"
    else:
        header = "⚠️ *Moderate Signal – Additional Confirmation Advised*"

    # === Sterne dynamisch berechnen ===
    stars = "⭐" * min(5, max(1, int(avg_confidence // 20)))

    # === Muster schön listen ===
    patterns_text = "\n".join([f"• {p}" for p in patterns])

    # === Final strukturierter Nachrichtentext ===
    message = (
        f"{header}\n\n"
        f"*Symbol:* `{symbol}`\n"
        f"*Action:* {combined_action}\n"
        f"*Trend Direction:* {trend_direction}\n"
        f"*Signal Quality:* {stars} ({avg_confidence:.1f}%)\n"
        f"*Indicator Score:* `{indicator_score:.1f}%`\n\n"
        f"✨ *Detected Patterns:*\n{patterns_text}\n\n"
        f"_🧠 Focus beats speed. Precision beats quantity._\n"
        f"_No spam. No stress. Pure mentorship._"
    )

    return message
