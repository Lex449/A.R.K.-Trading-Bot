# bot/handlers/commands.py

"""
A.R.K. Command Handler – Ultra Premium NASA 2025 Build
Bilingual Commands | Maximum Resilience | Instant Response | Human-grade interaction.
"""

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.logger import setup_logger
from bot.utils.error_reporter import report_error
from bot.engine.analysis_engine import analyze_symbol
from bot.utils.uptime_tracker import get_uptime

# Setup structured logger
logger = setup_logger(__name__)

# === /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user = update.effective_user.first_name or "Trader"
        lang = get_language(update.effective_chat.id) or "en"
        text = get_text("start", lang).format(user=user)

        await update.message.reply_text(text, parse_mode="Markdown")
        logger.info(f"✅ [Command] /start by {user} ({update.effective_chat.id})")

    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/start Handler Error")

# === /help ===
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        lang = get_language(update.effective_chat.id) or "en"
        text = get_text("help", lang)

        await update.message.reply_text(text, parse_mode="Markdown")
        logger.info(f"✅ [Command] /help sent to {update.effective_chat.id}")

    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/help Handler Error")

# === /analyse ===
async def analyze_symbol_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        lang = get_language(update.effective_chat.id) or "en"

        if not context.args:
            await update.message.reply_text(get_text("analysis_no_symbol", lang), parse_mode="Markdown")
            return

        symbol = context.args[0].upper()
        await update.message.reply_text(f"🔍 Analyzing *{symbol}*...", parse_mode="Markdown")

        result = await analyze_symbol(symbol)

        if result:
            move = result.get("move", "Unknown")
            confidence = result.get("confidence", 0)
            stars = result.get("stars", "⭐")

            message = (
                f"📊 *{symbol} Analysis Completed*\n\n"
                f"*Move Detected:* `{move}`\n"
                f"*Confidence:* `{confidence:.1f}%`\n"
                f"*Signal Rating:* {stars}"
            )

            await update.message.reply_text(message, parse_mode="Markdown")
            logger.info(f"✅ [Command] /analyse successful for {symbol}")

        else:
            await update.message.reply_text(f"❌ No valid data found for {symbol}.", parse_mode="Markdown")
            logger.warning(f"⚠️ [Command] /analyse failed for {symbol}")

    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/analyse Handler Error")

# === /signal ===
async def signal_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_text("⚡ *Real-time signals will appear here soon.*", parse_mode="Markdown")
        logger.info(f"✅ [Command] /signal triggered by {update.effective_chat.id}")

    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/signal Handler Error")

# === /status ===
async def status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_text("📊 *Status report generation is under construction.*", parse_mode="Markdown")
        logger.info(f"✅ [Command] /status triggered by {update.effective_chat.id}")

    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/status Handler Error")

# === /uptime ===
async def uptime_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        uptime = get_uptime()
        await update.message.reply_text(f"⏱️ *Uptime:* `{uptime}`", parse_mode="Markdown")
        logger.info(f"✅ [Command] /uptime requested by {update.effective_chat.id}")

    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/uptime Handler Error")

# === /setlanguage ===
async def set_language_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        if not context.args:
            await update.message.reply_text("❗ Please specify a language code: en or de", parse_mode="Markdown")
            return

        lang = context.args[0].lower()
        if lang not in ["en", "de"]:
            await update.message.reply_text("❗ Supported languages: en, de", parse_mode="Markdown")
            return

        from bot.utils.language import set_language
        set_language(update.effective_chat.id, lang)

        await update.message.reply_text(get_text("set_language", lang), parse_mode="Markdown")
        logger.info(f"✅ [Command] /setlanguage to {lang} by {update.effective_chat.id}")

    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/setlanguage Handler Error")

# === /shutdown ===
async def shutdown_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        lang = get_language(update.effective_chat.id) or "en"
        await update.message.reply_text(get_text("shutdown", lang), parse_mode="Markdown")

        logger.info(f"🛑 [Command] /shutdown triggered by {update.effective_chat.id}")
        await context.application.stop()

    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/shutdown Handler Error")
