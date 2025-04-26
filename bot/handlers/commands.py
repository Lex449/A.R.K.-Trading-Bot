import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.config.settings import get_settings
from bot.engine.analysis_engine import analyze_symbol
from bot.utils.session_tracker import get_session_report

# Setup Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Load configuration
config = get_settings()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Starts the bot and greets the user.
    """
    user = update.effective_user.first_name or "Trader"
    lang = get_language(update)
    greeting = get_text("start", lang).format(user=user)
    help_text = get_text("help", lang)

    logger.info(f"Start command by {user} ({lang})")
    await update.message.reply_text(f"{greeting}\n\n{help_text}", parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Returns an overview of available commands.
    """
    lang = get_language(update)
    help_text = get_text("help", lang)

    logger.info(f"Help command requested by {update.effective_user.first_name}")
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def analyse_symbol_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Analyzes a given financial symbol and returns structured results.
    """
    lang = get_language(update)

    if not context.args:
        logger.warning(f"No symbol provided in /analyse by {update.effective_user.first_name}")
        await update.message.reply_text(get_text("analysis_no_symbol", lang), parse_mode="Markdown")
        return

    symbol = context.args[0].upper()

    try:
        result = await analyze_symbol(symbol)

        if not result:
            await update.message.reply_text(f"⚠️ No data available for {symbol}.", parse_mode="Markdown")
            return

        message = (
            f"📊 *Single Symbol Analysis*\n\n"
            f"*Symbol:* `{symbol}`\n"
            f"*Action:* {result['signal']}\n"
            f"*Short-Term Trend:* {result['short_term_trend']}\n"
            f"*Mid-Term Trend:* {result['mid_term_trend']}\n"
            f"*RSI:* {result['rsi']}\n"
            f"*Pattern Detected:* {result['pattern']}\n"
            f"*Candlestick Formation:* {result['candlestick']}\n"
            f"*Quality Rating:* {result['stars']} ⭐\n"
            f"*Suggested Holding:* {result['suggested_holding']}\n\n"
            f"⚡ _Always manage your risk carefully. No financial advice._"
        )

        await update.message.reply_text(message, parse_mode="Markdown")
        logger.info(f"Analysis sent for {symbol} by {update.effective_user.first_name}")

    except Exception as e:
        logger.error(f"Analysis error for {symbol}: {e}")
        await update.message.reply_text(f"❌ Error analyzing {symbol}. Try again later.", parse_mode="Markdown")

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Sets the user's preferred language.
    """
    if not context.args:
        await update.message.reply_text("Please provide a language code (e.g., 'de' or 'en').", parse_mode="Markdown")
        return

    choice = context.args[0].lower()
    if choice in ("de", "deutsch"):
        lang = "de"
    elif choice in ("en", "english"):
        lang = "en"
    else:
        await update.message.reply_text("Unknown language. Supported: 'de', 'en'.", parse_mode="Markdown")
        return

    context.user_data["lang"] = lang
    confirmation = get_text("set_language", lang)

    logger.info(f"Language switched to {lang} by {update.effective_user.first_name}")
    await update.message.reply_text(confirmation, parse_mode="Markdown")

async def session_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Returns the current session trading statistics.
    """
    summary = get_session_summary()
    await update.message.reply_text(summary, parse_mode="Markdown")
