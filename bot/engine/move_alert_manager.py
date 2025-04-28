"""
A.R.K. Move Alert Manager – Ultra Signal Layer 3.0
Precision Filtering for Movement & Volatility Alerts.

Built for: Signal Excellence, Maximum Trust, Zero Spam.
"""

import logging
from telegram import Bot
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

async def send_move_alert(bot: Bot, chat_id: int, symbol: str, move_alert: dict, volatility_info: dict = None) -> None:
    """
    Sends a high-quality, filtered move alert to Telegram based on live market conditions.

    Args:
        bot (Bot): Telegram bot instance.
        chat_id (int): Target chat ID.
        symbol (str): Trading symbol (e.g., AAPL, TSLA).
        move_alert (dict): Detected movement details {"type": str, "move_percent": float}.
        volatility_info (dict, optional): Detected volatility metrics.
    """

    try:
        move_type = move_alert.get("type", "warning")
        move_percent = move_alert.get("move_percent", 0.0)

        # === Header ===
        if move_type == "full":
            headline = "🚨 *Major Market Move!*"
            emoji = "📈" if move_percent > 0 else "📉"
        else:
            headline = "⚠️ *Early Move Detected*"
            emoji = "⚡"

        # === Base Message ===
        message = (
            f"{headline}\n\n"
            f"*Symbol:* `{symbol}`\n"
            f"*Movement:* `{move_percent:.2f}%` {emoji}\n"
        )

        # === Volatility Context (if available) ===
        if volatility_info:
            current_move = volatility_info.get("current_move_percent", 0.0)
            average_move = volatility_info.get("average_move_percent", 0.0)
            atr_value = volatility_info.get("current_atr", 0.0)

            message += (
                f"*Volatility Spike:* `{current_move:.2f}%` (Avg: `{average_move:.2f}%`)\n"
                f"*ATR (14):* `{atr_value:.2f}`\n"
            )

        # === Motivational Footer ===
        message += "\n_🧠 Speed alone doesn't win. Precision does._"

        # === Send the Final Alert ===
        await bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
        logger.info(f"✅ [Move Alert] Sent for {symbol}: {move_percent:.2f}%")

    except Exception as e:
        logger.error(f"❌ [Move Alert Manager Critical Error] {e}")
