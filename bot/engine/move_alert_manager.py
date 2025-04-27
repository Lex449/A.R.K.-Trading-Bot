"""
A.R.K. Move Alert Manager – Premium Layer für Move- und Volatilitätsmeldungen.
Sorgt für smartes Filtern, keine Überflutung, nur echte Chancen.
"""

import logging
from telegram import Bot
from bot.utils.logger import setup_logger

# Logger
logger = setup_logger(__name__)

async def send_move_alert(bot: Bot, chat_id: int, symbol: str, move_alert: dict, volatility_info: dict = None):
    """
    Sends a detailed, filtered move alert to Telegram based on detected moves and volatility events.

    Args:
        bot (Bot): Telegram bot instance.
        chat_id (int): Target chat ID.
        symbol (str): Trading symbol (e.g., AAPL).
        move_alert (dict): Detected move event (type, move_percent).
        volatility_info (dict or None): Detected volatility spike details.
    """

    try:
        move_type = move_alert["type"]
        move_percent = move_alert["move_percent"]

        # === Build Main Text ===
        if move_type == "full":
            headline = "🚨 *Strong Move Alert!*"
            emoji = "📈" if move_percent > 0 else "📉"
        else:
            headline = "⚠️ *Early Move Detection*"
            emoji = "⚡"

        message = (
            f"{headline}\n\n"
            f"*Symbol:* `{symbol}`\n"
            f"*Move:* `{move_percent:.2f}%` {emoji}\n"
        )

        # === Add Volatility Info if detected ===
        if volatility_info:
            current_move = volatility_info.get("current_move", 0)
            average_move = volatility_info.get("average_move", 0)
            atr_value = volatility_info.get("atr", 0)

            message += (
                f"*Volatility Spike:* `{current_move:.2f}%` (Avg: `{average_move:.2f}%`)\n"
                f"*ATR:* `{atr_value:.2f}`\n"
            )

        # === Motivation Footer ===
        message += "\n_Stay alert. Precision beats noise._"

        # === Send Message ===
        await bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
        logger.info(f"📈 Move alert sent for {symbol}: {move_percent:.2f}%")

    except Exception as e:
        logger.error(f"❌ Error while sending move alert: {e}")
