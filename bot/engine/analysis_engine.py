"""
A.R.K. Analysis Engine – Full Signal Suite Ultra 2.1.
Handles Candle Patterns, ATR Volatility, Risk-Reward – Modular, Deep Learning Ready, Multilingual.
"""

import pandas as pd
from bot.engine.pattern_detector import detect_patterns
from bot.engine.volatility_detector import VolatilityDetector
from bot.engine.risk_reward_analyzer import RiskRewardAnalyzer
from bot.engine.data_loader import fetch_market_data
from bot.engine.deep_confidence_engine import adjust_confidence  # NEU: Deep Learning Boost
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# Instantiate once (Performance Optimierung)
volatility_detector = VolatilityDetector()
risk_reward_analyzer = RiskRewardAnalyzer()

async def analyze_symbol(symbol: str, chat_id: int = None) -> dict:
    """
    Master Analysis Function for a trading symbol.
    """

    try:
        # 1. Load Market Data
        df = await fetch_market_data(symbol, chat_id=chat_id)

        if df is None or len(df) < 20:
            logger.warning(f"[Analysis] Not enough data for {symbol}. Skipping.")
            return None

        # 2. Detect Patterns
        patterns = detect_patterns(df)

        # 3. Detect Volatility Spikes
        volatility_info = volatility_detector.detect_volatility_spike(df)

        # 4. Determine Combined Action (Long 📈, Short 📉, Neutral ⚪)
        combined_action = determine_action(patterns, volatility_info)

        # 5. Estimate Risk-Reward Ratio
        risk_reward_info = None
        if combined_action in ("Long 📈", "Short 📉"):
            risk_reward_info = risk_reward_analyzer.estimate(df, combined_action)

        # 6. Calculate and Boost Confidence Score
        raw_confidence = calculate_confidence(patterns)
        boosted_confidence = adjust_confidence(raw_confidence)  # Boosted Score

        return {
            "symbol": symbol,
            "patterns": patterns,
            "avg_confidence": boosted_confidence,  # WICHTIG: Deep-boosted Confidence
            "combined_action": combined_action,
            "volatility_info": volatility_info,
            "risk_reward_info": risk_reward_info,
            "df": df,
        }

    except Exception as e:
        logger.error(f"[Analysis] Error analyzing {symbol}: {e}")
        return None

def determine_action(patterns: list, volatility_info: dict) -> str:
    """
    Determines strategic trading action based on detected patterns and volatility.
    """
    strong_patterns = [p for p in patterns if "Bullish" in p]
    weak_patterns = [p for p in patterns if "Bearish" in p]

    volatility_strength = volatility_info.get("current_move_percent", 0) if volatility_info else 0

    if strong_patterns and volatility_strength >= 1.5:
        return "Long 📈"
    elif weak_patterns and volatility_strength >= 1.5:
        return "Short 📉"
    else:
        return "Neutral ⚪"

def calculate_confidence(patterns: list) -> float:
    """
    Calculates average signal confidence based on the pattern quality.
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

    return round(score / len(patterns), 2)
