"""
A.R.K. Testsignal Handler – Perfekte Testausgabe ohne Parsing-Fehler.
"""

from telegram import Update
from telegram.ext import ContextTypes

async def test_signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "⚡ *Test Trading Signal!*\n\n"
        "*Symbol:* `AAPL`\n"
        "*Aktion:* Ultra Long 📈\n"
        "*Durchschnittliche Confidence:* `74.5%`\n\n"
        "✨ *Erkannte Muster:*\n"
        "• Bullish Engulfing ⭐⭐⭐⭐⭐ (65%)\n"
        "• Piercing Line ⭐⭐⭐⭐ (60%)\n"
        "• Dragonfly Doji ⭐⭐⭐ (54%)\n\n"
        "_🧠 Qualität vor Quantität. Test erfolgreich._"
    )

    await update.message.reply_text(message, parse_mode="Markdown")
