# bot/engine/analysis_engine.py

"""
A.R.K. Analysis Engine – Ultra Full Signal Suite 6.1 Final Build
Handles Patterns, Trend, Volume, Volatility, Risk-Reward, Confidence Boost – Modular, Scalable, Premium-Grade.

Made in Bali. Engineered with German Precision.
"""

import pandas as pd
from bot.engine.pattern_analysis_engine import detect_patterns, evaluate_indicators
from bot.engine.volume_spike_detector import detect_volume_spike
from bot.engine.adaptive_trend_detector import detect_adaptive_trend
from bot.engine.confidence_optimizer import optimize_confidence
from bot.engine.signal_category_engine import categorize_signal
from bot.engine.data_loader import fetch_market_data
from bot.engine.data_auto_validator import validate_market_data
from bot.engine.risk_engine import analyze_risk_reward
from bot.utils.logger import setup_logger

# Setup Logger
logger = setup_logger(__name__)

async def analyze_symbol(symbol: str, chat_id: int = None) -> dict | None:
    """
    Core Ultra Signal Analyzer for A.R.K.
    """

    try:
        # === 1. Daten Laden
        df = await fetch_market_data(symbol, chat_id=chat_id)

        if not validate_market_data(df):
            logger.warning(f"🚫 [AnalysisEngine] Data validation failed for {symbol}. Skipping.")
            return None

        # === 2. Mustererkennung
        patterns = detect_patterns(df)

        # === 3. Volumen Spike Detection
        volume_info = detect_volume_spike(df)

        # === 4. Adaptive Trend Detection
        trend_info = detect_adaptive_trend(df)

        # === 5. Indikator Evaluierung
        indicator_score, trend_direction = evaluate_indicators(df)

        # === 6. Bestimme Handlung
        combined_action = determine_action(patterns, trend_info)

        # === 7. Risiko-/Chance Analyse
        risk_reward_info = (
            analyze_risk_reward(df, combined_action)
            if combined_action in ("Long 📈", "Short 📉")
            else None
        )

        # === 8. Confidence Optimierung
        base_confidence = calculate_confidence(patterns)
        final_confidence = optimize_confidence(base_confidence, trend_info)

        # === 9. Signal Kategorisierung
        signal_category = categorize_signal(final_confidence)

        # === 10. Finales Response-Building
        result = {
            "symbol": symbol,
            "patterns": patterns,
            "avg_confidence": final_confidence,
            "combined_action": combined_action,
            "signal_category": signal_category,
            "indicator_score": indicator_score,
            "trend_direction": trend_direction,
            "volume_info": volume_info,
            "trend_info": trend_info,
            "risk_reward_info": risk_reward_info,
            "df": df,
        }

        logger.info(f"✅ [AnalysisEngine] {symbol} → {combined_action} | Confidence: {final_confidence:.2f}%")
        return result

    except Exception as e:
        logger.error(f"❌ [AnalysisEngine Critical Error] while analyzing {symbol}: {e}")
        return None

def determine_action(patterns: list, trend_info: dict) -> str:
    """
    Determines the strategic trading direction.
    """

    strong_bullish = any(p.get("action", "").startswith("Long") for p in patterns)
    strong_bearish = any(p.get("action", "").startswith("Short") for p in patterns)

    early_trend = trend_info.get("trend") if trend_info else None

    if strong_bullish and early_trend == "bullish":
        return "Long 📈"
    elif strong_bearish and early_trend == "bearish":
        return "Short 📉"
    return "Neutral ⚪"

def calculate_confidence(patterns: list) -> float:
    """
    Calculates the base confidence score from detected patterns.
    """

    if not patterns:
        return 0.0

    total_confidence = sum(p.get("confidence", 50) for p in patterns)
    average_confidence = total_confidence / len(patterns)
    return round(average_confidence, 2)
