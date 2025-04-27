# bot/engine/risk_reward_analyzer.py

"""
A.R.K. Risk-Reward Analyzer – Smart Trade Evaluation System.
Estimates realistic reward/risk ratios for better decision-making.

Engineered for: Smarter Entries, Safer Trades, Dynamic Risk Management.
"""

import pandas as pd

class RiskRewardAnalyzer:
    """
    A.R.K. Risk-Reward Analyzer
    Bewertet mögliche Trades basierend auf aktueller Marktvolatilität und Trendrichtung.
    """

    def __init__(self, language: str = "en"):
        """
        Initialisiert den Risk/Reward Analyzer.

        Args:
            language (str): Sprache für Fehlerbehandlung ("en" oder "de").
        """
        self.language = language.lower()

    def _error_message(self, error_type: str) -> str:
        """
        Liefert lokalisierte Fehlernachrichten.

        Args:
            error_type (str): Typ des Fehlers.

        Returns:
            str: Fehlermeldung in der ausgewählten Sprache.
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
        Schätzt das Risiko/Ertrags-Verhältnis basierend auf den letzten Kursbewegungen.

        Args:
            df (pd.DataFrame): OHLCV DataFrame mit Spalten ['h', 'l', 'c'].
            combined_action (str): Erwartete Trade-Richtung ("Long 📈" oder "Short 📉").

        Returns:
            dict or None: Enthält Preis, Stop-Loss, Target, Risiko, Ertrag, RRR.
        """
        if df is None or df.empty or combined_action not in ("Long 📈", "Short 📉"):
            raise ValueError(self._error_message("invalid_input"))

        try:
            # Nur die letzten 20 Kerzen verwenden
            recent_closes = df['c'].tail(20)
            recent_highs = df['h'].tail(20)
            recent_lows = df['l'].tail(20)

            current_price = recent_closes.iloc[-1]
            recent_high = recent_highs.max()
            recent_low = recent_lows.min()

            if combined_action == "Long 📈":
                stop_loss = recent_low * 0.995  # 0.5% unter letztem Support
                target = current_price * 1.015  # 1.5% über Entry
            else:  # Short 📉
                stop_loss = recent_high * 1.005  # 0.5% über letztem Widerstand
                target = current_price * 0.985  # 1.5% unter Entry

            risk = abs(current_price - stop_loss)
            reward = abs(target - current_price)

            # Division durch Null vermeiden
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
