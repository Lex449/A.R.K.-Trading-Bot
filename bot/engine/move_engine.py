"""
A.R.K. Move Engine – Real-Time Move Detection & Alert System 2025
Fusion aus Move Detector, Move Alert Engine und Move Manager.

Designed for: Ultra-Fast Breakout Detection, High-Precision Alerts, No Spam.
"""

import pandas as pd
import logging
from telegram import Bot
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

class MoveEngine:
    """
    Consolidated Move Detection, Analysis and Telegram Alert Dispatcher.
    """

    def __init__(self, move_threshold_percent: float = 1.5):
        self.move_threshold_percent = move_threshold_percent

    def detect_move(self, df: pd.DataFrame) -> dict | None:
        """
        Detects strong intraday candle-based moves based on open-close delta.

        Returns:
            dict or None
        """
        if df is None or df.empty or not all(col in df.columns for col in ["o", "c"]):
            return None

        try:
            latest_open = df["o"].iloc[-1]
            latest_close = df["c"].iloc[-1]

            if latest_open == 0:
                return None  # Avoid division by zero

            move_percent = ((latest_close - latest_open) / latest_open) * 100

            if abs(move_percent) >= self.move_threshold_percent:
                direction = "long" if move_percent > 0 else "short"
                logger.info(f"✅ [MoveDetector] {direction.upper()} move detected: {move_percent:.2f}%")
                return {
                    "move_percent": round(move_percent, 2),
                    "direction": direction
                }

            return None

        except Exception as e:
            logger.error(f"❌ [MoveDetector Critical Error] {e}")
            return None

    async def send_move_alert(self, bot: Bot, chat_id: int, symbol: str, move_info: dict, volatility_info: dict = None) -> None:
        """
        Sends a real-time alert to Telegram if a significant move is detected.
        """

        try:
            move_percent = move_info.get("move_percent", 0.0)
            direction = move_info.get("direction", "long")

            # Determine message header
            if abs(move_percent) >= 2.5:
                headline = "🚨 *Major Market Move!*"
                emoji = "📈" if direction == "long" else "📉"
            else:
                headline = "⚡ *Early Move Detected*"
                emoji = "⚡"

            # Base message
            message = (
                f"{headline}\n\n"
                f"*Symbol:* `{symbol}`\n"
                f"*Movement:* `{move_percent:.2f}%` {emoji}\n"
            )

            # Volatility context
            if volatility_info:
                current_move = volatility_info.get("current_move_percent", 0.0)
                average_move = volatility_info.get("average_move_percent", 0.0)
                atr_value = volatility_info.get("current_atr", 0.0)

                message += (
                    f"*Volatility Spike:* `{current_move:.2f}%` (Avg: `{average_move:.2f}%`)\n"
                    f"*ATR (14):* `{atr_value:.2f}`\n"
                )

            # Motivational Footer
            message += "\n_🧠 Precision beats speed._"

            await bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode="Markdown",
                disable_web_page_preview=True
            )

            logger.info(f"✅ [MoveAlert] Sent move alert for {symbol}: {move_percent:.2f}%")

        except Exception as e:
            logger.error(f"❌ [MoveAlert Critical Error] {e}")
