# bot/engine/atr_engine.py

"""
A.R.K. ATR Engine – Dynamic Volatility Intelligence 2025
Fusioniert ATR-Berechnung und Spike-Erkennung in einer ultrastabilen Einheit.

Ziele: Adaptive Risk Control, Early Breakout Detection, Hyper Performance Analytics.
Made in Bali. Engineered with German Precision.
"""

import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class ATREngine:
    """
    Handles all ATR-based volatility detection and dynamic spike alerts.
    """

    def __init__(self, period: int = 14, language: str = "en"):
        self.period = period
        self.language = language.lower()

    def _localized_error(self, key: str) -> str:
        messages = {
            "invalid_df": {
                "en": "Invalid DataFrame for ATR calculation.",
                "de": "Ungültiges DataFrame für ATR-Berechnung."
            },
            "zero_close": {
                "en": "Closing price is zero – cannot compute ATR%.",
                "de": "Schlusskurs ist null – ATR% nicht berechenbar."
            }
        }
        return messages.get(key, {}).get(self.language, "Unknown error")

    def calculate_atr_percent(self, df: pd.DataFrame) -> float:
        """
        Calculates the Average True Range (ATR) as a percentage of the last close.

        Returns:
            float: ATR% rounded to 2 decimals.
        """
        if df is None or df.empty or len(df) < self.period:
            raise ValueError(self._localized_error("invalid_df"))

        if not all(col in df.columns for col in ["high", "low", "close"]):
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

            atr_percent = (atr / close) * 100
            return round(atr_percent, 2)

        finally:
            df.drop(columns=["hl", "hc", "lc", "tr"], inplace=True, errors="ignore")

    def detect_volatility_spike(self, df: pd.DataFrame, threshold: float = 1.8) -> dict | None:
        """
        Detects if current price move exceeds ATR-based expectation.

        Returns:
            dict: Details if spike detected, else None.
        """
        try:
            atr_pct = self.calculate_atr_percent(df)
            move_range = df["high"].iloc[-1] - df["low"].iloc[-1]
            last_close = df["close"].iloc[-1]

            if last_close <= 0 or move_range <= 0:
                logger.warning("[ATREngine] Invalid move/close values for spike detection.")
                return None

            move_pct = (move_range / last_close) * 100

            if move_pct > (atr_pct * threshold):
                logger.info(f"🌪️ [ATREngine] Spike detected: Move={move_pct:.2f}% > {atr_pct * threshold:.2f}%")
                return {
                    "atr_percent": round(atr_pct, 2),
                    "move_percent": round(move_pct, 2),
                    "spike": True
                }

            return None

        except Exception as e:
            logger.error(f"❌ [ATREngine Error] {e}")
            return None
