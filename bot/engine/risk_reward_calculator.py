"""
A.R.K. Risk-Reward Calculator – Premium Smart Estimates.
Provides quick risk/reward insights based on current market behavior.
"""

import pandas as pd

def calculate_risk_reward(df: pd.DataFrame, action: str) -> dict:
    """
    Calculates simple risk/reward percentages based on last 20 candles.

    Args:
        df (pd.DataFrame): Market OHLCV data.
        action (str): Expected action ("Long" or "Short").

    Returns:
        dict or None: Risk/Reward estimation, or None if invalid input.
    """
    if df is None or df.empty or action not in ["Long", "Short"]:
        return None

    try:
        recent_high = df["h"].rolling(window=20, min_periods=1).max().iloc[-1]
        recent_low = df["l"].rolling(window=20, min_periods=1).min().iloc[-1]
        current_close = df["c"].iloc[-1]

        if current_close == 0:
            return None  # Sicherheitscheck: Keine Division durch Null

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
