"""
A.R.K. ATR Engine – Dynamic Volatility Intelligence 2025
Fusioniert ATR-Berechnung und Spike-Erkennung in einer ultrastabilen Einheit.

Ziele: Adaptive Risk Control, Early Breakout Detection, Hyper Performance Analytics.
"""

import pandas as pd
import numpy as np
import logging

# Setup Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class ATREngine:
    """
    Handles all ATR-based volatility detection and dynamic spike alerts.
    """

    def __init__(self, period: int = 14, language: str = "en"):
        self.period = period
        self.language = language.lower()

    def _localized_error(self, error_type: str) -> str:
        """Localized error messages."""
        errors = {
            "invalid_df": {
                "en": "Invalid DataFrame supplied for ATR calculation.",
                "de": "Ungültiges DataFrame für ATR-Berechnung übergeben."
            },
            "zero_close": {
                "en": "Last closing price is zero. ATR percentage undefined.",
                "de": "Letzter Schlusskurs ist null. ATR-Prozent unbestimmbar."
            }
        }
        return errors.get(error_type, {}).get(self.language, "Unknown calculation error.")

    def calculate_atr_percent(self, df: pd.DataFrame) -> float:
        """
        Calculates the Average True Range as percentage of last close.

        Returns:
            float: ATR % or raises ValueError.
        """
        if df is None or len(df) < self.period or not all(col in df.columns for col in ["high", "low", "close"]):
            raise ValueError(self._localized_error("invalid_df"))

        try:
            df["hl"] = df["high"] - df["low"]
            df["hc"] = (df["high"] - df["close"].shift()).abs()
            df["lc"] = (df["low"] - df["close"].shift()).abs()
            df["tr"] = df[["hl", "hc", "lc"]].max(axis=1)

            atr = df["tr"].rolling(window=self.period, min_periods=1).mean().iloc[-1]
            close = df["close"].iloc[-1]

            if close == 0:
                raise ValueError(self._localized_error("zero_close"))

            return round((atr / close) * 100, 2)

        finally:
            df.drop(columns=["hl", "hc", "lc", "tr"], inplace=True, errors="ignore")

    def detect_volatility_spike(self, df: pd.DataFrame, threshold: float = 1.8) -> dict | None:
        """
        Detects volatility spikes relative to ATR baseline.
        Returns a detailed dict if spike detected, else None.
        """
        try:
            atr_pct = self.calculate_atr_percent(df)
            move_pct = ((df["high"].iloc[-1] - df["low"].iloc[-1]) / df["close"].iloc[-1]) * 100

            if move_pct > (atr_pct * threshold):
                logger.info(f"[ATR Spike] Detected: Move={move_pct:.2f}%, ATR={atr_pct:.2f}%")
                return {
                    "atr_percent": atr_pct,
                    "move_percent": round(move_pct, 2),
                    "spike": True
                }
            else:
                return None

        except Exception as e:
            logger.error(f"[ATR Engine Error] {e}")
            return None
