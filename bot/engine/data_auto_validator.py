"""
A.R.K. Data Auto-Validator – Ultra Precision Safety Net 6.1
Balances strict data checks with smart flexibility for higher signal throughput.

Built for: Robust Integrity, Signal Optimization, Fault-Tolerant Performance.
Made in Bali. Engineered with German Precision.
"""

import pandas as pd
from bot.utils.logger import setup_logger

logger = setup_logger(__name__)

def validate_market_data(df: pd.DataFrame, min_rows: int = 20) -> bool:
    """
    Validates OHLCV data integrity while tolerating minor data imperfections.

    Returns:
        bool: True if usable, False otherwise
    """
    try:
        if df is None or not isinstance(df, pd.DataFrame) or df.empty:
            logger.warning("⚠️ [Validator] DataFrame invalid or empty.")
            return False

        if len(df) < min_rows:
            logger.warning(f"⚠️ [Validator] Too few candles ({len(df)} < {min_rows})")
            return False

        required = {"o", "h", "l", "c", "v"}
        missing = required - set(df.columns)
        if missing:
            logger.warning(f"⚠️ [Validator] Missing columns: {missing}")
            return False

        # Allow up to 2% NaNs across all required columns
        nan_pct = df[list(required)].isnull().mean().mean()
        if nan_pct > 0.02:
            logger.warning(f"⚠️ [Validator] Too many NaNs: {nan_pct:.2%}")
            return False

        # Allow small price anomalies but catch full-zero or negative
        if (df[["o", "h", "l", "c"]] <= 0).sum().sum() > 0:
            logger.warning("⚠️ [Validator] Negative or zero price found.")
            return False

        # Candle logic: allow 1–2 bad rows (out of e.g. 300)
        high_fail = (df["h"] < df[["o", "c", "l"]].max(axis=1)).sum()
        low_fail = (df["l"] > df[["o", "c", "h"]].min(axis=1)).sum()
        if high_fail > 2 or low_fail > 2:
            logger.warning(f"⚠️ [Validator] Candle logic off → high_fail: {high_fail}, low_fail: {low_fail}")
            return False

        # Last candle flat = suspicious
        last = df.iloc[-1]
        if last[["o", "h", "l", "c"]].nunique() == 1:
            logger.warning("⚠️ [Validator] Last candle is flat – low activity?")
            return False

        logger.info("✅ [Validator] Market data accepted.")
        return True

    except Exception as e:
        logger.error(f"❌ [Validator Critical Error] {e}")
        return False
