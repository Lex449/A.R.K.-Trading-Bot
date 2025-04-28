"""
A.R.K. Risk-Reward Analyzer – Smart Trade Evaluation System.
Estimates realistic reward/risk ratios for smarter entries and safer trades.
"""

import pandas as pd

class RiskRewardAnalyzer:
    """
    A.R.K. Risk-Reward Analyzer
    Dynamically calculates realistic Risk/Reward setups for trades.
    """

    def __init__(self, language: str = "en"):
        """
        Initializes the Risk/Reward Analyzer.

        Args:
            language (str): Language ("en" or "de") for localized error messages.
        """
        self.language = language.lower()

    def _error_message(self, error_type: str) -> str:
        """
        Returns localized error messages.

        Args:
            error_type (str): Type of the error.

        Returns:
            str: Localized error message.
        """
        messages = {
            "invalid_input": {
                "en": "Invalid DataFrame or action provided to Risk-Reward Analyzer.",
                "de": "Ungültiges DataFrame oder Aktion an Risk-Reward Analyzer übergeben."
            }
        }
        return messages.get(error_type, {}).get(self.language, "Unknown error.")

    def estimate(self, df: pd.DataFrame, combined_action: str) -> dict:
        """
        Estimates the Risk/Reward based on the latest price action.

        Args:
            df (pd.DataFrame): OHLCV DataFrame with columns ['h', 'l', 'c'].
            combined_action (str): Expected trade direction ("Long 📈" or "Short 📉").

        Returns:
            dict or None: Risk-Reward data or None if not applicable.
        """
        if df is None or df.empty or combined_action not in ("Long 📈", "Short 📉"):
            raise ValueError(self._error_message("invalid_input"))

        try:
            recent_closes = df["c"].tail(20)
            recent_highs = df["h"].tail(20)
            recent_lows = df["l"].tail(20)

            current_price = recent_closes.iloc[-1]
            recent_high = recent_highs.max()
            recent_low = recent_lows.min()

            if combined_action == "Long 📈":
                stop_loss = recent_low * 0.995  # 0.5% under recent low
                target = current_price * 1.015  # 1.5% above current price
            else:  # Short 📉
                stop_loss = recent_high * 1.005  # 0.5% above recent high
                target = current_price * 0.985  # 1.5% below current price

            risk = abs(current_price - stop_loss)
            reward = abs(target - current_price)

            if risk == 0:
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

        except Exception:
            return None
