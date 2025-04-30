# bot/engine/volatility_engine.py

"""
A.R.K. Volatility Engine – Ultra Adaptive Breakout & Risk Filter 2025
Fusion aus Volatility Detector & Volatility Guard.

Built for: Real-Time Spike Detection, Adaptive Confidence Tuning, Smart Risk Defense.
Made in Bali. Engineered with German Precision.
"""

import pandas as pd
import numpy as np
import statistics
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

class VolatilityEngine:
    """
    A.R.K. Volatility Engine
    Combines real-time volatility spike detection and smart risk-based signal adjustment.
    """

    def __init__(self, period: int = 14, threshold_multiplier: float = 1.7, language: str = "en"):
        self.period = period
        self.threshold_multiplier = threshold_multiplier
        self.language = language.lower()

    def detect_volatility_spike(self, df: pd.DataFrame) -> dict | None:
        """
        Detects sudden volatility spikes based on dynamic ATR and price changes.

        Args:
            df (pd.DataFrame): OHLCV DataFrame.

        Returns:
            dict or None
        """
        if df is None or df.empty or not all(col in df.columns for col in ["h", "l", "c"]):
            logger.warning("⚠️ [VolatilityEngine] Invalid DataFrame for spike detection.")
            return None

        try:
            # True Range Calculation
            df["high_low"] = df["h"] - df["l"]
            df["high_close"] = (df["h"] - df["c"].shift()).abs()
            df["low_close"] = (df["l"] - df["c"].shift()).abs()
            df["true_range"] = df[["high_low", "high_close", "low_close"]].max(axis=1)

            # ATR Calculation
            df["atr"] = df["true_range"].rolling(window=self.period, min_periods=1).mean()

            # Percent Movement Calculation
            df["pct_change"] = df["c"].pct_change().abs() * 100

            current_atr = df["atr"].iloc[-1]
            avg_pct_change = df["pct_change"].rolling(window=self.period, min_periods=1).mean().iloc[-1]
            current_move = df["pct_change"].iloc[-1]

            # Spike Detection Logic
            spike_detected = current_move > avg_pct_change * self.threshold_multiplier

            if spike_detected:
                logger.info(f"🚀 [VolatilityEngine] Volatility Spike Detected: {current_move:.2f}% vs Avg {avg_pct_change:.2f}% | ATR={current_atr:.4f}")
                return {
                    "volatility_spike": True,
                    "current_move_percent": round(current_move, 2),
                    "average_move_percent": round(avg_pct_change, 2),
                    "current_atr": round(current_atr, 4)
                }

            return None

        except Exception as e:
            logger.error(f"❌ [VolatilityEngine] Critical Error: {e}")
            return None

        finally:
            df.drop(columns=["high_low", "high_close", "low_close", "true_range", "atr", "pct_change"], inplace=True, errors="ignore")

    def is_high_volatility_phase(self, candles: list[dict]) -> bool:
        """
        Analyzes if the market is currently in a high volatility phase.

        Args:
            candles (list[dict]): List of last candles with 'high' and 'low' prices.

        Returns:
            bool
        """
        if not candles or len(candles) < 10:
            return False

        try
