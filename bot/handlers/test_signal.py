"""
A.R.K. Testsignal Handler – Premium Showcase für höchste Präzision.
Designed für blitzschnelle, fehlerfreie Tests und Präsentationen.
"""

from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.logger import setup_logger

# Setup Logger
logger = setup_logger(__name__)

async def test_signal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles /testsignal command.
    Sends a premium sample trading signal for quick verification and demonstration.
    """
    try:
        message = (
            "⚡ *A.R.K. Test Trading Signal*\n\n"
            "*Symbol:* `AAPL`\n"
            "*Action:* Ultra Long 📈\n"
            "*Average Confidence:* `74.5%` 🔥\n"
            "*Stars:* ⭐⭐⭐⭐⭐\n\n"
            "✨ *Detected Patterns:*\n"
            "• Bullish Engulfing ⭐⭐⭐⭐⭐ (`65%`)\n"
            "• Piercing Line ⭐⭐⭐⭐ (`60%`)\n"
            "• Dragonfly Doji ⭐⭐⭐ (`54%`)\n\n"
            "🔎 *Risk/Reward Estimate:* `Very Favorable`\n"
            "🧠 _Focus beats speed. Quality beats quantity._\n"
            "🔔 _A.R.K. – Engineered for trading precision._"
        )

        await update.message.reply_text(message, parse_mode="Markdown")

        logger.info("[Test Signal] Sample trading signal successfully sent.")

    except Exception as error:
        logger.error(f"[Test Signal Error] {error}")
