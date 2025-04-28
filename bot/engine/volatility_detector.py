"""
A.R.K. Volatility Detector – Real-Time High Volatility Recognition.
Optimized for smarter signals, risk management, and crash prevention.
"""

import pandas as pd
import numpy as np

class VolatilityDetector:
    """
    Detects sudden volatility spikes based on ATR and price movement.
    Engineered for the A.R.K. Ultra Precision System.
    """

    def __init__(self, period: int = 14, threshold_multiplier: float = 1.8, language: str = "en"):
        """
        Initializes the Volatility Detector.

        Args:
            period (int): Period for ATR and movement averages.
            threshold_multiplier (float): Spike detection threshold.
            language (str): Language code ("en" or "de").
        """
        self.period = period
        self.threshold_multiplier = threshold_multiplier
        self.language = language.lower()

    def _error_message(self, error_type: str) -> str:
        """
        Returns localized error messages.

        Args:
            error_type (str): The error identifier.

        Returns:
            str: Localized error message.
        """
        messages = {
            "invalid_df": {
                "en": "Invalid DataFrame provided to Volatility Detector.",
                "de": "Ungültiges DataFrame an Volatility Detector übergeben."
            }
        }
        return messages.get(error_type, {}).get(self.language, "Unknown error.")

    def detect_volatility_spike(self, df: pd.DataFrame) -> dict:
        """
        Detects if a significant volatility spike has occurred.

        Args:
            df (pd.DataFrame): DataFrame with columns ['h', 'l', 'c'].

        Returns:
            dict or None: Volatility event details or None if no event.
        """
        if df is None or df.empty or not all(col in df.columns for col in ['h', 'l', 'c']):
            raise ValueError(self._error_message("invalid_df"))

        try:
            # === True Range Calculation ===
            df["high_low"] = df["h"] - df["l"]
            df["high_close"] = (df["h"] - df["c"].shift()).abs()
            df["low_close"] = (df["l"] - df["c"].shift()).abs()

            df["true_range"] = df[["high_low", "high_close", "low_close"]].max(axis=1)

            # === ATR Calculation ===
            df["atr"] = df["true_range"].rolling(window=self.period, min_periods=1).mean()

            # === Percentage Movement Calculation ===
            df["pct_change"] = df["c"].pct_change().abs() * 100

            avg_move = df["pct_change"].rolling(window=self.period, min_periods=1).mean().iloc[-1]
            current_move = df["pct_change"].iloc[-1]

            # === Volatility Spike Detection ===
            if current_move > avg_move * self.threshold_multiplier:
                return {
                    "volatility_spike": True,
                    "current_move_percent": round(current_move, 2),
                    "average_move_percent": round(avg_move, 2),
                    "current_atr": round(df["atr"].iloc[-1], 4)
                }

            return None

        except Exception:
            # Fail gracefully without crash
            return None
