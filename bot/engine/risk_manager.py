# bot/engine/risk_manager.py

import logging

# Setup Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async def assess_signal_risk(signal_data: dict) -> tuple:
    """
    Evaluates a trading signal based on stars, detected patterns, and RSI.
    Returns a formatted message and a warning flag if caution is needed.
    """

    stars = signal_data.get("stars", 0)
    confidence = signal_data.get("confidence", 0)
    pattern = signal_data.get("pattern", "Unknown")
    rsi = signal_data.get("rsi", None)

    try:
        # === Basic Evaluation based on Stars ===
        if stars >= 5:
            rating_text = "✅ *Ultra high quality signal (5⭐).* _Ideal technical alignment._"
        elif stars == 4:
            rating_text = "✅ *Strong quality signal (4⭐).* _Good conditions overall._"
        elif stars == 3:
            rating_text = "⚠️ *Moderate quality signal (3⭐).* _Caution advised. Confirm with extra factors._"
        elif stars == 2:
            rating_text = "❗ *Weak quality signal (2⭐).* _High caution required. Check additional indicators._"
        else:
            rating_text = "❌ *Very low quality signal (1⭐).* _Trade not recommended._"

        # === Confidence Evaluation ===
        confidence_warning = ""
        if confidence < 55:
            confidence_warning = "\n❗ *Low Confidence Alert (<55%).* _Consider avoiding this setup._"

        # === RSI Evaluation ===
        rsi_warning = ""
        if rsi is not None:
            if rsi > 70:
                rsi_warning = "\n🔴 *RSI Warning:* Market potentially overbought (>70)."
            elif rsi < 30:
                rsi_warning = "\n🔵 *RSI Warning:* Market potentially oversold (<30)."

        # === Suggested Action ===
        suggested_action = "Hold ⚪"
        if stars >= 4 and confidence >= 70:
            suggested_action = "Strong Buy 📈"
        elif stars >= 4 and confidence < 70:
            suggested_action = "Buy 📈 (with Caution)"
        elif stars <= 2:
            suggested_action = "Avoid ❌"

        # === Assembling the final Risk Message ===
        final_message = (
            f"⚡ *Risk Analysis*\n\n"
            f"*Pattern Detected:* {pattern}\n"
            f"*Confidence Level:* {confidence:.1f}%\n"
            f"*Rating:* {'⭐' * stars}\n\n"
            f"{rating_text}"
            f"{confidence_warning}"
            f"{rsi_warning}\n\n"
            f"📢 *Suggested Action:* {suggested_action}"
        )

        # === Define if warning should be flagged ===
        is_warning = True if stars <= 2 or confidence < 60 else False

        logger.info(f"[Risk Manager] Pattern: {pattern}, Stars: {stars}, Confidence: {confidence}%")
        return final_message, is_warning

    except Exception as e:
        logger.error(f"[Risk Manager Error] {str(e)}")
        return "⚠️ *Risk analysis error.* _Proceed cautiously._", True
