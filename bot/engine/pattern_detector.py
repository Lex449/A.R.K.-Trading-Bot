# bot/engine/pattern_detector.py

import pandas as pd
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

def detect_candle_patterns(df: pd.DataFrame) -> str:
    """
    Detects classic candlestick patterns for short- or long-setups.
    Supports Hammer, Shooting Star, Bullish Engulfing, Bearish Engulfing, and Doji.
    
    Args:
        df (pd.DataFrame): The OHLCV dataframe for a symbol.
    
    Returns:
        str: Detected candlestick pattern or "No Pattern".
    """
    try:
        last = df.iloc[-1]
        body = abs(last['c'] - last['o'])
        candle_range = last['h'] - last['l']

        if candle_range == 0:
            logger.warning("[Pattern Detector] Zero candle range detected. No Pattern.")
            return "No Pattern"

        # === Pattern Detection ===
        # Doji
        if body < 0.1 * candle_range:
            logger.info("[Pattern Detector] Detected: Doji")
            return "Doji"

        # Bullish Engulfing
        if (last['c'] > last['o']) and (body > 0.6 * candle_range):
            logger.info("[Pattern Detector] Detected: Bullish Engulfing")
            return "Bullish Engulfing"

        # Bearish Engulfing
        if (last['o'] > last['c']) and (body > 0.6 * candle_range):
            logger.info("[Pattern Detector] Detected: Bearish Engulfing")
            return "Bearish Engulfing"

        # Hammer
        if (last['c'] > last['o']) and (last['l'] < min(last['c'], last['o']) - body):
            logger.info("[Pattern Detector] Detected: Hammer")
            return "Hammer"

        # Shooting Star
        if (last['h'] > max(last['c'], last['o']) + body):
            logger.info("[Pattern Detector] Detected: Shooting Star")
            return "Shooting Star"

        logger.info("[Pattern Detector] No clear pattern detected.")
        return "No Pattern"

    except Exception as e:
        logger.error(f"[Pattern Detector Error] {str(e)}")
        return "No Pattern"
