"""
A.R.K. Volatility Detector – Ultra Dynamic Move Recognition.
Detects strong price movements + volume surges with ATR smart confirmation.
"""

import pandas as pd

async def detect_volatility(df: pd.DataFrame) -> dict:
    """
    Analyzes the last 30 candles for high volatility movements.
    
    Args:
        df (pd.DataFrame): Candle DataFrame (o, h, l, c, v)
    
    Returns:
        dict or None: Move Alert Data
    """
    if df is None or df.empty:
        return None

    try:
        df['range'] = df['h'] - df['l']
        df['atr'] = df['range'].rolling(window=14).mean()

        last_close = df['c'].iloc[-1]
        prev_close = df['c'].iloc[-2]
        move_percent = ((last_close - prev_close) / prev_close) * 100

        last_volume = df['v'].iloc[-1]
        avg_volume = df['v'].rolling(window=20).mean().iloc[-1]
        volume_spike = ((last_volume - avg_volume) / avg_volume) * 100

        atr_last = df['atr'].iloc[-1]
        volatility_condition = df['range'].iloc[-1] > atr_last * 1.2

        if abs(move_percent) >= 1.0 and volatility_condition:
            trend = "Long 📈" if move_percent > 0 else "Short 📉"

            return {
                "move_percent": move_percent,
                "volume_spike": volume_spike,
                "trend": trend,
                "volatility_validated": True
            }
        else:
            return None

    except Exception:
        return None
