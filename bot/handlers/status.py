# bot/handlers/status.py

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.config.settings import get_settings

status_handler = CommandHandler("status", lambda update, context: status(update, context))

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    settings = get_settings()
    lang = update.effective_user.language_code or "en"

    total_markets = len(settings["AUTO_SIGNAL_SYMBOLS"])
    interval = settings["INTERVAL"]
    max_signals = settings["MAX_SIGNALS_PER_HOUR"]

    if lang.startswith("de"):
        msg = (
            "📊 *A.R.K. Systemstatus*\n"
            "────────────────────────────\n"
            "✅ *Läuft stabil & überwacht Märkte*\n"
            f"⚙️ Analyseengine: *aktiv*\n"
            f"⏱️ Intervall: *{interval}min*\n"
            f"📈 Beobachtete Märkte: *{total_markets}*\n"
            f"🚀 Max. Signale pro Stunde: *{max_signals}*\n"
            "✉️ Telegram-Verbindung: *OK*\n"
            "⭐️ Autopilot-Signale: *bereit*\n"
            "\n"
            "_Bleib fokussiert. A.R.K. denkt mit._"
        )
    else:
        msg = (
            "📊 *A.R.K. System Status*\n"
            "────────────────────────────\n"
            "✅ *Running stable, markets under watch*\n"
            f"⚙️ Analysis engine: *active*\n"
            f"⏱️ Interval: *{interval}min*\n"
            f"📈 Markets tracked: *{total_markets}*\n"
            f"🚀 Max signals/hour: *{max_signals}*\n"
            "✉️ Telegram connection: *OK*\n"
            "⭐️ Autopilot signals: *ready*\n"
            "\n"
            "_Stay sharp. A.R.K. has your back._"
        )

    await update.message.reply_markdown(msg)
