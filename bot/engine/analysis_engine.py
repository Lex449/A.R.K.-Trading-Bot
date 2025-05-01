"""
A.R.K. Analysis Engine – Ultra Full Signal Suite v11.1  
Fusion aus Pattern, Trend, Volumen, Volatilität, RRR, Confidence Scaling & Category Scoring.  
Jetzt mit adaptivem Trend-Fallback & gelockerter Confidence-Schwelle.  
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
from bot.engine.signal_rating_improvement import rate_signal
from bot.utils.logger import setup_logger

logger = setup_logger(__name__)

async def analyze_symbol(symbol: str, chat_id: int = None, silent: bool = False) -> dict | None:
    try:
        df = await fetch_market_data(symbol, chat_id=chat_id)
        if df is None or not validate_market_data(df):
            logger.warning(f"🚫 [AnalysisEngine] Data validation failed for {symbol}")
            if df is not None:
                logger.debug(f"⚠️ [Debug] {symbol} → Close Prices: {df['c'].tail(10).tolist()}")
            return None

        last_price = df["c"].iloc[-1]
        patterns = detect_patterns(df) or []
        volume_info = detect_volume_spike(df) or {}
        trend_info = detect_adaptive_trend(df) or {}
        indicator_score, trend_direction = evaluate_indicators(df) or (0.0, "Neutral ⚪")
        combined_action = determine_action(patterns, trend_info, indicator_score)

        # === Lockerung: Trend-Only fallback, falls keine Patterns vorhanden ===
        if combined_action == "Neutral ⚪" and trend_direction in ["Long 📈", "Short 📉"] and indicator_score >= 65:
            combined_action = trend_direction
            logger.info(f"⚠️ [AnalysisEngine] {symbol} upgraded via Trend Fallback → {combined_action}")

        risk_reward_info = (
            analyze_risk_reward(df, combined_action)
            if combined_action in ("Long 📈", "Short 📉")
            else None
        )

        base_confidence = calculate_confidence(patterns)

        # === FINAL: Optimierte Confidence mit allen Kontextdaten ===
        adjusted_confidence = optimize_confidence(
            {
                "confidence": base_confidence,
                "trend_info": trend_info,
                "volume_info": volume_info,
                "patterns": patterns
            },
            {
                "signals_total": 100,
                "strong_signals": 40
            }
        )

        # === Bonuspunkte für starke Trends, RSI, Pattern-Menge ===
        if combined_action in ["Long 📈", "Short 📉"]:
            adjusted_confidence += 10
        if indicator_score >= 70:
            adjusted_confidence += 5
        if len(patterns) >= 2:
            adjusted_confidence += 3

        adjusted_confidence = min(adjusted_confidence, 100.0)

        signal_score = rate_signal(patterns, volatility_info=volume_info, trend_info=trend_info)
        signal_category = categorize_signal(adjusted_confidence)

        # === Neue, gelockerte Schwelle: 40 statt 50 ===
        if adjusted_confidence < 40:
            logger.info(f"⛔ [AnalysisEngine] {symbol} skipped – Confidence: {adjusted_confidence:.1f}%")
            return None

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
            f"✅ [AnalysisEngine] {symbol} | {combined_action} | "
            f"${last_price:.2f} | Confidence: {adjusted_confidence:.1f}% | "
            f"Score: {signal_score}/100 | Trend: {trend_direction}"
        )
        return result

    except Exception as e:
        logger.exception(f"❌ [AnalysisEngine] Critical error for {symbol}: {e}")
        return None


async def analyze_market(symbols: list[str]) -> list[dict]:
    import asyncio
    tasks = [analyze_symbol(symbol, silent=True) for symbol in symbols]
    results = await asyncio.gather(*tasks)
    return [r for r in results if r]


def determine_action(patterns: list, trend_info: dict, indicator_score: float) -> str:
    bullish = any(p.get("action", "").startswith("Long") for p in patterns)
    bearish = any(p.get("action", "").startswith("Short") for p in patterns)
    if bullish:
        return "Long 📈"
    elif bearish:
        return "Short 📉"
    return "Neutral ⚪"


def calculate_confidence(patterns: list) -> float:
    if not patterns:
        return 0.0
    total = sum(p.get("confidence", 60) for p in patterns)
    return round(total / len(patterns), 2)
