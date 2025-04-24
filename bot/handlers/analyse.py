# bot/handlers/analyse.py

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.engine.analysis_engine import analyze_market
from bot.config.settings import get_settings

analyse_handler = CommandHandler("analyse", lambda update, context: analyse(update, context))

async def analyse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    settings = get_settings()
    symbols = settings["AUTO_SIGNAL_SYMBOLS"]
    report = []

    await update.message.reply_text("🧠 Analyse läuft...")

    for symbol in symbols:
        result = analyze_market(symbol)
        if not result:
            continue

        stars = "⭐️" * result["confidence"] + "✩" * (5 - result["confidence"])
        block = (
            f"*{symbol}*\n"
            f"> *Signal:* {result['signal']}\n"
            f"> *Trend:* {result['trend']} | *Muster:* {result['pattern']}\n"
            f"> *RSI:* {result['rsi']:.2f}\n"
            f"> *Qualität:* {stars}\n"
        )
        report.append(block)

    if not report:
        report.append("_Keine starken Setups – Markt neutral._")

    final = "📊 *A.R.K. Analyseübersicht*\n\n" + "\n\n".join(report)
    await update.message.reply_markdown(final)
