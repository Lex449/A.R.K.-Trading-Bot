# bot/engine/move_engine.py

"""
A.R.K. Move Engine – Ultra Real-Time Move Detection & Emotional Signal Alerts
Jetzt mit Signalstärke, Volatilitätsfaktor, Mentorship-Messaging & Live Impact Formatierung.

Built for: Tactical Breakout Response, Alert Psychology, Zero-Latency Precision.
Made in Bali. Engineered with German Precision.
"""

import pandas as pd
import logging
from telegram import Bot
from datetime import datetime
from bot.utils.logger import setup_logger

logger = setup_logger(__name__)

class MoveEngine:
    def __init__(self, move_threshold_percent: float = 1.0):  # etwas früher triggern
        self.move_threshold_percent = move_threshold_percent

    def detect_move(self, df: pd.DataFrame) -> dict | None:
        """
        Detects strong move based on candle open/close movement.
        """
        if df is None or df.empty or not all(col in df.columns for col in ["o", "c"]):
            logger.warning("[MoveEngine] DataFrame incomplete.")
            return None

        try:
            o = df["o"].iloc[-1]
            c = df["c"].iloc[-1]
            if o <= 0 or c <= 0:
                return None

            move_pct = ((c - o) / o) * 100
            direction = "long" if move_pct > 0 else "short"

            if abs(move_pct) >= self.move_threshold_percent:
                logger.info(f"✅ [MoveEngine] {direction.upper()} move: {move_pct:.2f}%")
                return {
                    "move_percent": round(move_pct, 2),
                    "direction": direction,
                    "timestamp": df.index[-1].strftime("%H:%M UTC")
                }

            return None

        except Exception as e:
            logger.error(f"❌ [MoveEngine Detection Error] {e}")
            return None

    async def send_move_alert(self, bot: Bot, chat_id: int, symbol: str, move_info: dict, volatility_info: dict = None, rrr_info: dict = None) -> None:
        """
        Sends a tactical real-time alert to Telegram with emotion + strategy.
        """
        try:
            move_pct = move_info.get("move_percent", 0.0)
            direction = move_info.get("direction", "long")
            ts = move_info.get("timestamp", datetime.utcnow().strftime("%H:%M UTC"))
            emoji = "📈" if direction == "long" else "📉"

            # Headline classification
            if abs(move_pct) >= 3.5:
                headline = "🧨 *MARKET EXPLOSION*"
                tone = "_This is no drill._"
            elif abs(move_pct) >= 2.5:
                headline = "🚨 *Major Breakout Detected!*"
                tone = "_Momentum is on fire._"
            elif abs(move_pct) >= 1.5:
                headline = "⚠️ *Early Market Acceleration*"
                tone = "_Eyes on chart._"
            elif abs(move_pct) >= 1.0:
                headline = "⚡ *Pulse Move Forming*"
                tone = "_Volatility waking up._"
            else:
                headline = "🔍 *Micro Pulse Detected*"
                tone = "_Low-intensity move... stay ready._"

            # Build message
            message = (
                f"{headline}\n\n"
                f"*Symbol:* `{symbol}`  {emoji}\n"
                f"*Direction:* `{direction.upper()}`\n"
                f"*Movement:* `{move_pct:.2f}%`\n"
                f"*Timestamp:* `{ts}`\n"
            )

            if volatility_info:
                current = volatility_info.get("current_move_percent", 0.0)
                avg = volatility_info.get("average_move_percent", 0.0)
                atr = volatility_info.get("current_atr", 0.0)
                message += (
                    f"\n*Volatility Spike:* `{current:.2f}%` _(Avg: {avg:.2f}%)_\n"
                    f"*ATR (14):* `{atr:.4f}`"
                )

            if rrr_info:
                rrr = rrr_info.get("risk_reward_ratio", None)
                if rrr:
                    message += f"\n*Projected RRR:* `{rrr:.2f}`"

            message += f"\n\n_{tone}_\n_🔔 Trade smart. Not first._"

            await bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode="Markdown",
                disable_web_page_preview=True
            )

            logger.info(f"✅ [MoveAlert] ALERT for {symbol}: {move_pct:.2f}% @ {ts}")

        except Exception as e:
            logger.error(f"❌ [MoveAlert Error] {e}")
