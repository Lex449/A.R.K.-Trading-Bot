# bot/handlers/analyse.py

import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.engine.analysis_engine import analyze_symbol
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.error_reporter import report_error

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async def analyse_symbol(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles /analyse command for symbol-specific analysis.
    """
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"

    try:
        # Argumenten-Check
        if not context.args:
            await update.message.reply_text("❌ Please provide a symbol to analyze.\nExample: `/analyse AAPL`", parse_mode="Markdown")
            logger.warning(f"No symbol provided in /analyse by {user} (Chat ID: {chat_id})")
            return

        symbol = context.args[0].upper()

        # Basisvalidierung Symbol
        if not symbol.isalnum() or len(symbol) > 6:
            await update.message.reply_text("⚠️ Invalid symbol format. Please enter a valid stock symbol like `AAPL`, `MSFT`, etc.", parse_mode="Markdown")
            logger.warning(f"Invalid symbol format: {symbol} by {user}")
            return

        logger.info(f"Starting symbol analysis for {symbol} (Requested by {user})")

        # Analyse starten
        result = await analyze_symbol(symbol)

        if not result:
            await update.message.reply_text(f"⚠️ No data available for `{symbol}`.", parse_mode="Markdown")
            logger.warning(f"No data available for {symbol}")
            return

        # Ergebnis senden
        message = (
            f"📈 *Live Symbol Analysis*\n\n"
            f"*Symbol:* `{symbol}`\n"
            f"*Action:* {result['signal']}\n"
            f"*Short-Term Trend:* {result['short_term_trend']}\n"
            f"*Mid-Term Trend:* {result['mid_term_trend']}\n"
            f"*RSI:* {result['rsi']}\n"
            f"*Pattern Detected:* {result['pattern']}\n"
            f"*Candlestick Formation:* {result['candlestick']}\n"
            f"*Quality Rating:* {result['stars']} ⭐\n"
            f"*Suggested Holding:* {result['suggested_holding']}\n\n"
            f"⚡ Stay sharp. No financial advice."
        )

        await update.message.reply_text(message, parse_mode="Markdown")
        logger.info(f"Analysis for {symbol} completed successfully.")

    except Exception as e:
        await report_error(context.bot, chat_id, e, context_info="Analyse Command Error")
        logger.error(f"Error during /analyse command: {e}")
