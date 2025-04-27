# bot/handlers/test_analyse.py

"""
Test Analyse Command – Sends a demo analysis report.
"""

from telegram import Update
from telegram.ext import ContextTypes

async def test_analyse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Sends a clean, formatted test analysis message.
    """
    message = (
        "📊 <b>Test Analysis Report</b>\n\n"
        "<b>Symbol:</b> AAPL\n"
        "<b>Action:</b> Ultra Long 📈\n"
        "<b>Trend Direction:</b> Strong Long 📈\n"
        "<b>RSI (14):</b> 68.4\n"
        "<b>EMA(9)/EMA(21):</b> 52.8 / 50.1\n"
        "<b>Pattern Detection:</b>\n"
        "• Bullish Engulfing ⭐⭐⭐⭐⭐\n"
        "• Hammer ⭐⭐⭐⭐\n\n"
        "<i>Analysis complete. Stay sharp and disciplined.</i>"
    )

    await update.message.reply_text(
        text=message,
        parse_mode="HTML",
        disable_web_page_preview=True
    )
