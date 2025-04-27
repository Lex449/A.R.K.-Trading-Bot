# bot/utils/signal_builder.py

"""
Baut die Premium-Detail-Signale für Telegram-Ausgabe.
Masterclass Format: Alle Muster, Confidence, Sterne, klare Richtung.
"""

def build_signal_message(symbol: str, patterns: list, combined_action: str, avg_confidence: float) -> str:
    """
    Erzeugt ein strukturiertes Trading-Signal auf Ultra-Niveau.

    Args:
        symbol (str): Das gecheckte Symbol (z.B. US100).
        patterns (list): Liste erkannter Muster-Strings.
        combined_action (str): Zusammengefasste Richtung (Ultra Long/Short/Neutral).
        avg_confidence (float): Durchschnittliche Confidence aller Muster.

    Returns:
        str: Fertig formatierte Signalnachricht.
    """
    if not patterns:
        return ""

    # Premium-Format der Musterliste
    patterns_text = ""
    for p in patterns:
        patterns_text += f"• {p}\n"

    message = (
        f"⚡ *Live Trading Signal!*\n\n"
        f"*Symbol:* `{symbol}`\n"
        f"*Aktion:* {combined_action}\n"
        f"*Durchschnittliche Confidence:* `{avg_confidence:.1f}%`\n"
        f"*Muster erkannt:*\n{patterns_text}\n"
        f"🧠 _Qualität vor Quantität. Diszipliniertes Risikomanagement entscheidet._"
    )

    return message
