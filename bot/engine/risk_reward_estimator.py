"""
A.R.K. Risk-Reward Estimator – Ultra Precision 3.0
Calculates professional-grade risk/reward setups based on dynamic market structure.

Engineered for: Scalability, Safety, and Future AI Integrations.
"""

import pandas as pd

def estimate_risk_reward(df: pd.DataFrame, entry_price: float, direction: str) -> dict:
    """
    Calculates dynamic risk/reward metrics from recent OHLCV market data.

    Args:
        df (pd.DataFrame): DataFrame containing 'h', 'l' columns.
        entry_price (float): The planned entry price for the trade.
        direction (str): 'long' or 'short' (case-insensitive).

    Returns:
        dict: {
            "risk": float (absolute value),
            "reward": float (absolute value),
            "rr_ratio": float (Reward/Risk Ratio)
        }
        or safe nulls if invalid.
    """

    if df is None or df.empty or entry_price <= 0 or direction.lower() not in {"long", "short"}:
        return {"risk": None, "reward": None, "rr_ratio": None}

    try:
        # Fetch key points from last 20 candles
        recent_high = df["h"].tail(20).max()
        recent_low = df["l"].tail(20).min()

        if pd.isna(recent_high) or pd.isna(recent_low):
            return {"risk": None, "reward": None, "rr_ratio": None}

        # Calculate risk and reward
        if direction.lower() == "long":
            risk = max(entry_price - recent_low, 0)
            reward = max(recent_high - entry_price, 0)
        else:  # short
            risk = max(recent_high - entry_price, 0)
            reward = max(entry_price - recent_low, 0)

        if risk == 0 or reward == 0:
            return {"risk": None, "reward": None, "rr_ratio": None}

        rr_ratio = round(reward / risk, 2)

        return {
            "risk": round(risk, 4),
            "reward": round(reward, 4),
            "rr_ratio": rr_ratio
        }

    except Exception as e:
        # Safe fallback
        return {"risk": None, "reward": None, "rr_ratio": None}
