"""
A.R.K. Risk-Reward Calculator – Estimates simple risk/reward ratios.
"""

def estimate_risk_reward(trend_direction):
    """
    Provides simple risk-reward estimation.
    Args:
        trend_direction (str): "long", "short", "neutral"

    Returns:
        str
    """
    if trend_direction == "long":
        return "Risk-Reward approx. 1:2 📈"
    elif trend_direction == "short":
        return "Risk-Reward approx. 1:1.5 📉"
    else:
        return "Neutral conditions ⚪️ – Caution advised."
