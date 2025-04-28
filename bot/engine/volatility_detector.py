"""
A.R.K. Volatility Detector – Ultra Precision Volatility Engine.
Detects real-time volatility spikes for smarter trading decisions.
"""

import pandas as pd
import numpy as np
from bot.utils.logger import setup_logger

# Logger Setup
logger = setup_logger(__name__)

class VolatilityDetector:
    """
    Detects significant volatility based on ATR and percentage movement.
    """

    def __init__(self, period: int = 14, threshold_multiplier: float = 1.8, language: str = "en"):
        self.period = period
        self.threshold_multiplier = threshold_multiplier
        self.language = language.lower()

    def detect_volatility_spike(self, df: pd.DataFrame) -> dict:
        """
        Detects sudden volatility spikes.

        Args:
            df (pd.DataFrame): Market OHLCV DataFrame.

        Returns:
            dict or None: Volatility event details or None.
        """
        try:
            if df is None or df.empty or not all(col in df.columns for col in ['h', 'l', 'c']):
                logger.warning("[Volatility Detector] Invalid DataFrame provided.")
                return None

            # True Range Calculation
            df["high_low"] = df["h"] - df["l"]
            df["high_close"] = (df["h"] - df["c"].shift()).abs()
            df["low_close"] = (df["l"] - df["c"].shift()).abs()

            df["true_range"] = df[["high_low", "high_close", "low_close"]].max(axis=1)

            # ATR Calculation
            df["atr"] = df["true_range"].rolling(window=self.period, min_periods=1).mean()

            # Percentage Movement
            df["pct_change"] = df["c"].pct_change().abs() * 100

            avg_move = df["pct_change"].rolling(window=self.period, min_periods=1).mean().iloc[-1]
            current_move = df["pct_change"].iloc[-1]

            if current_move > avg_move * self.threshold_multiplier:
                return {
                    "volatility_spike": True,
                    "current_move_percent": round(current_move, 2),
                    "average_move_percent": round(avg_move, 2),
                    "current_atr": round(df["atr"].iloc[-1], 4)
                }

            return None

        except Exception as e:
            logger.error(f"[Volatility Detector] Critical error: {e}")
            return None
