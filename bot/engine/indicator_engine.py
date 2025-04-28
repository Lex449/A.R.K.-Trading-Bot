"""
A.R.K. Indicator Engine – Ultra Masterclass Build.
Calculates EMA-based trend and RSI-based momentum for premium trading signals.
"""

import pandas as pd
import numpy as np

def evaluate_indicators(df: pd.DataFrame) -> tuple:
    """
    Calculates EMA, RSI, and trend direction based on candle data.

    Args:
        df (pd.DataFrame): Candle data with columns ['o', 'h', 'l', 'c'].

    Returns:
        tuple: (Indicator Score 0–100, Trend Direction ["Long 📈", "Short 📉", "Neutral ⚪"])
    """
    if df is None or df.empty or len(df) < 20:
        return 50.0, "Neutral ⚪"  # Neutral base score if insufficient data

    try:
        # === Calculate EMAs ===
        df["EMA_9"] = df["c"].ewm(span=9, adjust=False).mean()
        df["EMA_21"] = df["c"].ewm(span=21, adjust=False).mean()

        last_close = df["c"].iloc[-1]
        last_ema9 = df["EMA_9"].iloc[-1]
        last_ema21 = df["EMA_21"].iloc[-1]

        # === Determine Trend ===
        if last_ema9 > last_ema21:
            trend = "Long 📈"
        elif last_ema9 < last_ema21:
            trend = "Short 📉"
        else:
            trend = "Neutral ⚪"

        # === Calculate RSI ===
        delta = df["c"].diff()
        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)

        avg_gain = pd.Series(gain).rolling(window=14, min_periods=1).mean().iloc[-1]
        avg_loss = pd.Series(loss).rolling(window=14, min_periods=1).mean().iloc[-1]

        if avg_loss == 0:
            rsi = 100.0
        else:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))

        # === Calculate Indicator Score ===
        indicator_score = 50.0

        # EMA Weight
        if trend == "Long 📈":
            indicator_score += 20
        elif trend == "Short 📉":
            indicator_score -= 20

        # RSI Weight
        if rsi > 70:
            indicator_score -= 10  # Overbought → Potential Short Risk
        elif rsi < 30:
            indicator_score += 10  # Oversold → Potential Long Chance

        indicator_score = max(0, min(100, indicator_score))  # Bound between 0–100

        return round(indicator_score, 2), trend

    except Exception:
        return 50.0, "Neutral ⚪"
