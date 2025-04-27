# bot/engine/volatility_detector.py

"""
A.R.K. Volatility Detector – Detects High Volatility Events in Real-Time.
Core component for smarter trading signals and dynamic risk assessment.

Engineered for: Smarter Entries, Risk Management, Crash Prevention.
"""

import pandas as pd
import numpy as np

class VolatilityDetector:
    """
    A.R.K. Volatility Detector
    Erfasst plötzliche Volatilitätsspitzen auf Basis von ATR und Preisbewegung.
    """

    def __init__(self, period: int = 14, threshold_multiplier: float = 1.8, language: str = "en"):
        """
        Initialisiert den Volatility Detector.

        Args:
            period (int): Perioden für ATR- und Durchschnittsberechnung.
            threshold_multiplier (float): Schwellenwert für die Spike-Erkennung.
            language (str): Sprache ("en" oder "de").
        """
        self.period = period
        self.threshold_multiplier = threshold_multiplier
        self.language = language.lower()

    def _error_message(self, error_type: str) -> str:
        """
        Liefert Fehlertexte je nach Sprache.

        Args:
            error_type (str): Typ des Fehlers.

        Returns:
            str: Lokalisierte Fehlermeldung.
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
        Ermittelt, ob ein signifikanter Volatilitätssprung vorliegt.

        Args:
            df (pd.DataFrame): OHLCV DataFrame mit Spalten ['h', 'l', 'c'].

        Returns:
            dict or None: Details zum Volatilitätsevent oder None bei keinem Ereignis.
        """
        if df is None or df.empty or not all(col in df.columns for col in ['h', 'l', 'c']):
            raise ValueError(self._error_message("invalid_df"))

        try:
            # True Range berechnen
            df['high_low'] = df['h'] - df['l']
            df['high_close'] = (df['h'] - df['c'].shift()).abs()
            df['low_close'] = (df['l'] - df['c'].shift()).abs()

            df['true_range'] = df[['high_low', 'high_close', 'low_close']].max(axis=1)

            # ATR berechnen
            df['atr'] = df['true_range'].rolling(window=self.period, min_periods=1).mean()

            # Prozentuale Veränderung pro Kerze
            df['pct_change'] = df['c'].pct_change().abs() * 100

            # Durchschnittliche Bewegung
            avg_move = df['pct_change'].rolling(window=self.period, min_periods=1).mean().iloc[-1]
            current_move = df['pct_change'].iloc[-1]

            # Spike Erkennung
            if current_move > avg_move * self.threshold_multiplier:
                return {
                    "volatility_spike": True,
                    "current_move_percent": round(current_move, 2),
                    "average_move_percent": round(avg_move, 2),
                    "current_atr": round(df['atr'].iloc[-1], 4)
                }

            return None

        except Exception as e:
            # Sanftes Scheitern ohne Crash
            return None
