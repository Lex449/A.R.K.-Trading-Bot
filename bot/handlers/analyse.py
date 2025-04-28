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
    Handles /analyse command.
    Delivers premium market analysis for a requested symbol.
    """
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"
    lang = get_language(chat_id) or "en"

    try:
        # Check if a symbol is provided
        if not context.args:
            await update.message.reply_text(
                get_text("analysis_no_symbol", lang),
                parse_mode="Markdown"
            )
            logger.warning(f"[Analyse] No symbol provided by {user} (Chat ID: {chat_id})")
            return

        symbol = context.args[0].upper()  # Ensure the symbol is uppercase
        result = await analyze_symbol(symbol)

        # Check if no analysis data is found
        if not result:
            await update.message.reply_text(
                f"⚠️ *No data available for* `{symbol}`.",
                parse_mode="Markdown"
            )
            logger.warning(f"[Analyse] No analysis data for {symbol}")
            return

        # Prepare the message to send to the user
        message = (
            f"📊 *A.R.K. Live Analysis*\n\n"
            f"*Symbol:* `{symbol}`\n"
            f"*Signal:* {result.get('combined_action', '-')}\n"
            f"*Short-Term Trend:* {result.get('short_term_trend', '-')}\n"
            f"*Mid-Term Trend:* {result.get('mid_term_trend', '-')}\n"
            f"*RSI (14):* `{result.get('rsi', '-')}%`\n"
            f"*Pattern:* {result.get('pattern', '-')}\n"
            f"*Candle Formation:* {result.get('candlestick', '-')}\n"
            f"*Rating:* {'⭐' * result.get('stars', 0)}\n"
            f"*Suggested Holding Time:* {result.get('suggested_holding', '-')}\n\n"
            f"_🧠 Stay focused. Greatness is built one decision at a time._"
        )

        await update.message.reply_text(message, parse_mode="Markdown")
        logger.info(f"[Analyse] Successful analysis for {symbol} sent to {user} (Chat ID: {chat_id})")

    except Exception as e:
        # Report error if something goes wrong
        await report_error(context.bot, chat_id, e, context_info="Analyse Command Error")
        logger.error(f"[Analyse] Exception: {e}")
