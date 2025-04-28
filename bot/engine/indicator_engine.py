"""
A.R.K. Indicator Engine – Ultra Precision 3.0
Calculates EMAs, RSI momentum, and dynamic trend detection for elite trading decisions.

Built for: Scalability, Fault Tolerance, and Strategic Signal Scoring.
"""

import pandas as pd
import numpy as np

def evaluate_indicators(df: pd.DataFrame) -> tuple:
    """
    Evaluates market momentum based on EMA crossovers and RSI levels.

    Args:
        df (pd.DataFrame): DataFrame with 'o', 'h', 'l', 'c' columns (candlestick data).

    Returns:
        tuple: (Indicator Score [0–100], Trend Direction: "Long 📈", "Short 📉", "Neutral ⚪")
    """

    if df is None or df.empty or len(df) < 20:
        return 50.0, "Neutral ⚪"  # Default if not enough data

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
        gain = np.maximum(delta, 0)
        loss = np.abs(np.minimum(delta, 0))

        avg_gain = pd.Series(gain).rolling(window=14, min_periods=14).mean().iloc[-1]
        avg_loss = pd.Series(loss).rolling(window=14, min_periods=14).mean().iloc[-1]

        rsi = 100.0 if avg_loss == 0 else 100 - (100 / (1 + (avg_gain / avg_loss)))

        # === Base Score ===
        indicator_score = 50.0

        # === EMA Influence ===
        if trend == "Long 📈":
            indicator_score += 20
        elif trend == "Short 📉":
            indicator_score -= 20

        # === RSI Influence ===
        if rsi > 70:
            indicator_score -= 10  # Overbought → Higher reversal risk
        elif rsi < 30:
            indicator_score += 10  # Oversold → Higher bounce chance

        # === Finalize Score ===
        indicator_score = round(max(0, min(100, indicator_score)), 2)

        return indicator_score, trend

    except Exception:
        # Safe fallback
        return 50.0, "Neutral ⚪"
