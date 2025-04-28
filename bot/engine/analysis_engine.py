"""
A.R.K. Analysis Engine – Full Signal Suite.
Candle Patterns, ATR Volatility, Risk-Reward Profile – Modular und Ultra Stabil.
"""

import pandas as pd
from bot.engine.pattern_detector import detect_patterns
from bot.engine.volatility_detector import detect_volatility
from bot.engine.risk_reward_analyzer import assess_risk_reward
from bot.engine.data_loader import fetch_market_data

async def analyze_symbol(symbol: str) -> dict:
    """
    Master Function: Analysiert ein Symbol umfassend.

    Args:
        symbol (str): Trading-Symbol (z.B. AAPL, TSLA).

    Returns:
        dict: Vollständiges Analysepaket oder None bei Fehlern.
    """
    # === 1. Daten abrufen ===
    df = await fetch_market_data(symbol)

    if df is None or len(df) < 20:
        return None

    # === 2. Mustererkennung ===
    patterns = detect_patterns(df)

    # === 3. Volatilitätsanalyse ===
    volatility_info = await detect_volatility(df)

    # === 4. Risiko-Rendite-Bewertung ===
    risk_reward_info = await assess_risk_reward(df)

    # === 5. Entscheidungslogik ===
    combined_action = determine_action(patterns, volatility_info)

    avg_confidence = calculate_confidence(patterns)

    return {
        "symbol": symbol,
        "patterns": patterns,
        "avg_confidence": avg_confidence,
        "combined_action": combined_action,
        "volatility_info": volatility_info,
        "risk_reward_info": risk_reward_info,
        "df": df,
    }

def determine_action(patterns: list, volatility_info: dict) -> str:
    """
    Leitet die Aktion (Long, Short, Neutral) basierend auf Mustern und Volatilität ab.

    Returns:
        str: Handlungsempfehlung.
    """
    strong_patterns = [p for p in patterns if "Bullish" in p]
    weak_patterns = [p for p in patterns if "Bearish" in p]

    volatility_strength = volatility_info.get("atr_percent", 0)

    if strong_patterns and volatility_strength >= 1.5:
        return "Ultra Long 📈"
    elif weak_patterns and volatility_strength >= 1.5:
        return "Ultra Short 📉"
    else:
        return "Neutral ⚪"

def calculate_confidence(patterns: list) -> float:
    """
    Berechnet die durchschnittliche Signalstärke basierend auf den Pattern-Bewertungen.

    Returns:
        float: Durchschnittliches Vertrauensniveau.
    """
    if not patterns:
        return 0.0

    score = 0
    for p in patterns:
        if "⭐⭐⭐⭐⭐" in p:
            score += 100
        elif "⭐⭐⭐⭐" in p:
            score += 80
        elif "⭐⭐⭐" in p:
            score += 60
        elif "⭐⭐" in p:
            score += 40
        else:
            score += 20

    return score / len(patterns)
