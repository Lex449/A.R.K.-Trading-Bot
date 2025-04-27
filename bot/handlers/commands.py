"""
A.R.K. Core Command Handlers – Strategic, Elegant, Ultra Reliable.
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
    """Handles the /start command with a warm, professional welcome."""
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
        logger.info(f"[Start] Triggered by {user} (Chat ID: {chat_id})")

    except Exception as e:
        await report_error(context.bot, chat_id, e, context_info="Start Command")
        logger.error(f"[Start] Error: {e}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /help command and displays clean guidance."""
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"
    lang = get_language(chat_id) or "en"

    try:
        help_text = get_text("help", lang)

        await update.message.reply_text(help_text, parse_mode="Markdown")
        logger.info(f"[Help] Triggered by {user} (Chat ID: {chat_id})")

    except Exception as e:
        await report_error(context.bot, chat_id, e, context_info="Help Command")
        logger.error(f"[Help] Error: {e}")

async def analyze_symbol_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /analyse command to deliver strategic insights."""
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"
    lang = get_language(chat_id) or "en"

    try:
        if not context.args:
            await update.message.reply_text(
                get_text("analysis_no_symbol", lang),
                parse_mode="Markdown"
            )
            logger.warning(f"[Analyse] No symbol provided by {user}")
            return

        symbol = context.args[0].upper()
        result = await analyze_symbol(symbol)

        if not result:
            await update.message.reply_text(
                f"⚠️ *No data available for* `{symbol}`.",
                parse_mode="Markdown"
            )
            logger.info(f"[Analyse] No data for {symbol}")
            return

        message = (
            f"📊 *A.R.K. Symbol Analysis*\n\n"
            f"*Symbol:* `{symbol}`\n"
            f"*Signal:* {result.get('combined_action', '-')}\n"
            f"*Short-Term Trend:* {result.get('short_term_trend', '-')}\n"
            f"*Mid-Term Trend:* {result.get('mid_term_trend', '-')}\n"
            f"*RSI (14):* `{result.get('rsi', '-')}%`\n"
            f"*Pattern:* {result.get('pattern', '-')}\n"
            f"*Candle Formation:* {result.get('candlestick', '-')}\n"
            f"*Rating:* {'⭐' * result.get('stars', 0)}\n"
            f"*Suggested Holding:* {result.get('suggested_holding', '-')}\n\n"
            f"_🧠 Stay strategic. Trade smart._"
        )

        await update.message.reply_text(message, parse_mode="Markdown")
        logger.info(f"[Analyse] Sent analysis for {symbol} to {user}")

    except Exception as e:
        await report_error(context.bot, chat_id, e, context_info="Analyse Command")
        logger.error(f"[Analyse] Error analyzing {symbol}: {e}")

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /setlanguage command to customize user experience."""
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"

    try:
        if not context.args:
            await update.message.reply_text(
                "❗ Please provide a language code: `en` or `de`.",
                parse_mode="Markdown"
            )
            logger.warning(f"[SetLanguage] No language provided by {user}")
            return

        choice = context.args[0].lower()
        if choice in ("de", "deutsch"):
            lang = "de"
        elif choice in ("en", "english"):
            lang = "en"
        else:
            await update.message.reply_text(
                "❗ Unknown language. Supported: `en`, `de`.",
                parse_mode="Markdown"
            )
            logger.warning(f"[SetLanguage] Invalid language by {user}: {choice}")
            return

        context.user_data["lang"] = lang
        confirmation = get_text("set_language", lang)

        await update.message.reply_text(confirmation, parse_mode="Markdown")
        logger.info(f"[SetLanguage] Language set to {lang} by {user}")

    except Exception as e:
        await report_error(context.bot, chat_id, e, context_info="SetLanguage Command")
        logger.error(f"[SetLanguage] Error: {e}")
