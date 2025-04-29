"""
A.R.K. Data Auto-Validator – Ultra Precision Safety Net 5.0
Validates fetched market data before any analysis or trading decision.

Designed for: Institutional Integrity Checks, Ultra-Low Error Rate, Pro-Level Fault Tolerance.
"""

import pandas as pd
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

def validate_market_data(df: pd.DataFrame, min_rows: int = 20) -> bool:
    """
    Validates that the market data is clean, complete, and tradable.

    Args:
        df (pd.DataFrame): Market OHLCV DataFrame.
        min_rows (int): Minimum number of required candles (default = 20).

    Returns:
        bool: True if data is valid, False if rejected.
    """
    try:
        if df is None:
            logger.warning("⚠️ [DataValidator] DataFrame is None.")
            return False

        if df.empty:
            logger.warning("⚠️ [DataValidator] DataFrame is empty.")
            return False

        if len(df) < min_rows:
            logger.warning(f"⚠️ [DataValidator] Insufficient rows: {len(df)} < {min_rows}.")
            return False

        required_columns = {"o", "h", "l", "c", "v"}
        if not required_columns.issubset(df.columns):
            logger.warning(f"⚠️ [DataValidator] Missing required columns: {required_columns - set(df.columns)}.")
            return False

        if df.isnull().any().any():
            logger.warning("⚠️ [DataValidator] NaN values detected in DataFrame.")
            return False

        if (df["o"] <= 0).any() or (df["h"] <= 0).any() or (df["l"] <= 0).any() or (df["c"] <= 0).any():
            logger.warning("⚠️ [DataValidator] Non-positive prices detected.")
            return False

        logger.info("✅ [DataValidator] Market data passed validation checks.")
        return True

    except Exception as e:
        logger.error(f"❌ [DataValidator Critical Error] {e}")
        return False
