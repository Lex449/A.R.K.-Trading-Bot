"""
A.R.K. Risk Manager – Ultra Premium Signal Risk Analyzer.
Evaluates signals based on Stars, Confidence, RSI, and generates smart trade advice.

Optimized for: Precision, Scalability, and Ultra-Fast Filtering.
"""

import logging

# Setup structured logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async def assess_signal_risk(signal_data: dict) -> tuple:
    """
    Evaluates a trading signal using:
    - Star Rating (Signal Quality)
    - Confidence % (Strength of the Pattern)
    - RSI Value (Overbought/Oversold Indicator)

    Returns:
        tuple: (Formatted Risk Message: str, Is High Risk: bool)
    """

    stars = signal_data.get("stars", 0)
    confidence = signal_data.get("confidence", 0.0)
    pattern = signal_data.get("pattern", "Unknown Pattern")
    rsi = signal_data.get("rsi")

    try:
        # === 1. Star Rating Analysis ===
        if stars == 5:
            rating_text = "✅ *Ultra High-Quality Signal (5⭐)* – _Technical Masterpiece._"
        elif stars == 4:
            rating_text = "✅ *Strong Signal (4⭐)* – _High probability trade._"
        elif stars == 3:
            rating_text = "⚠️ *Moderate Signal (3⭐)* – _Needs confirmation._"
        else:
            rating_text = "❌ *Weak Signal (<3⭐)* – _Trade not recommended._"

        # === 2. Confidence Analysis ===
        confidence_text = f"*Confidence:* `{confidence:.1f}%`"
        confidence_note = ""
        if confidence < 55:
            confidence_note = "\n❗ *Warning: Low Confidence (<55%).*"

        # === 3. RSI Zone Detection ===
        rsi_text = ""
        if isinstance(rsi, (int, float)):
            if rsi > 70:
                rsi_text = "\n🔴 *RSI: Overbought (>70)* – _Caution on Long entries._"
            elif rsi < 30:
                rsi_text = "\n🔵 *RSI: Oversold (<30)* – _Caution on Short entries._"

        # === 4. Suggested Trading Action ===
        if stars >= 4 and confidence >= 70:
            suggested_action = "🚀 *Strong Buy Setup*"
        elif stars >= 4 and confidence >= 60:
            suggested_action = "📈 *Potential Buy – Caution Advised*"
        elif stars == 3 and confidence >= 60:
            suggested_action = "👀 *Watchlist Candidate*"
        else:
            suggested_action = "❌ *Avoid Trade – Too Risky*"

        # === 5. Final Message Assembly ===
        final_message = (
            f"⚡ *Risk Analysis*\n\n"
            f"*Pattern:* `{pattern}`\n"
            f"{confidence_text}\n"
            f"*Rating:* {'⭐' * stars}\n\n"
            f"{rating_text}"
            f"{confidence_note}"
            f"{rsi_text}\n\n"
            f"📢 *Suggested Action:* {suggested_action}"
        )

        # === 6. High-Risk Flag Detection ===
        is_high_risk = stars < 3 or confidence < 55

        logger.info(f"[Risk Manager] Evaluated {pattern}: {stars}⭐, Confidence {confidence:.1f}%")

        return final_message, is_high_risk

    except Exception as e:
        logger.error(f"[Risk Manager Critical Error] {e}")
        return "⚠️ *Risk Analysis Failed.* _Trade at your own risk._", True
