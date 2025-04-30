# bot/engine/risk_engine.py

"""
A.R.K. Risk Engine – Ultra Precision Signal Evaluator 9.1
Strategic RRR Analytics + Dynamic Signal Assessment + Watchlist Tiering ab 50 %.

Built for: Institutional-Grade Validation, Real-Time Clarity, and Adaptive Signal Triage.
Made in Bali. Engineered with German Precision.
"""

import logging
import pandas as pd

# Setup structured logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# === 1. Signal Assessment Engine ===
async def assess_signal_risk(signal_data: dict) -> tuple:
    stars = signal_data.get("stars", 0)
    confidence = signal_data.get("confidence", 0.0)
    pattern = signal_data.get("pattern", "Unknown")
    rsi = signal_data.get("rsi", None)

    try:
        risk_level = (
            "✅ Elite Signal" if stars == 5 else
            "✅ Strong Signal" if stars == 4 else
            "⚠️ Moderate Signal" if stars == 3 else
            "❌ Weak Signal"
        )

        rsi_note = ""
        if isinstance(rsi, (int, float)):
            if rsi > 70:
                rsi_note = "\n🔴 *RSI Overbought (>70)* – Caution for Longs."
            elif rsi < 30:
                rsi_note = "\n🔵 *RSI Oversold (<30)* – Caution for Shorts."

        action_tip = (
            "🚀 *Prime Trade Candidate*" if stars >= 4 and confidence >= 75 else
            "📈 *Opportunity Detected*" if stars >= 3 and confidence >= 60 else
            "👀 *Watchlist Entry – Use Filters*" if confidence >= 50 else
            "❌ *Avoid Trade – Risk Too High*"
        )

        message = (
            f"⚡ *Risk Evaluation*\n\n"
            f"*Pattern:* `{pattern}`\n"
            f"*Confidence:* `{confidence:.1f}%`\n"
            f"*Rating:* {'⭐' * stars} ({risk_level})\n"
            f"{rsi_note}\n\n"
            f"📢 *Action Recommendation:* {action_tip}"
        )

        is_risky = stars < 3 or confidence < 55
        logger.info(f"[RiskEngine] {pattern} | {stars}⭐ | {confidence:.1f}% | High Risk: {is_risky}")
        return message, is_risky

    except Exception as e:
        logger.error(f"[RiskEngine Critical Error] {e}")
        return "⚠️ *Risk Assessment Failed.* Stay cautious.", True

# === 2. Smart Risk/Reward Analyzer ===
def analyze_risk_reward(df: pd.DataFrame, action: str) -> dict | None:
    if df is None or df.empty or action not in ("Long 📈", "Short 📉"):
        return None

    try:
        highs = df["h"].tail(20)
        lows = df["l"].tail(20)
        closes = df["c"].tail(20)

        price = closes.iloc[-1]
        high = highs.max()
        low = lows.min()
        volatility = (high - low) / closes.mean()

        if action == "Long 📈":
            stop = low * 0.996
            target = price * (1.02 if volatility > 0.03 else 1.015)
        else:
            stop = high * 1.004
            target = price * (0.985 if volatility <= 0.02 else 0.98)

        risk = abs(price - stop)
        reward = abs(target - price)
        if risk == 0:
            return None

        result = {
            "current_price": round(price, 4),
            "stop_loss": round(stop, 4),
            "target": round(target, 4),
            "risk": round(risk, 4),
            "reward": round(reward, 4),
            "risk_reward_ratio": round(reward / risk, 2)
        }

        logger.info(f"[RRR] {action} | Price: {price:.2f} | SL: {stop:.2f} | TP: {target:.2f} | RRR: {result['risk_reward_ratio']}")
        return result

    except Exception as e:
        logger.error(f"[RiskEngine RRR Error] {e}")
        return None

# === 3. Minimalistic RRR Calculator ===
def basic_risk_reward(df: pd.DataFrame, action: str) -> dict | None:
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

# === 4. Entry-Based RRR Estimator ===
def estimate_rr_with_entry(df: pd.DataFrame, entry_price: float, direction: str) -> dict:
    if df is None or df.empty or entry_price <= 0 or direction.lower() not in {"long", "short"}:
        return {"risk": None, "reward": None, "rr_ratio": None}

    try:
        high = df["h"].tail(20).max()
        low = df["l"].tail(20).min()

        if pd.isna(high) or pd.isna(low):
            return {"risk": None, "reward": None, "rr_ratio": None}

        if direction.lower() == "long":
            risk = max(entry_price - low, 0)
            reward = max(high - entry_price, 0)
        else:
            risk = max(high - entry_price, 0)
            reward = max(entry_price - low, 0)

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
