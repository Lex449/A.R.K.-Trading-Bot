# bot/engine/risk_manager.py

import logging
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

async def assess_signal_risk(signal_data: dict) -> tuple:
    """
    Evaluates a trading signal based on its 'stars' and 'rsi' rating
    and generates an intelligent risk advisory.

    Args:
        signal_data (dict): Full analysis result from analyze_symbol() including 'stars' and 'rsi'.

    Returns:
        tuple:
            - message (str): Risk advisory message
            - warning (bool): True if increased risk detected
    """
    try:
        stars = signal_data.get("stars", 0)
        rsi = signal_data.get("rsi", None)

        # === Evaluation Logic ===
        if stars >= 5:
            logger.info("[Risk Manager] ✅ Ultra high quality signal (5⭐).")
            return (
                "✅ *Ultra high quality trade detected (5⭐).* _Excellent technical alignment._",
                False
            )

        if stars == 4:
            logger.info("[Risk Manager] ✅ Strong trade detected (4⭐).")
            return (
                "✅ *Strong quality trade detected (4⭐).* _Solid conditions overall._",
                False
            )

        if stars == 3:
            logger.warning("[Risk Manager] ⚠️ Medium risk trade (3⭐). Caution advised.")
            rsi_warning = ""

            if rsi is not None:
                if rsi > 70:
                    rsi_warning = "\n🔴 *RSI Alert:* Overbought (>70). Increased reversal risk."
                elif rsi < 30:
                    rsi_warning = "\n🔵 *RSI Alert:* Oversold (<30). Increased rebound probability."

            return (
                "⚠️ *Medium risk trade detected (3⭐).* _Confirm with extra indicators._" + rsi_warning,
                True
            )

        logger.warning("[Risk Manager] ❌ Very low quality signal (<3⭐). Not recommended.")
        return (
            "❌ *Low quality trade detected (<3⭐).* _Entry not advised unless strong other factors exist._",
            True
        )

    except Exception as e:
        logger.error(f"[Risk Manager Error] {str(e)}")
        return (
            "⚠️ *Risk evaluation error.* _Proceed cautiously._",
            True
        )
