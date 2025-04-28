"""
A.R.K. Risk-Reward Analyzer – Smart Trade Evaluation System.
Ultra Masterclass Build – Precision meets Practicality.
"""

import pandas as pd

class RiskRewardAnalyzer:
    def __init__(self, language: str = "en"):
        self.language = language.lower()

    def _error_message(self, error_type: str) -> str:
        messages = {
            "invalid_input": {
                "en": "Invalid DataFrame or action provided to Risk-Reward Analyzer.",
                "de": "Ungültiges DataFrame oder Aktion an Risk-Reward Analyzer übergeben."
            }
        }
        return messages.get(error_type, {}).get(self.language, "Unknown error.")

    def estimate(self, df: pd.DataFrame, combined_action: str) -> dict:
        if df is None or df.empty or combined_action not in ("Ultra Long 📈", "Ultra Short 📉"):
            raise ValueError(self._error_message("invalid_input"))

        try:
            recent_highs = df["h"].tail(20)
            recent_lows = df["l"].tail(20)
            recent_closes = df["c"].tail(20)

            current_price = recent_closes.iloc[-1]
            highest_high = recent_highs.max()
            lowest_low = recent_lows.min()

            if combined_action == "Ultra Long 📈":
                stop_loss = lowest_low * 0.995
                target = current_price * 1.015
            else:
                stop_loss = highest_high * 1.005
                target = current_price * 0.985

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
