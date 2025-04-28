"""
A.R.K. Risk-Reward Analyzer – Strategic Trade Optimizer.
Calculates dynamic risk-reward profiles for precision trading.
"""

import pandas as pd
from bot.utils.logger import setup_logger

# Logger Setup
logger = setup_logger(__name__)

class RiskRewardAnalyzer:
    """
    Calculates optimized risk-reward setups based on current market structure.
    """

    def __init__(self, language: str = "en"):
        self.language = language.lower()

    def estimate(self, df: pd.DataFrame, combined_action: str) -> dict:
        """
        Estimates the risk/reward metrics for a given trade action.

        Args:
            df (pd.DataFrame): OHLCV market data.
            combined_action (str): "Long 📈" or "Short 📉".

        Returns:
            dict or None: Risk/Reward profile or None on failure.
        """
        try:
            if df is None or df.empty or combined_action not in ("Long 📈", "Short 📉"):
                logger.warning("[RiskRewardAnalyzer] Invalid input for estimation.")
                return None

            highs = df["h"].tail(20)
            lows = df["l"].tail(20)
            closes = df["c"].tail(20)

            current_price = closes.iloc[-1]
            highest_high = highs.max()
            lowest_low = lows.min()

            if combined_action == "Long 📈":
                stop_loss = lowest_low * 0.995
                target = current_price * 1.015
            else:
                stop_loss = highest_high * 1.005
                target = current_price * 0.985

            risk = abs(current_price - stop_loss)
            reward = abs(target - current_price)

            if risk == 0:
                logger.warning("[RiskRewardAnalyzer] Zero risk scenario detected.")
                return None

            risk_reward_ratio = round(reward / risk, 2)

            return {
                "current_price": round(current_price, 4),
                "stop_loss": round(stop_loss, 4),
                "target": round(target, 4),
                "risk": round(risk, 4),
                "reward": round(reward, 4),
                "risk_reward_ratio": risk_reward_ratio
            }

        except Exception as e:
            logger.error(f"[RiskRewardAnalyzer] Error estimating risk/reward: {e}")
            return None
