# bot/handlers/test_signal.py

"""
Test Signal Command – Sends a clean demo signal for verification.
"""

from telegram import Update
from telegram.ext import ContextTypes

async def test_signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Sends a clean, formatted test signal.
    """
    message = (
        "⚡ <b>Test Trading Signal!</b>\n\n"
        "<b>Symbol:</b> AAPL\n"
        "<b>Action:</b> Ultra Long 📈\n"
        "<b>Average Confidence:</b> 74.5%\n"
        "<b>Detected Patterns:</b>\n"
        "• Bullish Engulfing ⭐⭐⭐⭐⭐ (65%)\n"
        "• Piercing Line ⭐⭐⭐⭐ (60%)\n"
        "• Dragonfly Doji ⭐⭐⭐ (54%)\n\n"
        "🧠 <i>Quality over Quantity. Test successful.</i>"
    )

    await update.message.reply_text(
        text=message,
        parse_mode="HTML",
        disable_web_page_preview=True
    )
