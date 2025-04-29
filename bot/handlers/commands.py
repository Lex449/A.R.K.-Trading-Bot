# bot/handlers/commands.py

"""
A.R.K. Command Handler – Ultra Premium Build.
Handles all user commands with full i18n support and safe error protection.
"""

import logging
import platform
from datetime import datetime, timezone
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.i18n import get_text
from bot.utils.language import get_language
from bot.utils.logger import setup_logger
from bot.utils.error_reporter import report_error
from bot.utils.session_tracker import get_session_report

# Setup Structured Logger
logger = setup_logger(__name__)

# === START Command ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user = update.effective_user.first_name or "Trader"
        lang = get_language(update.effective_chat.id) or "en"

        welcome_message = get_text("start", lang).format(user=user)
        await update.message.reply_text(welcome_message, parse_mode="Markdown")

        logger.info(f"✅ /start by {user} ({update.effective_chat.id})")

    except Exception as e:
        logger.error(f"❌ [StartCommandError] {e}")
        await report_error(context.bot, update.effective_chat.id, e, context_info="/start command failure")

# === HELP Command ===
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        lang = get_language(update.effective_chat.id) or "en"

        help_text = get_text("help", lang)
        await update.message.reply_text(help_text, parse_mode="Markdown")

        logger.info(f"✅ /help used by {update.effective_chat.id}")

    except Exception as e:
        logger.error(f"❌ [HelpCommandError] {e}")
        await report_error(context.bot, update.effective_chat.id, e, context_info="/help command failure")

# === ANALYSE Command ===
async def analyze_symbol_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        lang = get_language(update.effective_chat.id) or "en"

        if not context.args:
            await update.message.reply_text(get_text("analysis_no_symbol", lang), parse_mode="Markdown")
            return

        symbol = context.args[0].upper()

        await update.message.reply_text(
            f"🔍 *Analyzing Symbol:* `{symbol}`...",
            parse_mode="Markdown"
        )

        # Lazy Import
        from bot.engine.analysis_engine import analyze_symbol
        result = await analyze_symbol(symbol)

        if result:
            await update.message.reply_text(get_text("analysis_completed", lang), parse_mode="Markdown")
        else:
            await update.message.reply_text(f"⚠️ No data found for `{symbol}`.", parse_mode="Markdown")

        logger.info(f"✅ /analyse {symbol} requested by {update.effective_chat.id}")

    except Exception as e:
        logger.error(f"❌ [AnalyseCommandError] {e}")
        await report_error(context.bot, update.effective_chat.id, e, context_info="/analyse command failure")

# === SETLANGUAGE Command ===
async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        if not context.args:
            await update.message.reply_text("❌ Please specify a language: /setlanguage en or /setlanguage de")
            return

        lang = context.args[0].lower()

        if lang not in ["en", "de"]:
            await update.message.reply_text("❌ Unsupported language. Use 'en' or 'de'.")
            return

        from bot.utils.language import set_language_for_chat
        set_language_for_chat(update.effective_chat.id, lang)

        await update.message.reply_text(get_text("set_language", lang), parse_mode="Markdown")

        logger.info(f"✅ Language set to {lang} for {update.effective_chat.id}")

    except Exception as e:
        logger.error(f"❌ [SetLanguageCommandError] {e}")
        await report_error(context.bot, update.effective_chat.id, e, context_info="/setlanguage command failure")

# === PING Command ===
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_text("🏓 Pong! System is alive.", parse_mode="Markdown")
        logger.info(f"✅ /ping by {update.effective_chat.id}")

    except Exception as e:
        logger.error(f"❌ [PingCommandError] {e}")
        await report_error(context.bot, update.effective_chat.id, e, context_info="/ping command failure")

# === UPTIME Command ===
async def uptime(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        now = datetime.utcnow().replace(tzinfo=timezone.utc)
        system_uptime = now - datetime.fromtimestamp(psutil.boot_time(), tz=timezone.utc)

        uptime_message = f"🕒 *Uptime:* {system_uptime.days}d {system_uptime.seconds // 3600}h {(system_uptime.seconds % 3600) // 60}m"
        await update.message.reply_text(uptime_message, parse_mode="Markdown")

        logger.info(f"✅ /uptime requested by {update.effective_chat.id}")

    except Exception as e:
        logger.error(f"❌ [UptimeCommandError] {e}")
        await report_error(context.bot, update.effective_chat.id, e, context_info="/uptime command failure")

# === STATUS Command ===
async def status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        session_report = get_session_report(update.effective_chat.id)

        await update.message.reply_text(session_report, parse_mode="Markdown")
        logger.info(f"✅ /status requested by {update.effective_chat.id}")

    except Exception as e:
        logger.error(f"❌ [StatusCommandError] {e}")
        await report_error(context.bot, update.effective_chat.id, e, context_info="/status command failure")

# === SHUTDOWN Command ===
async def shutdown_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        lang = get_language(update.effective_chat.id) or "en"
        shutdown_message = get_text("shutdown", lang)

        await update.message.reply_text(shutdown_message, parse_mode="Markdown")

        logger.warning(f"🛑 /shutdown triggered by {update.effective_chat.id}")
        import os
        os._exit(0)

    except Exception as e:
        logger.error(f"❌ [ShutdownCommandError] {e}")
        await report_error(context.bot, update.effective_chat.id, e, context_info="/shutdown command failure")
