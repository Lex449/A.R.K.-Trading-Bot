"""
A.R.K. Data Auto-Validator – Ultra Signal-Tolerant Mode v7.0
Balances precision with throughput for real-time market conditions.
Made in Bali. Engineered with German Precision.
"""

import pandas as pd
from bot.utils.logger import setup_logger

logger = setup_logger(__name__)

def validate_market_data(df: pd.DataFrame, min_rows: int = 20) -> bool:
    """
    Validates OHLCV market data with high flexibility.
    Returns:
        bool: True if valid, False if rejected.
    """
    try:
        # === Basic Validity Checks ===
        if df is None or not isinstance(df, pd.DataFrame) or df.empty:
            logger.warning("⚠️ [Validator] DataFrame invalid or empty.")
            return False

        if len(df) < min_rows:
            logger.warning(f"⚠️ [Validator] Too few candles ({len(df)} < {min_rows})")
            return False

        required_cols = {"o", "h", "l", "c", "v"}
        missing = required_cols - set(df.columns)
        if missing:
            logger.warning(f"⚠️ [Validator] Missing columns: {missing}")
            return False

        # === NaN Check (Up to 5% allowed) ===
        nan_ratio = df[list(required_cols)].isnull().mean().mean()
        if nan_ratio > 0.05:
            logger.warning(f"⚠️ [Validator] Too many NaNs: {nan_ratio:.2%}")
            return False

        # === Price Sanity Check (No zero/negative values) ===
        if (df[["o", "h", "l", "c"]] <= 0).any().any():
            logger.warning("⚠️ [Validator] Negative or zero prices detected.")
            return False

        # === Candle Structure Check (Max 5% fail tolerance) ===
        high_fail = (df["h"] < df[["o", "c", "l"]].max(axis=1)).sum()
        low_fail = (df["l"] > df[["o", "c", "h"]].min(axis=1)).sum()
        max_fails = int(len(df) * 0.05)

        if high_fail > max_fails or low_fail > max_fails:
            logger.warning(f"⚠️ [Validator] Candle logic fail – High: {high_fail}, Low: {low_fail}")
            return False

        # === Last Candle Flat Detection (Over last 5 candles) ===
        if df["c"].tail(5).nunique() <= 1:
            logger.warning("⚠️ [Validator] Last 5 candles flat – Market possibly inactive.")
            return False

        # === Final Status ===
        logger.info(f"✅ [Validator] Market data accepted for analysis. Rows: {len(df)} | NaN: {nan_ratio:.2%}")
        return True

    except Exception as e:
        logger.error(f"❌ [Validator Critical Error] {e}")
        return False
