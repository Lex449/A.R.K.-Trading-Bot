# bot/handlers/help.py

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.config.settings import get_settings

settings = get_settings()
ADMIN_ID = int(settings["TELEGRAM_CHAT_ID"])

help_handler = CommandHandler("help", lambda update, context: help_command(update, context))

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = update.effective_user.language_code or "en"
    is_admin = update.effective_user.id == ADMIN_ID

    if lang.startswith("de"):
        msg = (
            "🧭 *A.R.K. Hilfe & Kommandos*\n"
            "────────────────────────────\n"
            "`/start` – Bot starten & verbinden\n"
            "`/analyse` – Marktscan & Chancenübersicht\n"
            "`/signal` – Manuelles Live-Signal anfordern\n"
            "`/status` – Systemcheck & Marktstatus\n"
            "`/recap` – Tagesrückblick (BETA)"
        )
        if is_admin:
            msg += "\n`/shutdown` – Bot sicher stoppen (nur Admin)"
        msg += "\n\n_Fragen? Schreib uns: @arktradingteam_"

    else:
        msg = (
            "🧭 *A.R.K. Commands & Help*\n"
            "────────────────────────────\n"
            "`/start` – Launch the bot & connect\n"
            "`/analyse` – Market scan & trade potential\n"
            "`/signal` – Request a manual live signal\n"
            "`/status` – System check & signal engine\n"
            "`/recap` – Daily summary (BETA)"
        )
        if is_admin:
            msg += "\n`/shutdown` – Safely stop the bot (admin only)"
        msg += "\n\n_Questions? Contact: @arktradingteam_"

    await update.message.reply_markdown(msg)
