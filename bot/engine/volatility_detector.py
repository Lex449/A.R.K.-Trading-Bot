"""
A.R.K. Volatility Detector – Ultra Money Machine Precision 3.0
Detects high-quality volatility explosions live with dynamic ATR and percentage movement.

Engineered for: Faultless Real-Time Detection, Dynamic Adaptation, Premium Risk Filtering.
"""

import pandas as pd
import numpy as np
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

class VolatilityDetector:
    """
    A.R.K. Volatility Detector – Smart Adaptive Breakout Recognition.
    """

    def __init__(self, period: int = 14, threshold_multiplier: float = 1.7, language: str = "en"):
        """
        Args:
            period (int): Lookback period for ATR and volatility calculations.
            threshold_multiplier (float): Threshold multiplier for breakout detection.
            language (str): Localization ('en' or 'de').
        """
        self.period = period
        self.threshold_multiplier = threshold_multiplier
        self.language = language.lower()

    def detect_volatility_spike(self, df: pd.DataFrame) -> dict | None:
        """
        Detects real-time volatility spikes based on ATR and dynamic movement.

        Args:
            df (pd.DataFrame): DataFrame containing at least ['h', 'l', 'c'] columns.

        Returns:
            dict or None: Detailed volatility spike information, or None if no spike detected.
        """
        if df is None or df.empty or not all(col in df.columns for col in ["h", "l", "c"]):
            logger.warning("⚠️ [VolatilityDetector] Invalid or insufficient DataFrame provided.")
            return None

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

            current_atr = df["atr"].iloc[-1]
            avg_pct_change = df["pct_change"].rolling(window=self.period, min_periods=1).mean().iloc[-1]
            current_move = df["pct_change"].iloc[-1]

            # === Spike Condition ===
            spike_detected = current_move > avg_pct_change * self.threshold_multiplier

            if spike_detected:
                logger.info(
                    f"🚀 [VolatilityDetector] Spike Detected: {current_move:.2f}% vs Avg {avg_pct_change:.2f}% | ATR={current_atr:.4f}"
                )
                return {
                    "volatility_spike": True,
                    "current_move_percent": round(current_move, 2),
                    "average_move_percent": round(avg_pct_change, 2),
                    "current_atr": round(current_atr, 4)
                }

            return None

        except Exception as e:
            logger.error(f"❌ [VolatilityDetector Critical Error] {e}")
            return None

        finally:
            # === Clean Temporary Columns ===
            df.drop(columns=["high_low", "high_close", "low_close", "true_range", "atr", "pct_change"], inplace=True, errors="ignore")
