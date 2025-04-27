# bot/engine/indicator_engine.py

"""
Ultra Indicator Engine für EMA-, RSI- und Trendauswertung.
Designed für A.R.K. Masterclass Analyse-System.
"""

import pandas as pd
import numpy as np

def evaluate_indicators(df: pd.DataFrame) -> tuple:
    """
    Berechnet EMA, RSI und Trendrichtung auf Basis der Candle-Daten.

    Args:
        df (pd.DataFrame): Candle-Daten mit Spalten ['o', 'h', 'l', 'c'].

    Returns:
        tuple: (Score 0–100, Trendrichtung "Long 📈", "Short 📉" oder "Neutral ⚪")
    """
    if df.empty or len(df) < 20:
        return 50, "Neutral ⚪"  # Bei zu wenig Daten neutrale Basisbewertung

    # === EMA Berechnung (Trendrichtung) ===
    df['EMA_9'] = df['c'].ewm(span=9, adjust=False).mean()
    df['EMA_21'] = df['c'].ewm(span=21, adjust=False).mean()

    last_close = df['c'].iloc[-1]
    last_ema9 = df['EMA_9'].iloc[-1]
    last_ema21 = df['EMA_21'].iloc[-1]

    trend = "Neutral ⚪"
    if last_ema9 > last_ema21:
        trend = "Long 📈"
    elif last_ema9 < last_ema21:
        trend = "Short 📉"

    # === RSI Berechnung (Momentum) ===
    delta = df['c'].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    avg_gain = pd.Series(gain).rolling(window=14).mean().iloc[-1]
    avg_loss = pd.Series(loss).rolling(window=14).mean().iloc[-1]

    if avg_loss == 0:
        rsi = 100
    else:
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

    # === Score bestimmen ===
    indicator_score = 50

    # EMA Gewichtung
    if trend == "Long 📈":
        indicator_score += 20
    elif trend == "Short 📉":
        indicator_score -= 20

    # RSI Gewichtung
    if rsi > 70:
        indicator_score -= 10  # Überkauft → Risiko Short
    elif rsi < 30:
        indicator_score += 10  # Überverkauft → Chance Long

    indicator_score = max(0, min(100, indicator_score))  # Begrenzung auf 0–100

    return round(indicator_score, 2), trend
