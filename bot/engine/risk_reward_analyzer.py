"""
A.R.K. Risk-Reward Analyzer – Dynamic Signal Risk Evaluation.
Evaluates every detected signal based on logical RRR estimation.
"""

import pandas as pd

async def assess_risk_reward(df: pd.DataFrame) -> dict:
    """
    Evaluates the risk-reward ratio of the latest detected setup.

    Args:
        df (pd.DataFrame): Market candlestick data.

    Returns:
        dict: RRR estimation including recommended stop-loss, take-profit and risk evaluation.
    """
    if df is None or len(df) < 20:
        return {"rrr_status": "Insufficient Data", "stop_loss": None, "take_profit": None}

    # === Get last closed candle ===
    last_candle = df.iloc[-1]

    # === Define basic risk thresholds ===
    close_price = last_candle['close']
    candle_range = last_candle['high'] - last_candle['low']

    # === Basic Risk Management Estimations ===
    stop_loss = round(close_price - (candle_range * 1.5), 2)  # 1.5x last candle range below
    take_profit = round(close_price + (candle_range * 3), 2)  # 3x last candle range above

    # === Risk-Reward Ratio Calculation ===
    risk = close_price - stop_loss
    reward = take_profit - close_price

    if risk <= 0:
        return {"rrr_status": "Invalid Setup", "stop_loss": None, "take_profit": None}

    risk_reward_ratio = reward / risk

    # === Categorize RRR ===
    if risk_reward_ratio >= 3.0:
        rrr_status = "Excellent ✅"
    elif risk_reward_ratio >= 2.0:
        rrr_status = "Good 👍"
    elif risk_reward_ratio >= 1.5:
        rrr_status = "Acceptable ⚠️"
    else:
        rrr_status = "Risky ❌"

    return {
        "rrr_status": rrr_status,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "risk_reward_ratio": round(risk_reward_ratio, 2),
    }
