"""
A.R.K. Daily Recap Engine
Sendet motivierenden Tagesrückblick: Beste Signale, Erfolgsquote, Coaching-Motivation.
"""

import logging
from telegram import Bot
from telegram.ext import ContextTypes
from bot.utils.session_tracker import get_session_summary
from bot.config.settings import get_settings
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)
config = get_settings()

# Motivierende Zitate für Tagesabschluss
MOTIVATIONAL_QUOTES = [
    "Progress is invisible at first – then unstoppable.",
    "Small wins every day lead to massive results.",
    "Consistency beats talent when talent doesn't work hard.",
    "Stay focused. Stay resilient. Stay winning.",
    "You don't rise to your goals. You fall to your systems."
]

import random

async def daily_recap_job(context: ContextTypes.DEFAULT_TYPE):
    """
    Sends the daily trading recap in a motivating, coaching tone.
    """
    bot: Bot = context.bot
    chat_id = int(config["TELEGRAM_CHAT_ID"])

    try:
        logger.info("[Daily Recap] Creating daily summary...")

        # Get session data
        summary = get_session_summary()

        total_signals = summary.get("signals_total", 0)
        strong_signals = summary.get("strong_signals", 0)
        success_rate = (strong_signals / total_signals) * 100 if total_signals > 0 else 0

        # Select random motivational quote
        quote = random.choice(MOTIVATIONAL_QUOTES)

        # Build the message
        recap_message = (
            f"✅ *Daily Recap – Strong Finish!*\n\n"
            f"*Total Signals Today:* `{total_signals}`\n"
            f"*Top-Quality Signals (3⭐ and above):* `{strong_signals}`\n"
            f"*Success Rate:* `{success_rate:.1f}%`\n\n"
            f"_{quote}_"
        )

        await bot.send_message(
            chat_id=chat_id,
            text=recap_message,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

        logger.info("[Daily Recap] Successfully sent.")

    except Exception as e:
        logger.error(f"[Daily Recap] Error: {str(e)}")
