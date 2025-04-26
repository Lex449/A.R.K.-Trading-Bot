# bot/handlers/commands.py

import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.language import get_language
from bot.engine.analysis_engine import analyze_symbol
from bot.utils.i18n import get_text
from bot.utils.session_tracker import get_session_report  # ← korrigiert
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name or "Trader"
    lang = get_language(update)
    greeting = get_text("start", lang).format(user=user)
    help_text = get_text("help", lang)

    logger.info(f"Start command initiated by {user} (Language: {lang})")
    await update.message.reply_text(f"{greeting}\n\n{help_text}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_language(update)
    help_text = get_text("help", lang)

    logger.info(f"Help command invoked by {update.effective_user.first_name}")
    await update.message.reply_text(help_text)

async def analyse_symbol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_language(update)

    if not context.args:
        logger.warning(f"No symbol provided in /analyse by {update.effective_user.first_name}")
        await update.message.reply_text(get_text("analysis_no_symbol", lang))
        return

    symbol = context.args[0].upper()

    try:
        result = await analyze_symbol(symbol)

        if not result:
            await update.message.reply_text(f"⚠️ No data available for {symbol}.", parse_mode="Markdown")
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
        logger.info(f"Analysis completed for {symbol} by {update.effective_user.first_name}")

    except Exception as e:
        logger.error(f"[Analysis Error] {symbol}: {e}")
        await update.message.reply_text(f"⚠️ Error analyzing {symbol}. Please try again later.", parse_mode="Markdown")

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide a language code (e.g., 'de' or 'en').")
        return

    choice = context.args[0].lower()
    if choice in ("de", "deutsch"):
        lang = "de"
    elif choice in ("en", "english"):
        lang = "en"
    else:
        await update.message.reply_text("Unknown language. Supported options: 'de', 'en'.")
        return

    context.user_data["lang"] = lang
    confirmation = get_text("set_language", lang)

    logger.info(f"Language set to {lang} by {update.effective_user.first_name}")
    await update.message.reply_text(confirmation)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"

    try:
        summary_text = get_session_report()  # ← korrigiert

        await context.bot.send_message(
            chat_id=chat_id,
            text=f"🔎 *Session Status for {user}:*\n\n{summary_text}",
            parse_mode="Markdown"
        )

        logger.info(f"Status requested by {user} (Chat ID: {chat_id})")

    except Exception as e:
        await report_error(context.bot, chat_id, e, context_info="Status Command Error")
        logger.error(f"Error during status command: {e}")
