"""
A.R.K. ATR Engine – Dynamic Volatility Intelligence 2025
Calculates True Range Percentages and Detects Breakout Events.

Built for: Ultra Precision, Adaptive Risk Management, Early Warning System.
"""

import pandas as pd
import numpy as np

class ATREngine:
    """
    A.R.K. ATR Engine
    Computes ATR-based volatility measures for enhanced decision-making.
    """

    def __init__(self, period: int = 14, language: str = "en"):
        self.period = period
        self.language = language.lower()

    def _localized_error(self, error_type: str) -> str:
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
        Calculates ATR relative to last closing price (%).

        Args:
            df (pd.DataFrame): DataFrame containing 'high', 'low', 'close'.

        Returns:
            float: ATR percentage vs close price.
        """
        if df is None or len(df) < self.period or not all(col in df.columns for col in ["high", "low", "close"]):
            raise ValueError(self._localized_error("invalid_df"))

        try:
            df["high_low"] = df["high"] - df["low"]
            df["high_close"] = (df["high"] - df["close"].shift()).abs()
            df["low_close"] = (df["low"] - df["close"].shift()).abs()

            df["true_range"] = df[["high_low", "high_close", "low_close"]].max(axis=1)

            atr_value = df["true_range"].rolling(window=self.period, min_periods=1).mean().iloc[-1]
            last_close = df["close"].iloc[-1]

            if last_close == 0:
                raise ValueError(self._localized_error("zero_close"))

            atr_percent = (atr_value / last_close) * 100

            return round(atr_percent, 2)

        finally:
            df.drop(columns=["high_low", "high_close", "low_close", "true_range"], inplace=True, errors="ignore")

    def detect_volatility_spike(self, df: pd.DataFrame, threshold_multiplier: float = 1.8) -> bool:
        """
        Detects a volatility spike based on ATR threshold logic.

        Args:
            df (pd.DataFrame): Market data.
            threshold_multiplier (float): Spike sensitivity threshold.

        Returns:
            bool: True if spike detected, else False.
        """
        atr_percent = self.calculate_atr_percent(df)
        last_candle_move = ((df["high"].iloc[-1] - df["low"].iloc[-1]) / df["close"].iloc[-1]) * 100

        return last_candle_move > (atr_percent * threshold_multiplier)
