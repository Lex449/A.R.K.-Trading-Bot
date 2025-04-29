# bot/handlers/commands.py

"""
A.R.K. Command Handlers – Ultra Premium Trading Bot Commands.
Fully bilingual, modular, lightning-fast responses.
"""

from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.logger import setup_logger
from bot.utils.error_reporter import report_error
from bot.engine.analysis_engine import analyze_symbol
from bot.utils.uptime_tracker import get_uptime

# Setup Structured Logger
logger = setup_logger(__name__)

# === /start Command ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user = update.effective_user.first_name or "Trader"
        lang = get_language(update.effective_chat.id) or "en"
        text = get_text("start", lang).format(user=user)

        await update.message.reply_text(text, parse_mode="Markdown")
        logger.info(f"✅ [Start] Bot started by {user} ({update.effective_chat.id})")

    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/start Handler Error")

# === /help Command ===
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        lang = get_language(update.effective_chat.id) or "en"
        text = get_text("help", lang)

        await update.message.reply_text(text, parse_mode="Markdown")
        logger.info(f"✅ [Help] Help menu sent to {update.effective_chat.id}")

    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/help Handler Error")

# === /analyse Command ===
async def analyze_symbol_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        lang = get_language(update.effective_chat.id) or "en"

        if not context.args:
            await update.message.reply_text(get_text("analysis_no_symbol", lang), parse_mode="Markdown")
            return

        symbol = context.args[0].upper()

        await update.message.reply_text(get_text("fetching_data_primary", lang), parse_mode="Markdown")

        result = await analyze_symbol(symbol)

        if result:
            await update.message.reply_text(get_text("analysis_completed", lang), parse_mode="Markdown")
        else:
            await update.message.reply_text(get_text("error_primary_source", lang), parse_mode="Markdown")

        logger.info(f"✅ [Analyse] Symbol analyzed: {symbol}")

    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/analyse Handler Error")

# === /signal Command ===
async def signal_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_text("⚡ *Real-time signals will appear here soon.*", parse_mode="Markdown")
        logger.info(f"✅ [Signal] Signal request received from {update.effective_chat.id}")

    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/signal Handler Error")

# === /status Command ===
async def status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_text("📊 *Status report generation is under construction.*", parse_mode="Markdown")
        logger.info(f"✅ [Status] Status report requested by {update.effective_chat.id}")

    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/status Handler Error")

# === /uptime Command ===
async def uptime_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        uptime_text = get_uptime()
        await update.message.reply_text(f"⏱️ *Uptime:* `{uptime_text}`", parse_mode="Markdown")
        logger.info(f"✅ [Uptime] Sent uptime info to {update.effective_chat.id}")

    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/uptime Handler Error")

# === /setlanguage Command ===
async def set_language_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        lang = "en"
        if context.args and context.args[0].lower() == "de":
            lang = "de"

        # Store language preference (you should have a user manager that saves this)

        await update.message.reply_text(get_text("set_language", lang), parse_mode="Markdown")
        logger.info(f"✅ [SetLanguage] Language updated for {update.effective_chat.id}: {lang}")

    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/setlanguage Handler Error")

# === /shutdown Command ===
async def shutdown_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_text(get_text("shutdown", get_language(update.effective_chat.id) or "en"), parse_mode="Markdown")
        logger.info(f"🛑 [Shutdown] Shutdown triggered by {update.effective_chat.id}")

        await context.application.stop()

    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/shutdown Handler Error")
