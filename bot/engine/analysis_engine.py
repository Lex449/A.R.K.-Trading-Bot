# bot/engine/analysis_engine.py

"""
Ultra Analysis Engine für Trading-Signale – Masterclass Build.
Kombiniert Candle-Patterns, Trendanalyse, RSI, EMA und Score-System.
"""

import pandas as pd
import numpy as np
import os
import requests
from bot.engine.pattern_detector import detect_patterns
from bot.engine.indicator_engine import evaluate_indicators
from bot.config.settings import get_settings
from bot.utils.logger import setup_logger

# Setup Logger
logger = setup_logger(__name__)

# Load Settings
config = get_settings()
FINNHUB_API_KEY = config["FINNHUB_API_KEY"]
FINNHUB_BASE_URL = "https://finnhub.io/api/v1"

async def analyze_symbol(symbol: str) -> dict:
    """
    Analysiert ein Symbol (Aktie) mit kombinierter Muster- und Indikatorlogik.

    Args:
        symbol (str): z.B. "AAPL", "MSFT", "NVDA"

    Returns:
        dict: Analyseergebnis oder None.
    """
    try:
        # --- Candle-Daten abrufen ---
        candles_url = f"{FINNHUB_BASE_URL}/stock/candle"
        params = {
            "symbol": symbol,
            "resolution": "1",  # 1-Minuten-Candles
            "count": 30,
            "token": FINNHUB_API_KEY,
        }
        response = requests.get(candles_url, params=params)
        candles_resp = response.json()

        if candles_resp.get("s") != "ok":
            logger.warning(f"[Analysis Engine] Candle-Request fehlgeschlagen für {symbol}.")
            return None

        df = pd.DataFrame({
            "t": candles_resp["t"],
            "o": candles_resp["o"],
            "h": candles_resp["h"],
            "l": candles_resp["l"],
            "c": candles_resp["c"],
            "v": candles_resp["v"],
        })

        if df.empty:
            logger.warning(f"[Analysis Engine] Leere Candle-Daten für {symbol}.")
            return None

        # --- Mustererkennung ---
        patterns = detect_patterns(df)
        if not patterns:
            logger.info(f"[Analysis Engine] Keine Muster erkannt für {symbol}.")
            return None

        # --- Indikatoren evaluieren (EMA, RSI) ---
        indicator_score, trend_direction = evaluate_indicators(df)

        # --- Signalstärke berechnen ---
        pattern_confidences = [p['confidence'] for p in patterns]
        avg_pattern_confidence = np.mean(pattern_confidences) if pattern_confidences else 0

        final_score = (avg_pattern_confidence * 0.6) + (indicator_score * 0.4)  # Gewichtung Muster 60%, Indikatoren 40%
        final_score = round(final_score, 2)

        # --- Sterne Rating (visuell) ---
        if final_score >= 85:
            stars = 5
        elif final_score >= 70:
            stars = 4
        elif final_score >= 55:
            stars = 3
        else:
            stars = 2  # Nur intern, 3 Sterne Mindestfilter bleibt bestehen

        # --- Combined Action (Long/Short/Neutral) ---
        action_votes = {"Long": 0, "Short": 0}
        for p in patterns:
            action_votes[p["action"]] += 1

        if action_votes["Long"] > action_votes["Short"]:
            combined_action = "Long 📈"
        elif action_votes["Short"] > action_votes["Long"]:
            combined_action = "Short 📉"
        else:
            combined_action = trend_direction  # Fallback auf EMA/RSI Trend

        # --- Super Signal ---
        super_signal = True if final_score >= 85 else False

        # --- Ergebnis liefern ---
        return {
            "symbol": symbol,
            "patterns": [p['pattern'] for p in patterns],
            "combined_action": combined_action,
            "avg_confidence": avg_pattern_confidence,
            "stars": stars,
            "score": final_score,
            "super_signal": super_signal,
        }

    except Exception as e:
        logger.error(f"[Analysis Engine] Fehler bei {symbol}: {e}")
        return None
