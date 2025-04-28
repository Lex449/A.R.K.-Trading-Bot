"""
A.R.K. Risk-Reward Estimator – Evaluates Trade Potential Ultra-Precisely.
Premium build: Clean, scalable, and ready for future AI expansion.
"""

import pandas as pd

def estimate_risk_reward(df: pd.DataFrame, entry_price: float, direction: str) -> dict:
    """
    Estimates risk and reward levels based on recent volatility and price structure.

    Args:
        df (pd.DataFrame): OHLCV DataFrame with 'h', 'l' columns.
        entry_price (float): Intended entry price for the trade.
        direction (str): "long" or "short" indicating trade direction.

    Returns:
        dict: Risk value, Reward value, Risk-Reward ratio.
    """
    if df is None or df.empty or entry_price <= 0:
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
            "risk": round(risk, 4),
            "reward": round(reward, 4),
            "rr_ratio": rr_ratio
        }

    except Exception:
        return {"risk": None, "reward": None, "rr_ratio": None}
