"""
A.R.K. Risk-Reward Calculator – Ultra Precision Smart Estimator 2.0
Advanced risk/reward evaluation based on dynamic market behavior.
"""

import pandas as pd

def calculate_risk_reward(df: pd.DataFrame, action: str) -> dict | None:
    """
    Calculates dynamic risk/reward metrics using the last 20 candles.

    Args:
        df (pd.DataFrame): Market OHLCV data.
        action (str): "Long" or "Short" position expectation.

    Returns:
        dict: Risk/Reward estimates, or None if invalid input.
    """

    if df is None or df.empty or action not in ["Long", "Short"]:
        return None

    try:
        # Calculate local extrema
        recent_high = df["h"].rolling(window=20, min_periods=1).max().iloc[-1]
        recent_low = df["l"].rolling(window=20, min_periods=1).min().iloc[-1]
        current_close = df["c"].iloc[-1]

        if current_close <= 0:
            return None  # Defensive coding: invalid close price

        # Risk/Reward Calculation
        if action == "Long":
            risk = ((current_close - recent_low) / current_close) * 100
            reward = ((recent_high - current_close) / current_close) * 100
            stop_loss = recent_low
            target = recent_high
        else:  # Short
            risk = ((recent_high - current_close) / current_close) * 100
            reward = ((current_close - recent_low) / current_close) * 100
            stop_loss = recent_high
            target = recent_low

        risk_reward_ratio = (reward / risk) if risk > 0 else 0.0

        return {
            "risk_percent": round(risk, 2),
            "reward_percent": round(reward, 2),
            "risk_reward_ratio": round(risk_reward_ratio, 2),
            "stop_loss": round(stop_loss, 2),
            "target": round(target, 2),
        }

    except Exception:
        return None
