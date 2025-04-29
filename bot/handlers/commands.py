# bot/handlers/commands.py

"""
A.R.K. Commands Handler – NASA Precision Build.
Handles all main bot commands: /start, /help, /analyse, /setlanguage, /signal, /status, /shutdown, /uptime.
"""

import time
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.logger import setup_logger
from bot.utils.error_reporter import report_error

# Setup structured logger
logger = setup_logger(__name__)

# Track bot start time for uptime calculation
start_time = time.time()

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Responds to /start."""
    user = update.effective_user.first_name or "Trader"
    lang = get_language(update.effective_chat.id) or "en"
    welcome_message = get_text("start", lang).format(user=user)

    await update.message.reply_text(welcome_message, parse_mode="Markdown")

    logger.info(f"[Command] /start executed by {user} (Chat ID: {update.effective_chat.id}).")

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Responds to /help."""
    lang = get_language(update.effective_chat.id) or "en"
    help_message = get_text("help", lang)

    await update.message.reply_text(help_message, parse_mode="Markdown")

    logger.info(f"[Command] /help executed for Chat ID: {update.effective_chat.id}.")

async def analyse_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Responds to /analyse [symbol]."""
    lang = get_language(update.effective_chat.id) or "en"

    try:
        if not context.args:
            await update.message.reply_text(get_text("analysis_no_symbol", lang), parse_mode="Markdown")
            return

        symbol = context.args[0].upper()

        await update.message.reply_text(
            f"🔎 Analyzing `{symbol}`...",
            parse_mode="Markdown"
        )

        logger.info(f"[Command] /analyse {symbol} requested by Chat ID: {update.effective_chat.id}.")

        # Import live (damit Bot schneller hochfährt)
        from bot.engine.analysis_engine import analyze_symbol
        from bot.utils.ultra_signal_builder import build_ultra_signal

        result = await analyze_symbol(symbol)

        if not result:
            await update.message.reply_text(f"❌ No analysis data available for `{symbol}`.", parse_mode="Markdown")
            return

        message = build_ultra_signal(
            symbol=symbol,
            move=result.get("move"),
            volume_spike=result.get("volume_spike"),
            atr_breakout=result.get("atr_breakout"),
            risk_reward=result.get("risk_reward"),
            lang=lang
        )

        if message:
            await update.message.reply_text(message, parse_mode="Markdown")
        else:
            await update.message.reply_text(f"❌ No strong patterns detected for `{symbol}`.", parse_mode="Markdown")

    except Exception as e:
        logger.error(f"❌ [Command Error] /analyse failed: {e}")
        await report_error(context.bot, update.effective_chat.id, e, context_info="Analyse Command")

async def set_language_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Responds to /setlanguage [en/de]."""
    try:
        if not context.args:
            await update.message.reply_text("❌ Please specify a language: `/setlanguage en` or `/setlanguage de`", parse_mode="Markdown")
            return

        new_lang = context.args[0].lower()

        if new_lang not in ["en", "de"]:
            await update.message.reply_text("❌ Supported languages: en, de.", parse_mode="Markdown")
            return

        from bot.utils.language import save_language_preference
        save_language_preference(update.effective_chat.id, new_lang)

        await update.message.reply_text(get_text("set_language", new_lang), parse_mode="Markdown")

        logger.info(f"[Command] Language set to {new_lang} for Chat ID: {update.effective_chat.id}.")

    except Exception as e:
        logger.error(f"❌ [Command Error] /setlanguage failed: {e}")
        await report_error(context.bot, update.effective_chat.id, e, context_info="Set Language Command")

async def signal_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Responds to /signal."""
    try:
        from bot.auto.auto_signal_loop import auto_signal_loop
        await update.message.reply_text("🚀 *Auto Signal Monitoring started in background!*", parse_mode="Markdown")
        context.application.create_task(auto_signal_loop())

        logger.info(f"[Command] /signal executed for Chat ID: {update.effective_chat.id}.")

    except Exception as e:
        logger.error(f"❌ [Command Error] /signal failed: {e}")
        await report_error(context.bot, update.effective_chat.id, e, context_info="Signal Command")

async def status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Responds to /status."""
    try:
        from bot.utils.session_tracker import get_session_report
        report = get_session_report(update.effective_chat.id)

        await update.message.reply_text(report, parse_mode="Markdown")

        logger.info(f"[Command] /status requested by Chat ID: {update.effective_chat.id}.")

    except Exception as e:
        logger.error(f"❌ [Command Error] /status failed: {e}")
        await report_error(context.bot, update.effective_chat.id, e, context_info="Status Command")

async def shutdown_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Responds to /shutdown."""
    try:
        await update.message.reply_text(get_text("shutdown"), parse_mode="Markdown")
        logger.warning(f"🛑 Bot shutdown requested by Chat ID: {update.effective_chat.id}.")
        await context.application.stop()

    except Exception as e:
        logger.error(f"❌ [Command Error] /shutdown failed: {e}")
        await report_error(context.bot, update.effective_chat.id, e, context_info="Shutdown Command")

async def uptime_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Responds to /uptime."""
    try:
        uptime_seconds = int(time.time() - start_time)
        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        uptime_message = f"⏱️ *Bot Uptime:* {hours}h {minutes}m {seconds}s"

        await update.message.reply_text(uptime_message, parse_mode="Markdown")

        logger.info(f"[Command] /uptime requested by Chat ID: {update.effective_chat.id}.")

    except Exception as e:
        logger.error(f"❌ [Command Error] /uptime failed: {e}")
        await report_error(context.bot, update.effective_chat.id, e, context_info="Uptime Command")
