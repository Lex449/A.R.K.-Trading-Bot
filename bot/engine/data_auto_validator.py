"""
A.R.K. Data Validator – Integrity Checkpoint v1.4  
Sichert Datenintegrität vor Analyse. Verhindert fehlerhafte Berechnungen.  
Made in Bali. Engineered with German Precision.
"""

import pandas as pd
from bot.utils.logger import setup_logger

logger = setup_logger(__name__)

def validate_market_data(df: pd.DataFrame) -> bool:
    try:
        if df is None or df.empty:
            logger.warning("❌ [Validator] DataFrame is None or empty.")
            return False

        required_columns = {"o", "h", "l", "c", "v"}
        if not required_columns.issubset(df.columns):
            logger.warning(f"❌ [Validator] Missing columns in DataFrame: {required_columns - set(df.columns)}")
            return False

        if df["c"].nunique() <= 1:
            logger.warning("⚠️ [Validator] Price data shows no variation.")
            return False

        if df.isnull().sum().sum() > 0:
            logger.warning("⚠️ [Validator] Null values detected in DataFrame.")
            return False

        return True

    except Exception as e:
        logger.error(f"❌ [Validator] Error validating market data: {e}")
        return False
