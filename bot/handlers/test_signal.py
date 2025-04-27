# bot/handlers/test_signal.py

"""
Testbefehl für A.R.K. Bot.
Sendet ein manuelles Test-Trading-Signal (Stock-basiert).
"""

from telegram import Update
from telegram.ext import ContextTypes

async def test_signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    test_message = (
        "⚡ *Test Trading Signal\\!*\\n\\n"
        "*Symbol:* `AAPL`\\n"
        "*Aktion:* Ultra Long 📈\\n"
        "*Durchschnittliche Confidence:* `74\\.5\\%`\\n"
        "*Muster erkannt:*\\n"
        "• Bullish Engulfing ⭐⭐⭐⭐ \\(65\\%\\)\\n"
        "• Piercing Line ⭐⭐⭐⭐ \\(60\\%\\)\\n"
        "• Dragonfly Doji ⭐⭐⭐ \\(54\\%\\)\\n\\n"
        "🧠 _Qualität vor Quantität\\. Test erfolgreich\\._"
    )

    await update.message.reply_text(test_message, parse_mode="MarkdownV2")
