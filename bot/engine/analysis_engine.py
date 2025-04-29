# bot/engine/analysis_engine.py

"""
A.R.K. Analysis Engine – Ultra Full Signal Suite 6.0
Handles Candle Patterns, Volatility Detection, Risk-Reward Estimation,
Volume Spike Detection, Trend Early Warning, Confidence Boosting – Modular, Scalable, Multilingual, Adaptive.

Made for: Flawless Signal Mastery, Next-Gen Automation, and Institutional-Grade Risk Management.
"""

import pandas as pd
from bot.engine.pattern_analysis_engine import detect_patterns, evaluate_indicators
from bot.engine.volatility_detector import VolatilityDetector
from bot.engine.risk_engine import RiskRewardAnalyzer
from bot.engine.volume_spike_detector import detect_volume_spike
from bot.engine.adaptive_trend_detector import detect_multifactor_trend
from bot.engine.confidence_optimizer import optimize_confidence
from bot.engine.signal_category_engine import categorize_signal
from bot.engine.data_loader import fetch_market_data
from bot.engine.data_auto_validator import validate_market_data
from bot.utils.logger import setup_logger

# Logger Setup
logger = setup_logger(__name__)

# Engine Instanzen
volatility_detector = VolatilityDetector()
risk_analyzer = RiskRewardAnalyzer()

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

        # === 3. Volatilitätserkennung
        volatility_info = volatility_detector.detect_volatility_spike(df)

        # === 4. Volumen Spike Detection
        volume_info = detect_volume_spike(df)

        # === 5. Multifaktor Trend Erkennung
        trend_info = detect_multifactor_trend(df)

        # === 6. Indikatoren Evaluierung
        indicator_score, trend_direction = evaluate_indicators(df)

        # === 7. Bestimme Handlung
        combined_action = determine_action(patterns, volatility_info, trend_info)

        # === 8. Risiko-/Chance-Analyse
        risk_reward_info = (
            risk_analyzer.estimate(df, combined_action)
            if combined_action in ("Long 📈", "Short 📉")
            else None
        )

        # === 9. Confidence Optimierung
        base_confidence = calculate_confidence(patterns)
        final_confidence = optimize_confidence(base_confidence, volatility_info, trend_info)

        # === 10. Signal-Kategorisierung
        signal_category = categorize_signal(final_confidence)

        # === 11. Finales Response-Building
        result = {
            "symbol": symbol,
            "patterns": patterns,
            "avg_confidence": final_confidence,
            "combined_action": combined_action,
            "signal_category": signal_category,
            "indicator_score": indicator_score,
            "trend_direction": trend_direction,
            "volatility_info": volatility_info,
            "volume_info": volume_info,
            "trend_info": trend_info,
            "risk_reward_info": risk_reward_info,
            "df": df,
        }

        logger.info(f"✅ [AnalysisEngine] {symbol} ready: {combined_action} | {final_confidence:.2f}% confidence.")
        return result

    except Exception as e:
        logger.error(f"❌ [AnalysisEngine Critical Error] while analyzing {symbol}: {e}")
        return None

def determine_action(patterns: list, volatility_info: dict, trend_info: dict) -> str:
    """
    Determines the strategic trading direction.
    """

    strong_bullish = any(p.get("action", "").startswith("Long") for p in patterns)
    strong_bearish = any(p.get("action", "").startswith("Short") for p in patterns)

    volatility_spike = volatility_info.get("volatility_spike") if volatility_info else False
    early_trend = trend_info.get("early_trend") if trend_info else None

    if strong_bullish and (volatility_spike or early_trend == "bullish"):
        return "Long 📈"
    elif strong_bearish and (volatility_spike or early_trend == "bearish"):
        return "Short 📉"
    return "Neutral ⚪"

def calculate_confidence(patterns: list) -> float:
    """
    Calculates the base confidence score from detected patterns.
    """

    if not patterns:
        return 0.0

    total = sum(p.get("confidence", 50) for p in patterns)
    avg = total / len(patterns)
    return round(avg, 2)
