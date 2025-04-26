# bot/handlers/analyse.py

from telegram import Update
from telegram.ext import ContextTypes
from bot.engine.analysis_engine import analyze_symbol
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.error_reporter import report_error
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

async def analyse_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler for /analyse command.
    Analyzes a specific financial symbol provided by the user.
    """
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"
    lang = get_language(chat_id) or "en"

    try:
        if not context.args:
            await update.message.reply_text(get_text("analysis_no_symbol", lang))
            logger.warning(f"/analyse without symbol by {user}")
            return

        symbol = context.args[0].upper()
        result = await analyze_symbol(symbol)

        if not result:
            await update.message.reply_text(f"⚠️ No data found for `{symbol}`.", parse_mode="Markdown")
            logger.warning(f"No data for symbol: {symbol}")
            return

        message = (
            f"📈 *Symbol Analysis*\n\n"
            f"*Symbol:* `{symbol}`\n"
            f"*Action:* {result['signal']}\n"
            f"*Short-Term Trend:* {result['short_term_trend']}\n"
            f"*Mid-Term Trend:* {result['mid_term_trend']}\n"
            f"*RSI:* {result['rsi']}\n"
            f"*Pattern:* {result['pattern']}\n"
            f"*Candlestick:* {result['candlestick']}\n"
            f"*Rating:* {result['stars']} ⭐\n"
            f"*Suggested Holding:* {result['suggested_holding']}\n\n"
            f"⚡ Stay sharp."
        )

        await update.message.reply_text(message, parse_mode="Markdown")
        logger.info(f"Sent analysis for {symbol} to {user}")

    except Exception as e:
        await report_error(context.bot, chat_id, e, context_info="Analyse Command Error")
        logger.error(f"Error in /analyse command: {e}")
