# bot/engine/analysis_engine.py

"""
A.R.K. Analysis Engine – Ultra Full Signal Suite 10.0
Fusion aus Pattern, Trend, Volumen, Volatilität, RRR, Confidence Scaling & Category Scoring.

Ziel: Lückenlose Signalvalidierung, präzise Entscheidungsbasis, Masterclass-Effizienz.
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
from bot.engine.signal_rating_improvement import rate_signal  # <- FIXED HERE
from bot.utils.logger import setup_logger

logger = setup_logger(__name__)

async def analyze_symbol(symbol: str, chat_id: int = None) -> dict | None:
    """
    Führt eine vollständige Analyse eines Symbols durch.
    Gibt strukturierte Daten für Signalaufbau, Bewertung und Dispatch zurück.
    """
    try:
        df = await fetch_market_data(symbol, chat_id=chat_id)
        if not validate_market_data(df):
            logger.warning(f"🚫 [AnalysisEngine] Data validation failed for {symbol}.")
            return None

        last_price = df["c"].iloc[-1]

        # === Analyse-Module ===
        patterns = detect_patterns(df)
        volume_info = detect_volume_spike(df)
        trend_info = detect_adaptive_trend(df)
        indicator_score, trend_direction = evaluate_indicators(df)

        combined_action = determine_action(patterns, trend_info, indicator_score)
        risk_reward_info = (
            analyze_risk_reward(df, combined_action)
            if combined_action in ("Long 📈", "Short 📉")
            else None
        )

        base_confidence = calculate_confidence(patterns)
        adjusted_confidence = optimize_confidence(base_confidence, trend_info)

        if combined_action != "Neutral ⚪":
            adjusted_confidence += 10
        adjusted_confidence = min(adjusted_confidence, 100.0)

        signal_category = categorize_signal(adjusted_confidence)
        signal_score = rate_signal(patterns, volatility_info=volume_info, trend_info=trend_info)

        # === Final Result ===
        result = {
            "symbol": symbol,
            "last_price": round(last_price, 2),
            "patterns": patterns,
            "avg_confidence": adjusted_confidence,
            "combined_action": combined_action,
            "signal_category": signal_category,
            "signal_score": signal_score,
            "indicator_score": indicator_score,
            "trend_direction": trend_direction,
            "volume_info": volume_info,
            "trend_info": trend_info,
            "risk_reward_info": risk_reward_info,
            "df": df
        }

        logger.info(
            f"✅ [AnalysisEngine] {symbol} | Action: {combined_action} | "
            f"Price: {last_price:.2f} | Confidence: {adjusted_confidence:.1f}% | Score: {signal_score}/100"
        )
        return result

    except Exception as e:
        logger.error(f"❌ [AnalysisEngine] Critical failure for {symbol}: {e}")
        return None

def determine_action(patterns: list, trend_info: dict, indicator_score: float) -> str:
    """
    Kombiniert Pattern + Trendanalyse + Indikatorwerte zu einem klaren Handlungsvorschlag.
    """
    bullish = any(p.get("action", "").startswith("Long") for p in patterns)
    bearish = any(p.get("action", "").startswith("Short") for p in patterns)
    trend = trend_info.get("early_trend") if trend_info else None

    if (bullish and trend == "bullish") or (indicator_score > 60 and trend == "bullish"):
        return "Long 📈"
    elif (bearish and trend == "bearish") or (indicator_score < 40 and trend == "bearish"):
        return "Short 📉"
    return "Neutral ⚪"

def calculate_confidence(patterns: list) -> float:
    """
    Aggregiert die Confidence-Werte der Pattern zu einer Basisschätzung.
    """
    if not patterns:
        return 0.0
    total = sum(p.get("confidence", 60) for p in patterns)
    return round(total / len(patterns), 2)
