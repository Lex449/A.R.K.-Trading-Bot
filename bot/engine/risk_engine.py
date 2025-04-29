# bot/engine/risk_engine.py

"""
A.R.K. Risk Engine – Ultra Precision Signal Evaluator 5.0
Fuses Risk Manager, Analyzer, Calculator & Estimator into one ultimate precision module.
Designed for: Smart Risk Control, Signal Validation, Dynamic RRR Estimation.
"""

import logging
import pandas as pd

# Setup structured logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# === Ultra Signal Risk Assessment ===
async def assess_signal_risk(signal_data: dict) -> tuple:
    """
    Evaluates a trading signal with:
    - Stars (Signal Quality)
    - Confidence %
    - RSI Status
    Returns:
        (Formatted Message: str, Is High Risk: bool)
    """
    stars = signal_data.get("stars", 0)
    confidence = signal_data.get("confidence", 0.0)
    pattern = signal_data.get("pattern", "Unknown")
    rsi = signal_data.get("rsi", None)

    try:
        rating_text = (
            "✅ *Elite Signal (5⭐)* – _Masterpiece Setup._" if stars == 5 else
            "✅ *High-Quality Signal (4⭐)* – _Strong probability._" if stars == 4 else
            "⚠️ *Moderate Signal (3⭐)* – _Needs confirmation._" if stars == 3 else
            "❌ *Weak Signal* – _Avoid trading._"
        )

        confidence_text = f"*Confidence:* `{confidence:.1f}%`"
        confidence_warn = "\n❗ *Warning: Confidence below 55%.*" if confidence < 55 else ""

        rsi_text = ""
        if isinstance(rsi, (int, float)):
            if rsi > 70:
                rsi_text = "\n🔴 *RSI Overbought (>70)* – Caution Long."
            elif rsi < 30:
                rsi_text = "\n🔵 *RSI Oversold (<30)* – Caution Short."

        action_suggestion = (
            "🚀 *Strong Buy Setup*" if stars >= 4 and confidence >= 70 else
            "📈 *Potential Buy (Caution)*" if stars >= 4 and confidence >= 60 else
            "👀 *Watchlist Candidate*" if stars == 3 and confidence >= 60 else
            "❌ *Avoid Trade*"
        )

        message = (
            f"⚡ *Risk Assessment*\n\n"
            f"*Pattern:* `{pattern}`\n"
            f"{confidence_text}\n"
            f"*Rating:* {'⭐' * stars}\n\n"
            f"{rating_text}{confidence_warn}{rsi_text}\n\n"
            f"📢 *Suggested Action:* {action_suggestion}"
        )

        high_risk = stars < 3 or confidence < 55
        logger.info(f"[RiskEngine] Assessed {pattern}: {stars}⭐ | {confidence:.1f}%")
        return message, high_risk

    except Exception as e:
        logger.error(f"[RiskEngine Error] {e}")
        return "⚠️ *Risk Assessment Failed.* Proceed with Caution.", True

# === Dynamic Risk/Reward Analyzer ===
def analyze_risk_reward(df: pd.DataFrame, action: str) -> dict | None:
    """
    Calculates a smart Risk/Reward Ratio based on last 20 candles.
    Args:
        df (pd.DataFrame): Market data
        action (str): "Long 📈" or "Short 📉"
    Returns:
        dict: RRR data
    """
    if df is None or df.empty or action not in ("Long 📈", "Short 📉"):
        return None

    try:
        highs = df["h"].tail(20)
        lows = df["l"].tail(20)
        closes = df["c"].tail(20)

        current_price = closes.iloc[-1]
        highest_high = highs.max()
        lowest_low = lows.min()

        volatility = (highs.max() - lows.min()) / closes.mean()

        if action == "Long 📈":
            stop_loss = lowest_low * 0.996
            target = current_price * (1.012 if volatility > 0.02 else 1.015)
        else:
            stop_loss = highest_high * 1.004
            target = current_price * (0.988 if volatility > 0.02 else 0.985)

        risk = abs(current_price - stop_loss)
        reward = abs(target - current_price)

        if risk == 0:
            return None

        return {
            "current_price": round(current_price, 4),
            "stop_loss": round(stop_loss, 4),
            "target": round(target, 4),
            "risk": round(risk, 4),
            "reward": round(reward, 4),
            "risk_reward_ratio": round(reward / risk, 2)
        }

    except Exception as e:
        logger.error(f"[RiskEngine RRR Error] {e}")
        return None

# === Lightweight Risk Calculator ===
def basic_risk_reward(df: pd.DataFrame, action: str) -> dict | None:
    """
    Simple Risk/Reward Ratio calculation.
    """
    if df is None or df.empty or action not in ["Long", "Short"]:
        return None

    try:
        high = df["h"].rolling(window=20).max().iloc[-1]
        low = df["l"].rolling(window=20).min().iloc[-1]
        close = df["c"].iloc[-1]

        if close <= 0:
            return None

        if action == "Long":
            risk = ((close - low) / close) * 100
            reward = ((high - close) / close) * 100
        else:
            risk = ((high - close) / close) * 100
            reward = ((close - low) / close) * 100

        if risk <= 0:
            return None

        return {
            "risk_percent": round(risk, 2),
            "reward_percent": round(reward, 2),
            "risk_reward_ratio": round(reward / risk, 2),
            "stop_loss": round(low if action == "Long" else high, 4),
            "target": round(high if action == "Long" else low, 4),
        }

    except Exception as e:
        logger.error(f"[RiskEngine Basic RRR Error] {e}")
        return None

# === Advanced Entry-based Estimator ===
def estimate_rr_with_entry(df: pd.DataFrame, entry_price: float, direction: str) -> dict:
    """
    Estimates Risk/Reward based on custom entry point.
    """
    if df is None or df.empty or entry_price <= 0 or direction.lower() not in {"long", "short"}:
        return {"risk": None, "reward": None, "rr_ratio": None}

    try:
        recent_high = df["h"].tail(20).max()
        recent_low = df["l"].tail(20).min()

        if pd.isna(recent_high) or pd.isna(recent_low):
            return {"risk": None, "reward": None, "rr_ratio": None}

        if direction.lower() == "long":
            risk = max(entry_price - recent_low, 0)
            reward = max(recent_high - entry_price, 0)
        else:
            risk = max(recent_high - entry_price, 0)
            reward = max(entry_price - recent_low, 0)

        if risk == 0 or reward == 0:
            return {"risk": None, "reward": None, "rr_ratio": None}

        return {
            "risk": round(risk, 4),
            "reward": round(reward, 4),
            "rr_ratio": round(reward / risk, 2)
        }

    except Exception as e:
        logger.error(f"[RiskEngine Estimate RRR Error] {e}")
        return {"risk": None, "reward": None, "rr_ratio": None}
