# bot/engine/risk_manager.py

import logging

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async def assess_signal_risk(signal_data: dict) -> tuple:
    """
    Evaluates the trading signal and adds a risk warning if necessary.

    Args:
        signal_data (dict): The full result from analyze_symbol() including 'stars' rating.

    Returns:
        tuple: (message: str, warning: bool)
            - message: Additional message regarding the risk assessment
            - warning: True if increased risk detected
    """

    stars = signal_data.get("stars", 0)

    if stars >= 4:
        logger.info("High quality trade detected (4–5 stars).")
        return "✅ Good quality trade detected.", False

    elif stars == 3:
        logger.warning("Increased risk detected (3 stars).")
        warning_message = (
            "⚠️ *Increased risk detected: 3-star trade.*\n"
            "_Trade cautiously. Look for strong confirmations._"
        )
        return warning_message, True

    else:
        logger.warning("Low quality signal detected (below 3 stars).")
        return "⚠️ Trade signal below recommended quality threshold.", True
