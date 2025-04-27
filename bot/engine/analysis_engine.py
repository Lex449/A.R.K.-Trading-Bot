# bot/engine/analysis_engine.py

import pandas as pd
import numpy as np
import os
import requests
from bot.engine.pattern_detector import detect_patterns
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
    Ultra Analysis Engine für Trading-Signale auf Basis von Realtime-Daten,
    kombiniert Pattern-Detection, Trend, RSI und Confidence Scoring.
    """
    try:
        # Candle-Daten abrufen
        candles_url = f"{FINNHUB_BASE_URL}/stock/candle"
        params = {
            "symbol": symbol,
            "resolution": "1",
            "count": 30,
            "token": FINNHUB_API_KEY
        }
        candles_resp = requests.get(candles_url, params=params).json()

        if candles_resp.get("s") != "ok":
            logger.warning(f"Failed to fetch candle data for {symbol}")
            return None

        # DataFrame aufbauen
        df = pd.DataFrame({
            "t": candles_resp["t"],
            "o": candles_resp["o"],
            "h": candles_resp["h"],
            "l": candles_resp["l"],
            "c": candles_resp["c"],
            "v": candles_resp["v"]
        })

        # Muster erkennen
        patterns = detect_patterns(df)

        if not patterns:
            return None  # Kein Signal = kein Spam

        # Signal zusammenbauen
        action_count = {"Long": 0, "Short": 0}
        total_confidence = 0

        pattern_details = []

        for p in patterns:
            pattern_details.append(
                f"Pattern: {p['pattern']}\n"
                f"Action: {'Long 📈' if p['action'] == 'Long' else 'Short 📉'}\n"
                f"Confidence: {p['confidence']}%\n"
                f"Rating: {'⭐' * p['stars']}\n"
            )
            action_count[p['action']] += 1
            total_confidence += p['confidence']

        # Combined Action
        if action_count["Long"] > action_count["Short"]:
            combined_action = "Ultra Long 📈"
        elif action_count["Short"] > action_count["Long"]:
            combined_action = "Ultra Short 📉"
        else:
            combined_action = "Neutral ⚪"

        # Durchschnittliches Confidence
        avg_confidence = total_confidence / len(patterns)

        return {
            "symbol": symbol,
            "patterns": pattern_details,
            "combined_action": combined_action,
            "avg_confidence": round(avg_confidence, 2),
            "pattern_count": len(patterns)
        }

    except Exception as e:
        logger.error(f"Error analyzing {symbol}: {e}")
        return None
