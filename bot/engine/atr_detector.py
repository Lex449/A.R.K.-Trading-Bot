"""
A.R.K. Risk Manager – Ultra Premium Signal Risk Analyzer 3.0
Precision AI: Stars, Confidence, RSI & Context-Aware Trade Strategy.
"""

import logging

# Setup structured logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async def assess_signal_risk(signal_data: dict) -> tuple:
    """
    Evaluates trading signal risk based on:
    - Star Rating
    - Confidence Score
    - RSI Zone (Overbought/Oversold)

    Returns:
        tuple: (Formatted Risk Report: str, High-Risk Flag: bool)
    """

    stars = signal_data.get("stars", 0)
    confidence = signal_data.get("confidence", 0.0)
    pattern = signal_data.get("pattern", "Unknown Pattern")
    rsi = signal_data.get("rsi")

    try:
        # === 1. Star Quality Assessment ===
        rating_description = {
            5: "✅ *Masterclass Signal (5⭐)* – _Peak precision._",
            4: "✅ *Strong Setup (4⭐)* – _Very high probability._",
            3: "⚠️ *Moderate Setup (3⭐)* – _Confirmation recommended._",
        }.get(stars, "❌ *Weak Setup (<3⭐)* – _Risky environment._")

        # === 2. Confidence Scoring ===
        confidence_text = f"*Confidence:* `{confidence:.1f}%`"
        confidence_alert = "\n❗ *Low Confidence Warning (<55%).*" if confidence < 55 else ""

        # === 3. RSI Interpretation ===
        rsi_annotation = ""
        if isinstance(rsi, (int, float)):
            if rsi > 70:
                rsi_annotation = "\n🔴 *Overbought (>70 RSI)* – _Potential reversal risk._"
            elif rsi < 30:
                rsi_annotation = "\n🔵 *Oversold (<30 RSI)* – _Potential bounce risk._"

        # === 4. Trade Recommendation ===
        if stars == 5 and confidence >= 70:
            recommendation = "🚀 *Immediate Entry Recommended*"
        elif stars >= 4 and confidence >= 65:
            recommendation = "📈 *Good Opportunity (Monitor Closely)*"
        elif stars >= 3 and confidence >= 60:
            recommendation = "👀 *Potential Watchlist Candidate*"
        else:
            recommendation = "❌ *No Trade – Risk Dominates*"

        # === 5. Final Risk Message Composition ===
        risk_message = (
            f"⚡ *Risk Analysis*\n\n"
            f"*Pattern:* `{pattern}`\n"
            f"{confidence_text}\n"
            f"*Rating:* {'⭐' * stars}\n\n"
            f"{rating_description}"
            f"{confidence_alert}"
            f"{rsi_annotation}\n\n"
            f"📢 *Recommendation:* {recommendation}"
        )

        # === 6. Risk Flagging ===
        is_high_risk = stars < 3 or confidence < 55

        logger.info(f"[Risk Manager] Risk Evaluated: {pattern} | Stars={stars}⭐ | Confidence={confidence:.1f}%")

        return risk_message, is_high_risk

    except Exception as e:
        logger.error(f"[Risk Manager Critical Error] {e}")
        return "⚠️ *Risk Analysis Failed.* _Use maximum caution._", True
