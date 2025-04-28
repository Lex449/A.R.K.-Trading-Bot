"""
A.R.K. Analysis Engine – Full Signal Suite.
Candle Patterns, ATR Volatility, Risk-Reward Profile – Modular und Ultra Stabil.
"""

import pandas as pd
from bot.engine.pattern_detector import detect_patterns
from bot.engine.volatility_detector import VolatilityDetector
from bot.engine.risk_reward_analyzer import RiskRewardAnalyzer
from bot.engine.data_loader import fetch_market_data

# Instanzen bauen
volatility_detector = VolatilityDetector()
risk_reward_analyzer = RiskRewardAnalyzer()

async def analyze_symbol(symbol: str) -> dict:
    df = await fetch_market_data(symbol)

    if df is None or len(df) < 20:
        return None

    patterns = detect_patterns(df)
    volatility_info = volatility_detector.detect_volatility_spike(df)
    combined_action = determine_action(patterns, volatility_info)
    risk_reward_info = risk_reward_analyzer.estimate(df, combined_action)

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
    strong_patterns = [p for p in patterns if "Bullish" in p]
    weak_patterns = [p for p in patterns if "Bearish" in p]
    volatility_strength = volatility_info.get("current_move_percent", 0) if volatility_info else 0

    if strong_patterns and volatility_strength >= 1.5:
        return "Ultra Long 📈"
    elif weak_patterns and volatility_strength >= 1.5:
        return "Ultra Short 📉"
    else:
        return "Neutral ⚪"

def calculate_confidence(patterns: list) -> float:
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
