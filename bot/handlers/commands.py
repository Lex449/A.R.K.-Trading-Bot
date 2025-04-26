# bot/handlers/commands.py

from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.language import get_language
from bot.engine.analysis_engine import analyze_symbol
from bot.utils.i18n import get_text
from bot.config.settings import get_settings
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# Load configuration
config = get_settings()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Starts the bot and greets the user."""
    user = update.effective_user.first_name or "Trader"
    lang = get_language(update)
    greeting = get_text("start", lang).format(user=user)
    help_text = get_text("help", lang)

    logger.info(f"/start command triggered by {user} (Language: {lang})")
    await update.message.reply_text(f"{greeting}\n\n{help_text}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Returns an overview of available commands."""
    user = update.effective_user.first_name or "Trader"
    lang = get_language(update)

    logger.info(f"/help command triggered by {user}")
    help_text = get_text("help", lang)
    await update.message.reply_text(help_text)

async def analyze_symbol_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Analyzes a given financial symbol and returns the results."""
    user = update.effective_user.first_name or "Trader"
    lang = get_language(update)

    if not context.args:
        logger.warning(f"/analyse triggered by {user} without symbol argument.")
        await update.message.reply_text(get_text("analysis_no_symbol", lang))
        return

    symbol = context.args[0].upper()

    try:
        result = await analyze_symbol(symbol)

        if not result:
            await update.message.reply_text(f"⚠️ No data available for {symbol}.", parse_mode="Markdown")
            logger.info(f"No data found for symbol {symbol}")
            return

        message = (
            f"📈 *Symbol Analysis*\n\n"
            f"*Symbol:* {symbol}\n"
            f"*Action:* {result['signal']}\n"
            f"*Short-Term Trend:* {result['short_term_trend']}\n"
            f"*Mid-Term Trend:* {result['mid_term_trend']}\n"
            f"*RSI:* {result['rsi']}\n"
            f"*Pattern Detected:* {result['pattern']}\n"
            f"*Candlestick Formation:* {result['candlestick']}\n"
            f"*Quality Rating:* {result['stars']} ⭐\n"
            f"*Suggested Holding:* {result['suggested_holding']}\n\n"
            f"🔎 Always manage your risk. No financial advice."
        )

        await update.message.reply_text(message, parse_mode="Markdown")
        logger.info(f"Analysis completed for {symbol} – triggered by {user}")

    except Exception as e:
        logger.error(f"Error analyzing symbol {symbol}: {e}")
        await update.message.reply_text(f"⚠️ Error analyzing {symbol}. Please try again later.", parse_mode="Markdown")

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sets the user preferred language."""
    user = update.effective_user.first_name or "Trader"

    if not context.args:
        await update.message.reply_text("Please provide a language code (e.g., 'de' or 'en').")
        logger.warning(f"/setlanguage triggered by {user} without specifying language.")
        return

    choice = context.args[0].lower()
    if choice in ("de", "deutsch"):
        lang = "de"
    elif choice in ("en", "english"):
        lang = "en"
    else:
        await update.message.reply_text("Unknown language. Supported options: 'de', 'en'.")
        logger.warning(f"/setlanguage triggered by {user} with invalid language input: {choice}")
        return

    context.user_data["lang"] = lang
    confirmation = get_text("set_language", lang)

    logger.info(f"Language set to {lang} by {user}")
    await update.message.reply_text(confirmation)
