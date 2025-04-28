"""
A.R.K. Risk Manager – Ultra Premium Signal Risk Analyzer.
Evaluates signals based on Stars, Confidence, and RSI impact.

Built for: Precision Decision-Making & Signal Filtering.
"""

import logging

# Setup structured logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async def assess_signal_risk(signal_data: dict) -> tuple:
    """
    Evaluates a trading signal based on:
    - Star Rating
    - Confidence %
    - RSI value (if available)
    
    Returns:
        tuple: (Risk Analysis Message: str, Is High Risk: bool)
    """
    stars = signal_data.get("stars", 0)
    confidence = signal_data.get("confidence", 0.0)
    pattern = signal_data.get("pattern", "Unknown Pattern")
    rsi = signal_data.get("rsi")

    try:
        # === Star-Based Assessment ===
        if stars == 5:
            rating_text = "✅ *Ultra High-Quality Signal (5⭐)* – _Technical Excellence._"
        elif stars == 4:
            rating_text = "✅ *Strong Signal (4⭐)* – _High probability setup._"
        elif stars == 3:
            rating_text = "⚠️ *Moderate Signal (3⭐)* – _Requires confirmation._"
        else:
            rating_text = "❌ *Weak Signal (<3⭐)* – _Not recommended._"

        # === Confidence Check ===
        confidence_text = f"*Confidence:* `{confidence:.1f}%`"
        confidence_warning = ""
        if confidence < 55:
            confidence_warning = "\n❗ *Low Confidence Warning (<55%).*"

        # === RSI Interpretation ===
        rsi_text = ""
        if isinstance(rsi, (int, float)):
            if rsi > 70:
                rsi_text = "\n🔴 *Overbought Zone (>70 RSI)*"
            elif rsi < 30:
                rsi_text = "\n🔵 *Oversold Zone (<30 RSI)*"

        # === Action Recommendation ===
        if stars >= 4 and confidence >= 70:
            suggested_action = "📈 *Strong Buy Signal*"
        elif stars >= 4 and confidence >= 60:
            suggested_action = "📈 *Buy Signal (Caution)*"
        elif stars == 3 and confidence >= 60:
            suggested_action = "👀 *Add to Watchlist*"
        else:
            suggested_action = "❌ *Avoid Trade*"

        # === Assemble Final Risk Message ===
        final_message = (
            f"⚡ *Risk Analysis*\n\n"
            f"*Pattern:* `{pattern}`\n"
            f"{confidence_text}\n"
            f"*Rating:* {'⭐' * stars}\n\n"
            f"{rating_text}"
            f"{confidence_warning}"
            f"{rsi_text}\n\n"
            f"📢 *Suggested Action:* {suggested_action}"
        )

        # === High-Risk Flagging Logic ===
        is_warning = stars < 3 or confidence < 55

        logger.info(f"[Risk Manager] Signal Risk Evaluated: Pattern={pattern}, Stars={stars}, Confidence={confidence}%")

        return final_message, is_warning

    except Exception as e:
        logger.error(f"[Risk Manager Error] {e}")
        return "⚠️ *Risk Analysis Error.* _Trade with extreme caution._", True
