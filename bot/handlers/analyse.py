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

    await update.message.reply_text("🧠 Analyse der Märkte läuft...")

    for symbol in symbols:
        result = analyze_market(symbol)
        if not result:
            report.append(f"*{symbol}*: ⚠️ *Keine verwertbaren Daten.*")
            continue

        confidence = result["confidence"]
        stars = "⭐️" * min(int(confidence // 20), 5) + "✩" * (5 - min(int(confidence // 20), 5))

        block = (
            f"*{symbol}*\n"
            f"> *Trend:* `{result['trend']}` | *Pattern:* `{result['pattern']}`\n"
            f"> *RSI:* `{result['rsi']:.2f}` | *Qualität:* {stars}\n"
            f"> *Stärke:* `{confidence:.2f}%`\n"
        )
        report.append(block)

    if not report:
        report.append("_Keine starken Setups erkannt – Märkte derzeit neutral._")

    final = "📊 *A.R.K. Analyseübersicht*\n\n" + "\n\n".join(report)
    await update.message.reply_markdown(final)
