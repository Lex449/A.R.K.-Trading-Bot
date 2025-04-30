"""
A.R.K. Data Auto-Validator – Ultra Signal-Tolerant Mode v7.2
Validiert OHLCV-Kerzendaten mit smarter Fehlertoleranz und präzisem Logging.
Optimiert für hohe Durchsatzrate bei gleichzeitiger Datenintegrität.

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
        # === 1. Strukturcheck ===
        if df is None or not isinstance(df, pd.DataFrame) or df.empty:
            logger.warning("⚠️ [Validator] ❌ Kein gültiger DataFrame – leer oder ungültig.")
            return False

        if len(df) < min_rows:
            logger.warning(f"⚠️ [Validator] ❌ Zu wenige Kerzen ({len(df)} < {min_rows})")
            return False

        # === 2. Spaltenprüfung ===
        required_cols = {"o", "h", "l", "c", "v"}
        missing = required_cols - set(df.columns)
        if missing:
            logger.warning(f"⚠️ [Validator] ❌ Fehlende Spalten: {missing}")
            return False

        # === 3. NaN-Toleranzprüfung ===
        nan_ratio = df[list(required_cols)].isnull().mean().mean()
        if nan_ratio > 0.05:
            logger.warning(f"⚠️ [Validator] ❌ Zu viele NaNs – Quote: {nan_ratio:.2%}")
            return False

        # === 4. Preis-Sanity Check ===
        if (df[["o", "h", "l", "c"]] <= 0).any().any():
            logger.warning("⚠️ [Validator] ❌ Negative oder Nullpreise erkannt.")
            return False

        # === 5. Candle-Logikprüfung (max. 5 % Toleranz) ===
        high_fail = (df["h"] < df[["o", "c", "l"]].max(axis=1)).sum()
        low_fail = (df["l"] > df[["o", "c", "h"]].min(axis=1)).sum()
        max_fails = int(len(df) * 0.05)

        if high_fail > max_fails or low_fail > max_fails:
            logger.warning(f"⚠️ [Validator] ❌ Candle-Logik Fehler – HighFail: {high_fail}, LowFail: {low_fail}")
            return False

        # === 6. Flacher Markt-Check ===
        if df["c"].tail(5).nunique() <= 1:
            logger.warning("⚠️ [Validator] ❌ Letzte 5 Schlusskurse identisch – Kein Volumen.")
            return False

        # === 7. Erfolgsmeldung ===
        logger.info(
            f"✅ [Validator] Daten akzeptiert – Zeilen: {len(df)}, NaN: {nan_ratio:.2%}, HighFail: {high_fail}, LowFail: {low_fail}"
        )
        return True

    except Exception as e:
        logger.error(f"❌ [Validator Critical Error] {e}")
        return False
