"""
A.R.K. Analysis Engine – Ultra Full Signal Suite v10.5
Fusion aus Pattern, Trend, Volumen, Volatilität, RRR, Confidence Scaling & Category Scoring.
Mit smarter Telegram-Analyseausgabe und dynamischer Rejection-Diagnose.
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

async def analyze_symbol(symbol: str, chat_id: int = None) -> dict | None:
    try:
        df = await fetch_market_data(symbol, chat_id=chat_id)
        if df is None or not validate_market_data(df):
            logger.warning(f"🚫 [AnalysisEngine] Data validation failed or no data returned for {symbol}.")
            if df is not None:
                logger.debug(f"⚠️ [Debug] {symbol} → Close Prices (last 10): {df['c'].tail(10).tolist()}")
            if chat_id:
                from bot import application
                await application.bot.send_message(
                    chat_id=chat_id,
                    text=(
                        f"⚠️ *{symbol} konnte nicht analysiert werden:*\n"
                        f"_Grund:_ Kursdaten nicht valide oder leer.\n\n"
                        f"_API war aktiv – Symbol wurde übersprungen._"
                    ),
                    parse_mode="Markdown"
                )
            return None

        last_price = df["c"].iloc[-1]
        patterns = detect_patterns(df) or []
        volume_info = detect_volume_spike(df) or {}
        trend_info = detect_adaptive_trend(df) or {}
        indicator_score, trend_direction = evaluate_indicators(df) or (0.0, "Neutral")
        combined_action = determine_action(patterns, trend_info, indicator_score)

        risk_reward_info = (
            analyze_risk_reward(df, combined_action)
            if combined_action in ("Long 📈", "Short 📉")
            else None
        )

        base_confidence = calculate_confidence(patterns)
        adjusted_confidence = optimize_confidence(base_confidence, trend_info)

        if combined_action in ["Long 📈", "Short 📉"]:
            adjusted_confidence += 10
        adjusted_confidence = min(adjusted_confidence, 100.0)

        signal_score = rate_signal(patterns, volatility_info=volume_info, trend_info=trend_info)

        if adjusted_confidence < 50:
            flat_market = df["c"].tail(5).nunique() <= 1
            if chat_id:
                from bot import application
                await application.bot.send_message(
                    chat_id=chat_id,
                    text=(
                        f"⚠️ *{symbol} konnte nicht analysiert werden.*\n"
                        f"_Grund:_ Confidence zu niedrig (`{adjusted_confidence:.1f}%`)\n\n"
                        f"*Details:*\n"
                        f"• Patterns: `{len(patterns)}` erkannt\n"
                        f"• Signal Score: `{signal_score}/100`\n"
                        f"• Indicator Score: `{indicator_score}`\n"
                        f"• Trend: {trend_direction}\n"
                        f"• Flat Market: {'Ja' if flat_market else 'Nein'}\n"
                        f"• Daten: {len(df)} Rows, NaNs: {df.isnull().mean().mean():.2%}"
                    ),
                    parse_mode="Markdown"
                )
            logger.info(
                f"⛔ [AnalysisEngine] {symbol} skipped – Confidence: {adjusted_confidence:.1f}%, "
                f"Patterns: {len(patterns)}, Score: {signal_score}, IndicatorScore: {indicator_score}, "
                f"Trend: {trend_direction}, FlatMarket: {flat_market}"
            )
            return None

        signal_category = categorize_signal(adjusted_confidence)

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
            f"Price: {last_price:.2f} | Confidence: {adjusted_confidence:.1f}% | "
            f"Score: {signal_score}/100 | Trend: {trend_direction}"
        )
        return result

    except Exception as e:
        logger = setup_logger(__name__)
        logger.exception(f"❌ [AnalysisEngine] Critical failure for {symbol}: {e}")
        return None

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
