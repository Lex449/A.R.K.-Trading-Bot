# bot/engine/risk_manager.py

import logging

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async def assess_signal_risk(signal_data: dict) -> tuple:
    """
    Evaluates a trading signal based on its 'stars' rating
    and generates an appropriate risk warning.

    Args:
        signal_data (dict): The full result dictionary from analyze_symbol() including 'stars'.

    Returns:
        tuple:
            - message (str): Risk advisory message
            - warning (bool): True if increased risk detected
    """

    stars = signal_data.get("stars", 0)
    rsi = signal_data.get("rsi", None)

    if stars >= 5:
        logger.info("✅ Ultra high quality signal (5 stars). Minimal additional risk.")
        return "✅ *Ultra high quality trade detected (5⭐).* _Excellent technical alignment._", False

    elif stars == 4:
        logger.info("✅ Solid high quality trade (4 stars).")
        return "✅ *Good quality trade detected (4⭐).* _Conditions are favorable._", False

    elif stars == 3:
        logger.warning("⚠️ Medium quality trade (3 stars). Increased caution advised.")
        rsi_warning = ""
        if rsi:
            if rsi > 70:
                rsi_warning = "\n🔴 *RSI is high (>70)* – market could be overbought."
            elif rsi < 30:
                rsi_warning = "\n🔵 *RSI is low (<30)* – market could be oversold."

        warning_message = (
            "⚠️ *Moderate risk detected (3-star trade).*"
            "\n_Confirm additional indicators before entry._" +
            rsi_warning
        )
        return warning_message, True

    else:
        logger.warning("❌ Very low quality signal detected (<3 stars). Entry not advised.")
        return (
            "❌ *Low quality trade detected (<3⭐).*\n"
            "_Entry is highly discouraged unless other strong factors are present._",
            True
        )
