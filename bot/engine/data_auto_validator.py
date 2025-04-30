# bot/engine/data_auto_validator.py

"""
A.R.K. Data Auto-Validator – Ultra Precision Safety Net 6.0
Validates fetched market data before any analysis or trading decision.

Designed for: Institutional Integrity Checks, Ultra-Low Error Rate, Pro-Level Fault Tolerance.
Made in Bali. Engineered with German Precision.
"""

import pandas as pd
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

def validate_market_data(df: pd.DataFrame, min_rows: int = 20) -> bool:
    """
    Validates that the market OHLCV data is complete, accurate and tradable.

    Args:
        df (pd.DataFrame): Market data
        min_rows (int): Minimum candles required (default = 20)

    Returns:
        bool: True if valid, False otherwise
    """
    try:
        if df is None:
            logger.warning("⚠️ [DataValidator] DataFrame is None.")
            return False

        if not isinstance(df, pd.DataFrame):
            logger.warning("⚠️ [DataValidator] Invalid object type.")
            return False

        if df.empty:
            logger.warning("⚠️ [DataValidator] DataFrame is empty.")
            return False

        if len(df) < min_rows:
            logger.warning(f"⚠️ [DataValidator] Too few rows: {len(df)} < {min_rows}")
            return False

        required_cols = {"o", "h", "l", "c", "v"}
        missing_cols = required_cols - set(df.columns)
        if missing_cols:
            logger.warning(f"⚠️ [DataValidator] Missing columns: {missing_cols}")
            return False

        if df[required_cols].isnull().any().any():
            logger.warning("⚠️ [DataValidator] NaN values detected.")
            return False

        if (df[["o", "h", "l", "c"]] <= 0).any().any():
            logger.warning("⚠️ [DataValidator] Non-positive prices found.")
            return False

        # Validate candle logic
        invalid_highs = (df["h"] < df[["o", "c", "l"]].max(axis=1)).sum()
        invalid_lows = (df["l"] > df[["o", "c", "h"]].min(axis=1)).sum()
        if invalid_highs > 0 or invalid_lows > 0:
            logger.warning(f"⚠️ [DataValidator] Candle logic failure: highs={invalid_highs}, lows={invalid_lows}")
            return False

        # Check last candle for zero movement (flat candles)
        last = df.iloc[-1]
        if last["h"] == last["l"] == last["o"] == last["c"]:
            logger.warning("⚠️ [DataValidator] Last candle is flat – no market activity?")
            return False

        logger.info("✅ [DataValidator] Market data passed all validation checks.")
        return True

    except Exception as e:
        logger.error(f"❌ [DataValidator Fatal Error] {e}")
        return False
