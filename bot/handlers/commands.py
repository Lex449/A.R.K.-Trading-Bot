# bot/handlers/commands.py

"""
A.R.K. Command Handlers – Ultra Stable, Ultra Expandable.
Made in Bali. Engineered with German Precision.
"""

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.engine.analysis_engine import analyze_symbol
from bot.utils.logger import setup_logger
from bot.utils.error_reporter import report_error

logger = setup_logger(__name__)

# === Core Command Functions ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the bot and send welcome message."""
    try:
        lang = get_language(update.effective_chat.id) or "en"
        await update.message.reply_text(get_text("start", lang), parse_mode="Markdown")
        logger.info(f"[Start] Sent welcome message to {update.effective_chat.id}")
    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/start Command Error")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send list of available commands."""
    try:
        lang = get_language(update.effective_chat.id) or "en"
        await update.message.reply_text(get_text("help", lang), parse_mode="Markdown")
        logger.info(f"[Help] Help requested by {update.effective_chat.id}")
    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/help Command Error")

async def analyze_symbol_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Analyse a given symbol."""
    try:
        if not context.args:
            lang = get_language(update.effective_chat.id) or "en"
            await update.message.reply_text(get_text("analysis_no_symbol", lang), parse_mode="Markdown")
            return

        symbol = context.args[0].upper()

        lang = get_language(update.effective_chat.id) or "en"
        await update.message.reply_text(f"🔍 {get_text('fetching_data_primary', lang)} `{symbol}`...", parse_mode="Markdown")

        result = await analyze_symbol(symbol)

        if result:
            await update.message.reply_text(f"✅ {get_text('analysis_completed', lang)}", parse_mode="Markdown")
        else:
            await update.message.reply_text(f"❌ {get_text('error_primary_source', lang)}", parse_mode="Markdown")

    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/analyse Command Error")

async def signal_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send live trading signals (future expansion)."""
    try:
        await update.message.reply_text("🚀 [Signal] Feature coming soon!", parse_mode="Markdown")
        logger.info(f"[Signal] Signal requested by {update.effective_chat.id}")
    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/signal Command Error")

async def status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send current session status (future expansion)."""
    try:
        await update.message.reply_text("📊 [Status] Feature coming soon!", parse_mode="Markdown")
        logger.info(f"[Status] Status requested by {update.effective_chat.id}")
    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/status Command Error")

async def uptime_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send bot uptime."""
    try:
        await update.message.reply_text("⏳ [Uptime] Feature coming soon!", parse_mode="Markdown")
        logger.info(f"[Uptime] Uptime requested by {update.effective_chat.id}")
    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/uptime Command Error")

async def set_language_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Change language settings."""
    try:
        await update.message.reply_text("🌍 [Set Language] Feature coming soon!", parse_mode="Markdown")
        logger.info(f"[Language] Language setting requested by {update.effective_chat.id}")
    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/setlanguage Command Error")

async def shutdown_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Shutdown the bot safely."""
    try:
        await update.message.reply_text("🛑 Bot is shutting down. See you soon!", parse_mode="Markdown")
        await context.bot.shutdown()
        logger.info(f"[Shutdown] Shutdown initiated by {update.effective_chat.id}")
    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/shutdown Command Error")

# === Command Handler Collection ===

command_handlers = [
    CommandHandler("start", start),
    CommandHandler("help", help_command),
    CommandHandler("analyse", analyze_symbol_handler),
    CommandHandler("signal", signal_handler),
    CommandHandler("status", status_handler),
    CommandHandler("uptime", uptime_handler),
    CommandHandler("setlanguage", set_language_handler),
    CommandHandler("shutdown", shutdown_handler),
]
