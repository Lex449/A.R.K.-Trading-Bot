"""
A.R.K. Data Auto-Validator – Ultra Signal Tolerance Build 6.9
Smarter Schwellenwert, akzeptiert alle verwertbaren Kursdaten. Kein Blockieren bei schwacher Bewegung.
Made in Bali. Engineered with German Precision.
"""

import pandas as pd
from bot.utils.logger import setup_logger

logger = setup_logger(__name__)

def validate_market_data(df: pd.DataFrame, min_rows: int = 30) -> bool:
    """
    Validiert OHLCV-Daten flexibel – hohe Toleranz für stille Phasen.
    """
    try:
        if df is None or not isinstance(df, pd.DataFrame) or df.empty:
            logger.warning("⚠️ [Validator] Kein gültiger DataFrame übergeben.")
            return False

        if len(df) < min_rows:
            logger.warning(f"⚠️ [Validator] Zu wenige Kerzen ({len(df)} < {min_rows})")
            return False

        required = {"o", "h", "l", "c", "v"}
        if not required.issubset(set(df.columns)):
            missing = required - set(df.columns)
            logger.warning(f"⚠️ [Validator] Fehlende Spalten: {missing}")
            return False

        if df[list(required)].isnull().mean().mean() > 0.05:
            logger.warning("⚠️ [Validator] Zu viele NaNs in Kerzenstruktur.")
            return False

        if (df[["o", "h", "l", "c"]] <= 0).any().any():
            logger.warning("⚠️ [Validator] Negative oder 0-Werte entdeckt.")
            return False

        # Nicht sofort blockieren bei flachen Kursen – nur bei 100 % Stagnation
        unique_closes = df["c"].tail(20).nunique()
        if unique_closes <= 1:
            logger.warning("⚠️ [Validator] Letzte 20 Schlusskurse sind identisch – Flat Market.")
            return False

        logger.info("✅ [Validator] Kursdaten akzeptiert.")
        return True

    except Exception as e:
        logger.error(f"❌ [Validator] Schwerwiegender Fehler: {e}")
        return False
