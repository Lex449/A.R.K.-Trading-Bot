"""
A.R.K. Analysis Engine – Ultra Full Signal Suite 2.5.
Handles Candle Patterns, ATR Volatility, Risk-Reward Estimation, Deep Confidence Boosting – Modular, Scalable, Multilingual.
"""

import pandas as pd
from bot.engine.pattern_detector import detect_patterns
from bot.engine.volatility_detector import VolatilityDetector
from bot.engine.risk_reward_analyzer import RiskRewardAnalyzer
from bot.engine.data_loader import fetch_market_data
from bot.engine.deep_confidence_engine import adjust_confidence
from bot.utils.logger import setup_logger

# Setup Logger
logger = setup_logger(__name__)

# Instantiate Critical Engines
volatility_detector = VolatilityDetector()
risk_reward_analyzer = RiskRewardAnalyzer()

async def analyze_symbol(symbol: str, chat_id: int = None) -> dict:
    """
    Main Signal Analysis Function.
    """

    try:
        # === 1. Load Data
        df = await fetch_market_data(symbol, chat_id=chat_id)

        if df is None or len(df) < 20:
            logger.warning(f"[Analysis Engine] Insufficient data for {symbol}. Skipping.")
            return None

        # === 2. Detect Patterns
        patterns = detect_patterns(df)

        # === 3. Volatility Scan
        volatility_info = volatility_detector.detect_volatility_spike(df)

        # === 4. Determine Action
        combined_action = determine_action(patterns, volatility_info)

        # === 5. Estimate Risk-Reward
        risk_reward_info = risk_reward_analyzer.estimate(df, combined_action) if combined_action in ("Long 📈", "Short 📉") else None

        # === 6. Confidence Calculation
        raw_confidence = calculate_confidence(patterns)
        boosted_confidence = adjust_confidence(raw_confidence)

        # === 7. Build Final Response
        return {
            "symbol": symbol,
            "patterns": patterns,
            "avg_confidence": boosted_confidence,
            "combined_action": combined_action,
            "volatility_info": volatility_info,
            "risk_reward_info": risk_reward_info,
            "df": df,
        }

    except Exception as e:
        logger.error(f"❌ [Analysis Engine] Critical error analyzing {symbol}: {e}")
        return None

def determine_action(patterns: list, volatility_info: dict) -> str:
    """
    Determines strategic trading action.
    """
    strong_patterns = [p for p in patterns if "Bullish" in p]
    weak_patterns = [p for p in patterns if "Bearish" in p]
    volatility_strength = volatility_info.get("current_move_percent", 0) if volatility_info else 0

    if strong_patterns and volatility_strength >= 1.5:
        return "Long 📈"
    elif weak_patterns and volatility_strength >= 1.5:
        return "Short 📉"
    return "Neutral ⚪"

def calculate_confidence(patterns: list) -> float:
    """
    Calculates base confidence score.
    """
    if not patterns:
        return 0.0

    score = 0
    for p in patterns:
        score += {
            "⭐⭐⭐⭐⭐": 100,
            "⭐⭐⭐⭐": 80,
            "⭐⭐⭐": 60,
            "⭐⭐": 40
        }.get(p[p.find("⭐"):], 20)

    return round(score / len(patterns), 2)
