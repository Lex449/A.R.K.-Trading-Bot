"""
A.R.K. ATR Detector – Detects large True Range movements.
"""

def detect_atr_breakout(df, atr_multiplier=1.5):
    """
    Detects ATR breakouts (high volatility candles).
    Args:
        df (DataFrame): Market data.
        atr_multiplier (float): Factor over average True Range to trigger.

    Returns:
        dict or None
    """
    if df is None or df.empty or not {"high", "low", "close"}.issubset(df.columns):
        return None

    df["tr"] = df[["high", "close"]].max(axis=1) - df[["low", "close"]].min(axis=1)
    atr = df["tr"].rolling(window=14).mean().iloc[-1]
    latest_tr = df["tr"].iloc[-1]

    if latest_tr >= atr * atr_multiplier:
        return {
            "atr_breakout": True,
            "atr_ratio": (latest_tr / atr) * 100
        }

    return None
