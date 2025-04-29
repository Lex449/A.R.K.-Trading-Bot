"""
A.R.K. Core Commands – Unified Command Center
Made in Bali. Engineered with German Precision.
"""

from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.logger import setup_logger
from bot.utils.error_reporter import report_error
from bot.engine.analysis_engine import analyze_symbol

# Setup Logger
logger = setup_logger(__name__)

# === /start Command ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user = update.effective_user.first_name or "Trader"
        lang = get_language(update.effective_chat.id) or "en"
        start_text = get_text("start", lang).format(user=user)

        await update.message.reply_text(start_text, parse_mode="Markdown")
        logger.info(f"✅ [Start] Triggered by {user}")

    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/start Command Error")

# === /help Command ===
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        lang = get_language(update.effective_chat.id) or "en"
        help_text = get_text("help", lang)

        await update.message.reply_text(help_text, parse_mode="Markdown")
        logger.info(f"✅ [Help] Triggered.")

    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/help Command Error")

# === /analyse Command ===
async def analyze_symbol_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        if not context.args:
            lang = get_language(update.effective_chat.id) or "en"
            no_symbol_text = get_text("analysis_no_symbol", lang)
            await update.message.reply_text(no_symbol_text, parse_mode="Markdown")
            return

        symbol = context.args[0].upper()
        lang = get_language(update.effective_chat.id) or "en"

        await update.message.reply_text(f"🔎 Analyzing `{symbol}`...", parse_mode="Markdown")
        result = await analyze_symbol(symbol)

        if not result:
            await update.message.reply_text("❌ No analysis result available.", parse_mode="Markdown")
            return

        patterns = "\n".join(result.get("patterns", []))
        move = result.get("move", "N/A")
        volume_spike = result.get("volume_spike", False)

        text = (
            f"📈 *Analysis for {symbol}*\n\n"
            f"• Movement: `{move}`\n"
            f"• Volume Spike: `{volume_spike}`\n"
            f"• Patterns:\n{patterns or 'None'}"
        )

        await update.message.reply_text(text, parse_mode="Markdown")
        logger.info(f"✅ [Analyse] Analysis sent for {symbol}.")

    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/analyse Command Error")

# === /setlanguage Command ===
async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        if not context.args:
            await update.message.reply_text("❌ Please provide a language code: `/setlanguage en` or `/setlanguage de`", parse_mode="Markdown")
            return

        new_lang = context.args[0].lower()
        if new_lang not in ["en", "de"]:
            await update.message.reply_text("❌ Invalid language. Use `en` or `de`.", parse_mode="Markdown")
            return

        from bot.utils.language import save_language
        save_language(update.effective_chat.id, new_lang)

        success_message = get_text("set_language", new_lang)
        await update.message.reply_text(success_message, parse_mode="Markdown")
        logger.info(f"✅ [SetLanguage] Language set to {new_lang}.")

    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/setlanguage Command Error")

# === /signal Command ===
async def signal_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_text("🚀 Signal engine is operating automatically.", parse_mode="Markdown")
        logger.info(f"✅ [Signal] Triggered manually.")

    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/signal Command Error")

# === /status Command ===
async def status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        from bot.utils.session_tracker import get_session_summary
        lang = get_language(update.effective_chat.id) or "en"

        summary_text = get_session_summary(lang)

        await update.message.reply_text(summary_text, parse_mode="Markdown")
        logger.info(f"✅ [Status] Session summary sent.")

    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/status Command Error")

# === /shutdown Command ===
async def shutdown_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        lang = get_language(update.effective_chat.id) or "en"
        shutdown_text = get_text("shutdown", lang)

        await update.message.reply_text(shutdown_text, parse_mode="Markdown")
        logger.info(f"🛑 [Shutdown] Bot shutdown initiated.")

        await context.application.stop()

    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/shutdown Command Error")

# === /health Command (NEU!!) ===
async def health_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        lang = get_language(update.effective_chat.id) or "en"
        health_message = get_text("health_ok", lang)

        await update.message.reply_text(health_message, parse_mode="Markdown")
        logger.info(f"✅ [HealthCheck] System OK.")

    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/health Command Error")
