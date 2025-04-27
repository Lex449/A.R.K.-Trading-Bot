"""
A.R.K. Testsignal Handler – Premium Testausgabe für höchste Präzision.
Designed for ultra-fast validation without parsing errors.
"""

from telegram import Update
from telegram.ext import ContextTypes

async def test_signal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles /testsignal command.
    Sends a premium sample trading signal for verification and demonstration.
    """
    try:
        message = (
            "⚡ *A.R.K. Test Trading Signal*\n\n"
            "*Symbol:* `AAPL`\n"
            "*Action:* Ultra Long 📈\n"
            "*Average Confidence:* `74.5%` 🔥\n\n"
            "✨ *Detected Patterns:*\n"
            "• Bullish Engulfing ⭐⭐⭐⭐⭐ (`65%`)\n"
            "• Piercing Line ⭐⭐⭐⭐ (`60%`)\n"
            "• Dragonfly Doji ⭐⭐⭐ (`54%`)\n\n"
            "🧠 _Focus beats speed. Quality beats quantity._\n"
            "🔔 _A.R.K. – Engineered for trading precision._"
        )

        await update.message.reply_text(message, parse_mode="Markdown")

    except Exception as error:
        print(f"[Test Signal Error] {error}")
