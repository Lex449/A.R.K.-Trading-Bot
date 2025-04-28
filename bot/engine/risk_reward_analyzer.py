"""
A.R.K. Risk-Reward Analyzer – Ultra Strategic Build.
Precision-engineered for smarter trades, tighter stops, and dynamic targets.
"""

import pandas as pd
from bot.utils.logger import setup_logger

# Setup Logger
logger = setup_logger(__name__)

class RiskRewardAnalyzer:
    """
    Calculates dynamic Risk/Reward setups based on current volatility and momentum.
    """

    def __init__(self, language: str = "en"):
        self.language = language.lower()

    def estimate(self, df: pd.DataFrame, combined_action: str) -> dict:
        """
        Smartly estimates the risk/reward profile based on latest price behavior.

        Args:
            df (pd.DataFrame): OHLCV data.
            combined_action (str): "Long 📈" or "Short 📉".

        Returns:
            dict or None
        """
        if df is None or df.empty or combined_action not in ("Long 📈", "Short 📉"):
            logger.warning("⚠️ [RiskReward] Invalid input detected.")
            return None

        try:
            highs = df["h"].tail(20)
            lows = df["l"].tail(20)
            closes = df["c"].tail(20)

            current_price = closes.iloc[-1]
            highest_high = highs.max()
            lowest_low = lows.min()

            volatility = (highs.max() - lows.min()) / closes.mean()

            if combined_action == "Long 📈":
                stop_loss = lowest_low * 0.996  # Tighter for high precision
                target = current_price * (1.012 if volatility > 0.02 else 1.015)
            else:  # Short 📉
                stop_loss = highest_high * 1.004
                target = current_price * (0.988 if volatility > 0.02 else 0.985)

            risk = abs(current_price - stop_loss)
            reward = abs(target - current_price)

            if risk == 0:
                logger.warning("⚠️ [RiskReward] Zero risk detected, skipping.")
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
            logger.error(f"❌ [RiskReward] Critical failure: {e}")
            return None
