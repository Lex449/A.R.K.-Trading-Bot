# bot/handlers/commands.py

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
    """Handles the /start command and greets the user."""
    user = update.effective_user.first_name or "Trader"
    lang = get_language(update)

    try:
        greeting = get_text("start", lang).format(user=user)
        help_text = get_text("help", lang)

        await update.message.reply_text(f"{greeting}\n\n{help_text}", parse_mode="Markdown")
        logger.info(f"/start called by {user} ({lang})")

    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/start command")
        logger.error(f"Error in /start: {e}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /help command and provides available commands."""
    user = update.effective_user.first_name or "Trader"
    lang = get_language(update)

    try:
        help_text = get_text("help", lang)

        await update.message.reply_text(help_text, parse_mode="Markdown")
        logger.info(f"/help called by {user}")

    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/help command")
        logger.error(f"Error in /help: {e}")

async def analyze_symbol_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /analyse command for symbol analysis."""
    user = update.effective_user.first_name or "Trader"
    lang = get_language(update)

    if not context.args:
        logger.warning(f"/analyse called by {user} without arguments.")
        await update.message.reply_text(get_text("analysis_no_symbol", lang))
        return

    symbol = context.args[0].upper()

    try:
        result = await analyze_symbol(symbol)

        if not result:
            await update.message.reply_text(f"⚠️ No data available for `{symbol}`.", parse_mode="Markdown")
            logger.info(f"No data for symbol {symbol}")
            return

        message = (
            f"📊 *Symbol Analysis*\n\n"
            f"*Symbol:* `{symbol}`\n"
            f"*Action:* {result['signal']}\n"
            f"*Short-Term Trend:* {result['short_term_trend']}\n"
            f"*Mid-Term Trend:* {result['mid_term_trend']}\n"
            f"*RSI:* {result['rsi']}\n"
            f"*Pattern:* {result['pattern']}\n"
            f"*Candlestick:* {result['candlestick']}\n"
            f"*Rating:* {result['stars']} ⭐\n"
            f"*Suggested Holding:* {result['suggested_holding']}\n\n"
            f"⚡ Stay sharp. No financial advice."
        )

        await update.message.reply_text(message, parse_mode="Markdown")
        logger.info(f"Analysis sent for {symbol} by {user}")

    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/analyse command")
        logger.error(f"Error analyzing {symbol}: {e}")

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /setlanguage command to change user's preferred language."""
    user = update.effective_user.first_name or "Trader"

    if not context.args:
        logger.warning(f"/setlanguage called by {user} without argument.")
        await update.message.reply_text("Please provide a language code (e.g., 'de' or 'en').")
        return

    choice = context.args[0].lower()
    if choice in ("de", "deutsch"):
        lang = "de"
    elif choice in ("en", "english"):
        lang = "en"
    else:
        logger.warning(f"/setlanguage invalid input by {user}: {choice}")
        await update.message.reply_text("Unknown language. Supported options: 'de', 'en'.")
        return

    context.user_data["lang"] = lang
    confirmation = get_text("set_language", lang)

    await update.message.reply_text(confirmation, parse_mode="Markdown")
    logger.info(f"Language set to {lang} by {user}")
