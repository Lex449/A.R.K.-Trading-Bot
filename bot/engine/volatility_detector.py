"""
A.R.K. Volatility Detector – Ultra Money Machine Precision.
Detects high-quality volatility breakouts in real-time trading conditions.
"""

import pandas as pd
import numpy as np
from bot.utils.logger import setup_logger

# Setup Logger
logger = setup_logger(__name__)

class VolatilityDetector:
    """
    Detects serious volatility explosions using adaptive ATR and percentage movement.
    """

    def __init__(self, period: int = 14, threshold_multiplier: float = 1.7, language: str = "en"):
        """
        Args:
            period (int): ATR calculation window.
            threshold_multiplier (float): How extreme movement must be to trigger detection.
            language (str): 'en' or 'de' for localized messages.
        """
        self.period = period
        self.threshold_multiplier = threshold_multiplier
        self.language = language.lower()

    def detect_volatility_spike(self, df: pd.DataFrame) -> dict:
        """
        Detects high-priority volatility spikes.

        Args:
            df (pd.DataFrame): DataFrame ['o', 'h', 'l', 'c'] minimum required.

        Returns:
            dict or None: Volatility alert information.
        """
        if df is None or df.empty or not all(col in df.columns for col in ['h', 'l', 'c']):
            logger.warning("⚠️ [Volatility Detector] Invalid or missing data.")
            return None

        try:
            # True Range calculation
            df["high_low"] = df["h"] - df["l"]
            df["high_close"] = (df["h"] - df["c"].shift()).abs()
            df["low_close"] = (df["l"] - df["c"].shift()).abs()

            df["true_range"] = df[["high_low", "high_close", "low_close"]].max(axis=1)

            # ATR calculation
            df["atr"] = df["true_range"].rolling(window=self.period, min_periods=1).mean()

            # Percentage Change calculation
            df["pct_change"] = df["c"].pct_change().abs() * 100

            current_atr = df["atr"].iloc[-1]
            avg_pct_change = df["pct_change"].rolling(window=self.period, min_periods=1).mean().iloc[-1]
            current_move = df["pct_change"].iloc[-1]

            # Spike Detection
            spike_condition = current_move > avg_pct_change * self.threshold_multiplier

            if spike_condition:
                logger.info(f"🚨 [Volatility Detector] Spike detected: Move {current_move:.2f}% vs Avg {avg_pct_change:.2f}%")
                return {
                    "volatility_spike": True,
                    "current_move_percent": round(current_move, 2),
                    "average_move_percent": round(avg_pct_change, 2),
                    "current_atr": round(current_atr, 4)
                }

            return None

        except Exception as e:
            logger.error(f"❌ [Volatility Detector] Critical error: {e}")
            return None
