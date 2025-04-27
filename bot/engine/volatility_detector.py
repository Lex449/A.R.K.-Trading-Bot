"""
A.R.K. Volatility Detector – Advanced Dynamic Volatility Analysis.
Combines ATR, Candlestick Behavior, and Trend Confirmation.

Objective: Detect prime trading setups with maximum precision.
"""

import pandas as pd
from bot.engine.atr_engine import calculate_atr

async def detect_volatility(df: pd.DataFrame) -> dict:
    """
    Detects significant volatility spikes and optimal trading setups.

    Args:
        df (pd.DataFrame): Market candlestick data.

    Returns:
        dict: Detection result including move info, volatility rating, and trend suggestion.
    """
    if df is None or len(df) < 20:
        return {"volatility_spike": False, "atr": 0.0, "trend": "Neutral ⚪", "signal_quality": "Low ⚠️"}

    # === Calculate Core Metrics ===
    atr_percent = calculate_atr(df)
    last_candle = df.iloc[-1]
    previous_candle = df.iloc[-2]

    # === Move Detection ===
    move_percent = ((last_candle['close'] - previous_candle['close']) / previous_candle['close']) * 100

    # === Trend Identification (Simple EMA Method) ===
    trend = "Neutral ⚪"
    if df['close'].rolling(20).mean().iloc[-1] < last_candle['close']:
        trend = "Long Bias 📈"
    elif df['close'].rolling(20).mean().iloc[-1] > last_candle['close']:
        trend = "Short Bias 📉"

    # === Volatility Spike Detection ===
    volatility_spike = atr_percent > 2.0  # Threshold for real action (can be tuned)

    # === Signal Quality Estimation ===
    if abs(move_percent) > 1.5 and volatility_spike:
        signal_quality = "Strong 🔥"
    elif abs(move_percent) > 1.0:
        signal_quality = "Medium ⚡"
    else:
        signal_quality = "Low ⚠️"

    return {
        "volatility_spike": volatility_spike,
        "atr": round(atr_percent, 2),
        "trend": trend,
        "signal_quality": signal_quality,
        "last_move_percent": round(move_percent, 2),
    }
