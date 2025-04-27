"""
A.R.K. ATR Engine – Volatility Precision Scanner.
Calculates Average True Range (ATR) based market volatility.

Engineered for: Ultra Precision, Risk-Reward Strategies, Early Move Detection.
"""

import pandas as pd

def calculate_atr(df: pd.DataFrame, period: int = 14) -> float:
    """
    Calculates the Average True Range (ATR) in percent.

    Args:
        df (pd.DataFrame): DataFrame containing 'high', 'low', and 'close' columns.
        period (int): Number of periods to use for ATR calculation (default = 14).

    Returns:
        float: ATR percentage relative to the last close price.
    """
    if df is None or len(df) < period:
        return 0.0

    df['high_low'] = df['high'] - df['low']
    df['high_close'] = (df['high'] - df['close'].shift()).abs()
    df['low_close'] = (df['low'] - df['close'].shift()).abs()

    df['true_range'] = df[['high_low', 'high_close', 'low_close']].max(axis=1)
    atr = df['true_range'].rolling(window=period).mean().iloc[-1]

    last_close = df['close'].iloc[-1]

    if last_close == 0:
        return 0.0

    atr_percent = (atr / last_close) * 100

    # Cleanup to avoid pollution
    df.drop(columns=['high_low', 'high_close', 'low_close', 'true_range'], inplace=True, errors='ignore')

    return round(atr_percent, 2)
