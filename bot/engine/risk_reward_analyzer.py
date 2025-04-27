"""
A.R.K. Risk-Reward Analyzer – Smart Trade Evaluation System.
Estimates realistic reward/risk ratios for better decision-making.
"""

import pandas as pd

def estimate_risk_reward(df: pd.DataFrame, combined_action: str) -> dict:
    """
    Estimates Risk/Reward Ratio based on recent volatility and trend direction.

    Args:
        df (pd.DataFrame): OHLCV DataFrame (latest candles).
        combined_action (str): Suggested trade direction ("Long" or "Short").

    Returns:
        dict: Estimated reward, risk, and R/R ratio.
    """

    if df is None or df.empty or combined_action not in ("Long 📈", "Short 📉"):
        return None

    try:
        recent_closes = df["c"].tail(20)
        recent_highs = df["h"].tail(20)
        recent_lows = df["l"].tail(20)

        current_price = recent_closes.iloc[-1]
        recent_high = recent_highs.max()
        recent_low = recent_lows.min()

        # Estimate stop-loss and target
        if combined_action == "Long 📈":
            stop_loss = recent_low * 0.995  # Tight stop 0.5% below support
            target = current_price * 1.015   # Modest target 1.5% above entry
        else:  # Short 📉
            stop_loss = recent_high * 1.005  # Tight stop 0.5% above resistance
            target = current_price * 0.985   # Modest target 1.5% below entry

        risk = abs(current_price - stop_loss)
        reward = abs(target - current_price)
        if risk == 0:
            return None  # Avoid division by zero

        risk_reward_ratio = round(reward / risk, 2)

        return {
            "current_price": current_price,
            "stop_loss": round(stop_loss, 2),
            "target": round(target, 2),
            "risk": round(risk, 2),
            "reward": round(reward, 2),
            "risk_reward_ratio": risk_reward_ratio
        }

    except Exception:
        return None
