# bot/handlers/commands.py

"""
A.R.K. Command Handler – Ultra Diamond Stability 2025
Handles all main Telegram commands with full i18n support.
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.i18n import get_text
from bot.utils.language import get_language
from bot.utils.error_reporter import report_error
from bot.utils.logger import setup_logger

# Logger Setup
logger = setup_logger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles /start command."""
    chat_id = update.effective_chat.id
    user_name = update.effective_user.first_name or "Trader"
    lang = get_language(chat_id) or "en"

    try:
        message = get_text("start", lang).format(user=user_name)
        await update.message.reply_text(message, parse_mode="Markdown")
        logger.info(f"✅ /start by {user_name}")

    except Exception as e:
        logger.error(f"❌ [Start] Error: {e}")
        await report_error(context.bot, chat_id, e, context_info="/start command")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles /help command."""
    chat_id = update.effective_chat.id
    lang = get_language(chat_id) or "en"

    try:
        message = get_text("help", lang)
        await update.message.reply_text(message, parse_mode="Markdown")
        logger.info(f"✅ /help executed for chat_id {chat_id}")

    except Exception as e:
        logger.error(f"❌ [Help] Error: {e}")
        await report_error(context.bot, chat_id, e, context_info="/help command")

async def analyse_symbol_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles /analyse [symbol] command."""
    chat_id = update.effective_chat.id
    lang = get_language(chat_id) or "en"

    try:
        if not context.args:
            await update.message.reply_text(get_text("analysis_no_symbol", lang), parse_mode="Markdown")
            return

        symbol = context.args[0].upper()
        await update.message.reply_text(f"🔍 Analyzing `{symbol}`...", parse_mode="Markdown")

        from bot.engine.analysis_engine import analyze_symbol
        result = await analyze_symbol(symbol)

        if result:
            await update.message.reply_text("✅ *Analysis completed!*", parse_mode="Markdown")
        else:
            await update.message.reply_text("⚠️ No valid data for this symbol.", parse_mode="Markdown")

        logger.info(f"✅ /analyse {symbol} completed for chat_id {chat_id}")

    except Exception as e:
        logger.error(f"❌ [Analyse] Error: {e}")
        await report_error(context.bot, chat_id, e, context_info="/analyse command")

async def signal_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles /signal command."""
    chat_id = update.effective_chat.id

    try:
        from bot.auto.auto_signal_loop import auto_signal_loop
        await update.message.reply_text("🚀 *Auto Signal Loop manually triggered.*", parse_mode="Markdown")
        context.application.create_task(auto_signal_loop())
        logger.info(f"✅ /signal manually triggered by {chat_id}")

    except Exception as e:
        logger.error(f"❌ [Signal] Error: {e}")
        await report_error(context.bot, chat_id, e, context_info="/signal command")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles /ping command."""
    chat_id = update.effective_chat.id

    try:
        await update.message.reply_text("🏓 Pong! Bot is alive.")
        logger.info(f"✅ /ping responded for chat_id {chat_id}")

    except Exception as e:
        logger.error(f"❌ [Ping] Error: {e}")
        await report_error(context.bot, chat_id, e, context_info="/ping command")

async def status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles /status command."""
    chat_id = update.effective_chat.id

    try:
        from bot.utils.session_tracker import get_session_report
        report = get_session_report(chat_id)
        await update.message.reply_text(report, parse_mode="Markdown")
        logger.info(f"✅ /status report sent for chat_id {chat_id}")

    except Exception as e:
        logger.error(f"❌ [Status] Error: {e}")
        await report_error(context.bot, chat_id, e, context_info="/status command")

async def uptime(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles /uptime command."""
    chat_id = update.effective_chat.id

    try:
        from bot.utils.session_tracker import get_today_report
        report = get_today_report(chat_id)
        await update.message.reply_text(report, parse_mode="Markdown")
        logger.info(f"✅ /uptime report sent for chat_id {chat_id}")

    except Exception as e:
        logger.error(f"❌ [Uptime] Error: {e}")
        await report_error(context.bot, chat_id, e, context_info="/uptime command")

async def shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles /shutdown command."""
    chat_id = update.effective_chat.id
    lang = get_language(chat_id) or "en"

    try:
        shutdown_message = get_text("shutdown", lang)
        await update.message.reply_text(shutdown_message, parse_mode="Markdown")
        logger.info(f"✅ /shutdown initiated by chat_id {chat_id}")

        import os
        os._exit(0)

    except Exception as e:
        logger.error(f"❌ [Shutdown] Error: {e}")
        await report_error(context.bot, chat_id, e, context_info="/shutdown command")

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles /setlanguage [en/de] command."""
    chat_id = update.effective_chat.id

    try:
        if not context.args:
            await update.message.reply_text("❌ Please specify a language: /setlanguage en or de")
            return

        lang_choice = context.args[0].lower()
        if lang_choice not in ["en", "de"]:
            await update.message.reply_text("❌ Invalid language. Choose 'en' or 'de'.")
            return

        from bot.utils.language import update_language
        update_language(chat_id, lang_choice)

        confirmation = get_text("set_language", lang_choice)
        await update.message.reply_text(confirmation, parse_mode="Markdown")
        logger.info(f"✅ Language changed to {lang_choice} for chat_id {chat_id}")

    except Exception as e:
        logger.error(f"❌ [SetLanguage] Error: {e}")
        await report_error(context.bot, chat_id, e, context_info="/setlanguage command")
