"""
A.R.K. ATR Engine – Volatility Precision Scanner.
Berechnet die durchschnittliche True Range (ATR) für Marktschwankungsanalyse.

Engineered for: Ultra Precision, Dynamic Risk Management, Early Move Detection.
"""

import pandas as pd
import numpy as np

class ATREngine:
    """
    A.R.K. ATR Engine
    Calculates ATR (Average True Range) relative to price for smarter trading decisions.
    """

    def __init__(self, period: int = 14, language: str = "en"):
        """
        Initializes the ATR Engine.

        Args:
            period (int): Lookback period for ATR calculation (default: 14).
            language (str): Language for error messages ("en" or "de").
        """
        self.period = period
        self.language = language.lower()

    def _error_message(self, error_type: str) -> str:
        """
        Returns localized error messages.

        Args:
            error_type (str): Specific error type key.

        Returns:
            str: Error message text.
        """
        messages = {
            "invalid_df": {
                "en": "Invalid DataFrame provided to ATR Engine.",
                "de": "Ungültiges DataFrame an ATR Engine übergeben."
            },
            "zero_close": {
                "en": "Last close price is zero. Cannot calculate ATR percentage.",
                "de": "Letzter Schlusskurs ist null. ATR-Prozent kann nicht berechnet werden."
            }
        }
        return messages.get(error_type, {}).get(self.language, "Unknown error.")

    def calculate_atr_percent(self, df: pd.DataFrame) -> float:
        """
        Calculates ATR as a percentage of the last closing price.

        Args:
            df (pd.DataFrame): DataFrame with 'high', 'low', 'close' columns.

        Returns:
            float: ATR percentage relative to last close price.
        """
        if df is None or len(df) < self.period or not all(col in df.columns for col in ["high", "low", "close"]):
            raise ValueError(self._error_message("invalid_df"))

        try:
            # Calculate True Range components
            df["high_low"] = df["high"] - df["low"]
            df["high_close"] = (df["high"] - df["close"].shift()).abs()
            df["low_close"] = (df["low"] - df["close"].shift()).abs()

            df["true_range"] = df[["high_low", "high_close", "low_close"]].max(axis=1)

            # Calculate ATR
            atr = df["true_range"].rolling(window=self.period, min_periods=1).mean().iloc[-1]
            last_close = df["close"].iloc[-1]

            if last_close == 0:
                raise ValueError(self._error_message("zero_close"))

            atr_percent = (atr / last_close) * 100

            return round(atr_percent, 2)

        finally:
            # Cleanup to prevent DataFrame pollution
            df.drop(columns=["high_low", "high_close", "low_close", "true_range"], inplace=True, errors="ignore")

    def detect_volatility_spike(self, df: pd.DataFrame, threshold_multiplier: float = 1.8) -> bool:
        """
        Detects volatility spike based on ATR threshold.

        Args:
            df (pd.DataFrame): DataFrame with 'high', 'low', 'close' columns.
            threshold_multiplier (float): Spike detection threshold (default: 1.8).

        Returns:
            bool: True if a volatility spike is detected, else False.
        """
        atr_percent = self.calculate_atr_percent(df)
        last_candle_move = ((df["high"].iloc[-1] - df["low"].iloc[-1]) / df["close"].iloc[-1]) * 100

        return last_candle_move > (atr_percent * threshold_multiplier)
