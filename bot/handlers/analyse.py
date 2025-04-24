# bot/handlers/analyse.py

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.engine.analysis import run_analysis
from bot.config.settings import get_settings

analyse_handler = CommandHandler("analyse", lambda update, context: analyse(update, context))

async def analyse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    settings = get_settings()
    symbols = settings["AUTO_SIGNAL_SYMBOLS"]

    await update.message.reply_text("🧠 Marktanalyse wird durchgeführt...")

    try:
        summary, ranking, strong_setups = run_analysis(symbols)

        message = "🧠 *A.R.K. Marktanalyse (Live)*\n_Nur klare Chancen – kein Lärm._\n\n"
        message += "\n".join(ranking) + "\n\n"

        if strong_setups:
            message += "\n".join(strong_setups)
        else:
            message += "_Aktuell keine starken Setups – Markt neutral._"

        await update.message.reply_markdown(message)

    except Exception as e:
        await update.message.reply_text("❌ Analyse fehlgeschlagen.")
        print(f"[ERROR] Analyse-Handler: {e}")
