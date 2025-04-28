"""
A.R.K. Command Handlers – Ultra Strategic, Elegant, Ultra Reliable.
Handles /start, /help, /analyse, /setlanguage with maximum UX perfection.
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.engine.analysis_engine import analyze_symbol
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.config.settings import get_settings
from bot.utils.logger import setup_logger
from bot.utils.error_reporter import report_error

# Setup structured logger
logger = setup_logger(__name__)

# Load configuration
config = get_settings()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /start command."""
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"
    lang = get_language(chat_id) or "en"

    try:
        greeting = get_text("start", lang).format(user=user)
        help_hint = get_text("start_help_hint", lang)

        await update.message.reply_text(
            f"{greeting}\n\n{help_hint}",
            parse_mode="Markdown"
        )
        logger.info(f"[Start] Triggered by {user} (Chat ID: {chat_id}).")

    except Exception as e:
        await report_error(context.bot, chat_id, e, context_info="Start Command Error")
        logger.error(f"[Start] Fatal Error: {e}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /help command."""
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"
    lang = get_language(chat_id) or "en"

    try:
        help_text = get_text("help", lang)

        await update.message.reply_text(
            help_text,
            parse_mode="Markdown"
        )
        logger.info(f"[Help] Triggered by {user} (Chat ID: {chat_id}).")

    except Exception as e:
        await report_error(context.bot, chat_id, e, context_info="Help Command Error")
        logger.error(f"[Help] Fatal Error: {e}")

async def analyze_symbol_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /analyse [symbol] command."""
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"
    lang = get_language(chat_id) or "en"

    try:
        if not context.args:
            await update.message.reply_text(
                get_text("analysis_no_symbol", lang),
                parse_mode="Markdown"
            )
            logger.warning(f"[Analyse] No symbol provided by {user}.")
            return

        symbol = context.args[0].upper()
        result = await analyze_symbol(symbol, chat_id)

        if not result:
            await update.message.reply_text(
                f"⚠️ *No data available for* `{symbol}`.",
                parse_mode="Markdown"
            )
            logger.info(f"[Analyse] No data found for {symbol}.")
            return

        message = (
            f"📊 *A.R.K. Symbol Analysis*\n\n"
            f"*Symbol:* `{symbol}`\n"
            f"*Signal:* {result.get('combined_action', '-')}\n"
            f"*Confidence:* `{result.get('avg_confidence', 0):.1f}%`\n"
            f"*Patterns Detected:* `{len(result.get('patterns', []))}`\n"
            f"*Risk/Reward:* `{result.get('risk_reward_info', {}).get('risk_reward_ratio', '-')}`\n"
            f"*Volatility (Move %):* `{result.get('volatility_info', {}).get('current_move_percent', '-')}`\n\n"
            f"_🎯 Precision builds consistency. Consistency builds freedom._"
        )

        await update.message.reply_text(
            message,
            parse_mode="Markdown"
        )
        logger.info(f"[Analyse] Analysis sent for {symbol} (User: {user}).")

    except Exception as e:
        await report_error(context.bot, chat_id, e, context_info="Analyse Command Error")
        logger.error(f"[Analyse] Critical Error analyzing {symbol}: {e}")

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /setlanguage command."""
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"

    try:
        if not context.args:
            await update.message.reply_text(
                "❗ *Please specify a language code:* `en` or `de`.",
                parse_mode="Markdown"
            )
            logger.warning(f"[SetLanguage] No language specified by {user}.")
            return

        choice = context.args[0].lower()

        if choice in ("de", "deutsch"):
            lang = "de"
        elif choice in ("en", "english"):
            lang = "en"
        else:
            await update.message.reply_text(
                "❗ *Unsupported language.* Available: `en`, `de`.",
                parse_mode="Markdown"
            )
            logger.warning(f"[SetLanguage] Unsupported choice by {user}: {choice}.")
            return

        context.user_data["lang"] = lang
        confirmation = get_text("set_language", lang)

        await update.message.reply_text(
            confirmation,
            parse_mode="Markdown"
        )
        logger.info(f"[SetLanguage] Language set to {lang} for {user}.")

    except Exception as e:
        await report_error(context.bot, chat_id, e, context_info="SetLanguage Command Error")
        logger.error(f"[SetLanguage] Fatal Error: {e}")
