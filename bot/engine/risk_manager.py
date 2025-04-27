# bot/engine/risk_manager.py

"""
Bewertung von Trading-Signalen basierend auf Sternebewertung, Confidence und RSI.
Ultra-Masterclass Build für maximale Entscheidungsqualität.
"""

import logging

# Setup Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async def assess_signal_risk(signal_data: dict) -> tuple:
    """
    Bewertet ein Trading-Signal basierend auf:
    - Sternebewertung
    - Confidence
    - RSI
    Gibt ein formatiertes Risiko-Message-Template zurück + Warnflag.
    
    Args:
        signal_data (dict): Signal-Daten mit Sternen, Confidence, Pattern, RSI.

    Returns:
        tuple: (Risk-Message: str, Warning-Flag: bool)
    """
    stars = signal_data.get("stars", 0)
    confidence = signal_data.get("confidence", 0)
    pattern = signal_data.get("pattern", "Unknown")
    rsi = signal_data.get("rsi", None)

    try:
        # === Bewertung basierend auf Sternen ===
        if stars == 5:
            rating_text = "✅ *Ultra High-Quality Signal (5⭐)* – _Technische Perfektion._"
        elif stars == 4:
            rating_text = "✅ *Strong Quality Signal (4⭐)* – _Sehr gute Marktbedingungen._"
        elif stars == 3:
            rating_text = "⚠️ *Moderate Signal (3⭐)* – _Zusatzbestätigung empfohlen._"
        else:
            rating_text = "❌ *Low Quality Signal (<3⭐)* – _Nicht handeln empfohlen._"

        # === Confidence Bewertung ===
        confidence_text = f"*Confidence:* `{confidence:.1f}%`"
        confidence_warning = ""
        if confidence < 55:
            confidence_warning = "\n❗ *Low Confidence Warning (<55%).*"

        # === RSI Bewertung ===
        rsi_text = ""
        if rsi is not None:
            if rsi > 70:
                rsi_text = "\n🔴 *RSI Overbought Warning (>70)*"
            elif rsi < 30:
                rsi_text = "\n🔵 *RSI Oversold Opportunity (<30)*"

        # === Handlungsempfehlung ===
        suggested_action = "Hold ⚪"
        if stars >= 4 and confidence >= 70:
            suggested_action = "Strong Buy 📈"
        elif stars >= 4 and confidence < 70:
            suggested_action = "Buy 📈 (Caution)"
        elif stars == 3 and confidence >= 60:
            suggested_action = "Watchlist 👀"
        elif stars <= 2:
            suggested_action = "Avoid ❌"

        # === Finale Risk Message ===
        final_message = (
            f"⚡ *Risk Analysis*\n\n"
            f"*Pattern Detected:* `{pattern}`\n"
            f"{confidence_text}\n"
            f"*Rating:* {'⭐' * stars}\n\n"
            f"{rating_text}"
            f"{confidence_warning}"
            f"{rsi_text}\n\n"
            f"📢 *Suggested Action:* {suggested_action}"
        )

        # === Risiko-Flag bestimmen ===
        is_warning = stars <= 2 or confidence < 55

        logger.info(f"[Risk Manager] Pattern: {pattern}, Stars: {stars}, Confidence: {confidence}%")
        return final_message, is_warning

    except Exception as e:
        logger.error(f"[Risk Manager Error] {str(e)}")
        return "⚠️ *Risk Analysis Error.* _Proceed cautiously._", True
