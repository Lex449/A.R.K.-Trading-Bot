# bot/engine/atr_engine.py

"""
A.R.K. ATR Engine – Volatility Precision Scanner.
Berechnet die durchschnittliche True Range (ATR) auf Basis der Marktschwankungen.

Engineered for: Ultra Precision, Risk-Reward Strategies, Early Move Detection.
"""

import pandas as pd
import numpy as np

class ATREngine:
    """
    A.R.K. ATR Engine
    Calculates Average True Range (ATR) as a percentage of the last closing price.
    Optimized for Ultra-Precision, early detection and dynamic risk adjustment.
    """

    def __init__(self, period: int = 14, language: str = "en"):
        """
        Initializes the ATR Engine.

        Args:
            period (int): Number of periods for ATR calculation (default: 14).
            language (str): Language for error messages ("en" or "de").
        """
        self.period = period
        self.language = language.lower()

    def _error_message(self, error_type: str) -> str:
        """
        Returns error messages based on selected language.

        Args:
            error_type (str): Type of the error.

        Returns:
            str: Localized error message.
        """
        messages = {
            "invalid_df": {
                "en": "Invalid DataFrame provided to ATR Engine.",
                "de": "Ungültiges DataFrame an ATR Engine übergeben."
            },
            "zero_close": {
                "en": "Last close price is zero, cannot calculate ATR percent.",
                "de": "Letzter Schlusskurs ist null, ATR-Prozent kann nicht berechnet werden."
            }
        }
        return messages.get(error_type, {}).get(self.language, "Unknown error.")

    def calculate_atr_percent(self, df: pd.DataFrame) -> float:
        """
        Calculates ATR as a percentage of the last closing price.

        Args:
            df (pd.DataFrame): OHLCV DataFrame with 'high', 'low', 'close' columns.

        Returns:
            float: ATR percentage relative to the last close.
        """
        if df is None or len(df) < self.period or not all(col in df.columns for col in ['high', 'low', 'close']):
            raise ValueError(self._error_message("invalid_df"))

        df['high_low'] = df['high'] - df['low']
        df['high_close'] = (df['high'] - df['close'].shift()).abs()
        df['low_close'] = (df['low'] - df['close'].shift()).abs()

        df['true_range'] = df[['high_low', 'high_close', 'low_close']].max(axis=1)
        atr = df['true_range'].rolling(window=self.period, min_periods=1).mean().iloc[-1]

        last_close = df['close'].iloc[-1]

        if last_close == 0:
            raise ValueError(self._error_message("zero_close"))

        atr_percent = (atr / last_close) * 100

        # Cleanup
        df.drop(columns=['high_low', 'high_close', 'low_close', 'true_range'], inplace=True, errors='ignore')

        return round(atr_percent, 2)

    def detect_volatility_spike(self, df: pd.DataFrame, threshold_multiplier: float = 1.8) -> bool:
        """
        Detects if a volatility spike has occurred based on ATR percentage.

        Args:
            df (pd.DataFrame): OHLCV DataFrame.
            threshold_multiplier (float): Multiplier threshold for spike detection (default: 1.8).

        Returns:
            bool: True if spike detected, else False.
        """
        atr_percent = self.calculate_atr_percent(df)
        current_move_percent = ((df['high'].iloc[-1] - df['low'].iloc[-1]) / df['close'].iloc[-1]) * 100

        return current_move_percent > (atr_percent * threshold_multiplier)
