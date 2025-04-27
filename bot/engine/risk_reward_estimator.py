"""
A.R.K. Risk-Reward Estimator – Evaluates Trade Potential Ultra-Precisely.
Premium build: Clean, scalable, and ready for future AI expansion.
"""

import pandas as pd

def estimate_risk_reward(df: pd.DataFrame, entry_price: float, direction: str) -> dict:
    """
    Estimates risk and reward levels based on recent volatility and structure.

    Args:
        df (pd.DataFrame): OHLCV DataFrame.
        entry_price (float): Intended entry price.
        direction (str): "long" or "short".

    Returns:
        dict: risk, reward, and risk-reward ratio.
    """
    if df is None or df.empty:
        return {"risk": None, "reward": None, "rr_ratio": None}

    try:
        recent_high = df["h"].tail(20).max()
        recent_low = df["l"].tail(20).min()

        if direction.lower() == "long":
            risk = entry_price - recent_low
            reward = recent_high - entry_price
        elif direction.lower() == "short":
            risk = recent_high - entry_price
            reward = entry_price - recent_low
        else:
            return {"risk": None, "reward": None, "rr_ratio": None}

        if risk <= 0 or reward <= 0:
            return {"risk": None, "reward": None, "rr_ratio": None}

        rr_ratio = round(reward / risk, 2)

        return {
            "risk": round(risk, 2),
            "reward": round(reward, 2),
            "rr_ratio": rr_ratio
        }

    except Exception:
        return {"risk": None, "reward": None, "rr_ratio": None}
