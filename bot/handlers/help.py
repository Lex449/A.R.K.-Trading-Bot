# bot/handlers/help.py

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

help_handler = CommandHandler("help", lambda update, context: help_command(update, context))

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = update.effective_user.language_code or "en"

    if lang.startswith("de"):
        msg = (
            "🛠️ *A.R.K. Hilfe & Übersicht*\n"
            "────────────────────────────\n"
            "`/start` – Bot starten & verbinden\n"
            "`/analyse` – Marktscan & Chancenübersicht\n"
            "`/signal` – Manuelles Live-Signal anfordern\n"
            "`/status` – Systemcheck & Status\n"
            "`/recap` – Tagesrückblick (BETA)\n"
            "`/shutdown` – Bot sicher stoppen (nur Admin)\n"
            "\n"
            "_Fragen? Schreib uns: @arktradingteam_"
        )
    else:
        msg = (
            "🛠️ *A.R.K. Help & Overview*\n"
            "────────────────────────────\n"
            "`/start` – Launch the bot & connect\n"
            "`/analyse` – Market scan & top picks\n"
            "`/signal` – Request live signal manually\n"
            "`/status` – System check & uptime\n"
            "`/recap` – Daily recap (BETA)\n"
            "`/shutdown` – Safely stop the bot (admin only)\n"
            "\n"
            "_Need help? DM us: @arktradingteam_"
        )

    await update.message.reply_markdown(msg)
