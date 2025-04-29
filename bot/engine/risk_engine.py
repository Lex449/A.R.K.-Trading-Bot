"""
A.R.K. Risk Engine – Ultra Precision Signal Evaluator 4-in-1
Vereint Risk Manager, Analyzer, Calculator & Estimator für maximale Effizienz.
"""

import logging
import pandas as pd

# Setup structured logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# === Signal Risk Assessment ===
async def assess_signal_risk(signal_data: dict) -> tuple:
    """
    Evaluates a trading signal using:
    - Star Rating (Signal Quality)
    - Confidence %
    - RSI Value
    Returns: (Formatted Message: str, Is High Risk: bool)
    """
    stars = signal_data.get("stars", 0)
    confidence = signal_data.get("confidence", 0.0)
    pattern = signal_data.get("pattern", "Unknown Pattern")
    rsi = signal_data.get("rsi")

    try:
        rating_text = (
            "✅ *Ultra High-Quality Signal (5⭐)* – _Technical Masterpiece._" if stars == 5 else
            "✅ *Strong Signal (4⭐)* – _High probability trade._" if stars == 4 else
            "⚠️ *Moderate Signal (3⭐)* – _Needs confirmation._" if stars == 3 else
            "❌ *Weak Signal (<3⭐)* – _Trade not recommended._"
        )

        confidence_text = f"*Confidence:* `{confidence:.1f}%`"
        confidence_note = "\n❗ *Warning: Low Confidence (<55%).*" if confidence < 55 else ""

        rsi_text = ""
        if isinstance(rsi, (int, float)):
            if rsi > 70:
                rsi_text = "\n🔴 *RSI: Overbought (>70)* – _Caution on Long entries._"
            elif rsi < 30:
                rsi_text = "\n🔵 *RSI: Oversold (<30)* – _Caution on Short entries._"

        suggested_action = (
            "🚀 *Strong Buy Setup*" if stars >= 4 and confidence >= 70 else
            "📈 *Potential Buy – Caution Advised*" if stars >= 4 and confidence >= 60 else
            "👀 *Watchlist Candidate*" if stars == 3 and confidence >= 60 else
            "❌ *Avoid Trade – Too Risky*"
        )

        message = (
            f"⚡ *Risk Analysis*\n\n"
            f"*Pattern:* `{pattern}`\n"
            f"{confidence_text}\n"
            f"*Rating:* {'⭐' * stars}\n\n"
            f"{rating_text}{confidence_note}{rsi_text}\n\n"
            f"📢 *Suggested Action:* {suggested_action}"
        )

        is_high_risk = stars < 3 or confidence < 55
        logger.info(f"[RiskEngine] Evaluated {pattern}: {stars}⭐, {confidence:.1f}%")
        return message, is_high_risk

    except Exception as e:
        logger.error(f"[RiskEngine Critical] {e}")
        return "⚠️ *Risk Analysis Failed.* _Trade at your own risk._", True


# === Risk/Reward Analyzer v3.0 ===
def analyze_risk_reward(df: pd.DataFrame, action: str) -> dict | None:
    """
    Dynamische RRR Analyse. Verwendet letzte 20 Kerzen.
    Args:
        df (pd.DataFrame): OHLCV
        action (str): "Long 📈" or "Short 📉"
    Returns:
        dict with stop loss, target, RRR etc.
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
        logger.error(f"[RiskEngine RRR] Critical failure: {e}")
        return None


# === Lightweight Calculator ===
def basic_risk_reward(df: pd.DataFrame, action: str) -> dict | None:
    """
    Simple RRR-Messung ohne Entry Price.
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
            stop_loss = low
            target = high
        else:
            risk = ((high - close) / close) * 100
            reward = ((close - low) / close) * 100
            stop_loss = high
            target = low

        return {
            "risk_percent": round(risk, 2),
            "reward_percent": round(reward, 2),
            "risk_reward_ratio": round(reward / risk, 2) if risk > 0 else 0.0,
            "stop_loss": round(stop_loss, 2),
            "target": round(target, 2),
        }

    except Exception:
        return None


# === Estimator mit Entry Price ===
def estimate_rr_with_entry(df: pd.DataFrame, entry_price: float, direction: str) -> dict:
    """
    Entry-basierte RRR-Schätzung mit Fallbacks.
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

    except Exception:
        return {"risk": None, "reward": None, "rr_ratio": None}
