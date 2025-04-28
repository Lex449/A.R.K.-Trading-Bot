"""
A.R.K. Move Alert Manager – Premium Signal Layer für Bewegungs- und Volatilitätsmeldungen.
Maximale Signalqualität – null Spam, nur echte Trading-Chancen.
"""

import logging
from telegram import Bot
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

async def send_move_alert(bot: Bot, chat_id: int, symbol: str, move_alert: dict, volatility_info: dict = None):
    """
    Sends a filtered and detailed move alert to Telegram based on detected movement and volatility.

    Args:
        bot (Bot): Telegram bot instance.
        chat_id (int): Target chat ID.
        symbol (str): Trading symbol (e.g., AAPL).
        move_alert (dict): Move detection result (type: "full" or "warning", move_percent).
        volatility_info (dict or None): Volatility spike data (optional).
    """

    try:
        move_type = move_alert.get("type", "warning")
        move_percent = move_alert.get("move_percent", 0.0)

        # === Build Header based on Move Type ===
        if move_type == "full":
            headline = "🚨 *Strong Move Detected!*"
            emoji = "📈" if move_percent > 0 else "📉"
        else:
            headline = "⚠️ *Early Move Warning*"
            emoji = "⚡"

        # === Build Message ===
        message = (
            f"{headline}\n\n"
            f"*Symbol:* `{symbol}`\n"
            f"*Move:* `{move_percent:.2f}%` {emoji}\n"
        )

        # === Optional Volatility Spike Info ===
        if volatility_info:
            current_move = volatility_info.get("current_move_percent", 0.0)
            average_move = volatility_info.get("average_move_percent", 0.0)
            atr_value = volatility_info.get("current_atr", 0.0)

            message += (
                f"*Volatility Spike:* `{current_move:.2f}%` (Avg: `{average_move:.2f}%`)\n"
                f"*ATR (14):* `{atr_value:.2f}`\n"
            )

        # === Motivational Footer ===
        message += "\n_Stay sharp. Great moves don't wait._"

        # === Send Message ===
        await bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
        logger.info(f"✅ Move alert sent for {symbol}: {move_percent:.2f}%")

    except Exception as e:
        logger.error(f"❌ [Move Alert Manager] Error while sending move alert: {e}")
