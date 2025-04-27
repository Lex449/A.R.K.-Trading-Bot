"""
A.R.K. Risk-Reward Calculator – Premium Smart Estimates.
Helps evaluate optimal trade setups based on current price action.
"""

import pandas as pd

def calculate_risk_reward(df: pd.DataFrame, action: str) -> dict:
    """
    Calculates simple Risk/Reward estimates based on recent volatility.

    Args:
        df (pd.DataFrame): OHLCV DataFrame
        action (str): "Long" or "Short"

    Returns:
        dict: {risk: x%, reward: y%} or None if insufficient data
    """
    if df is None or df.empty or action not in ["Long", "Short"]:
        return None

    try:
        recent_high = df["h"].rolling(window=20, min_periods=1).max().iloc[-1]
        recent_low = df["l"].rolling(window=20, min_periods=1).min().iloc[-1]
        current_close = df["c"].iloc[-1]

        if action == "Long":
            risk = ((current_close - recent_low) / current_close) * 100
            reward = ((recent_high - current_close) / current_close) * 100
        else:  # Short
            risk = ((recent_high - current_close) / current_close) * 100
            reward = ((current_close - recent_low) / current_close) * 100

        return {
            "risk_percent": round(risk, 2),
            "reward_percent": round(reward, 2)
        }

    except Exception:
        return None
