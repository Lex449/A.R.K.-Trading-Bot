"""
A.R.K. Analyse Command Handler – Live Deep Precision Analysis
Handles /analyse requests with dynamic Deep Confidence boosting.
"""

from telegram import Update
from telegram.ext import ContextTypes
from bot.engine.analysis_engine import analyze_symbol
from bot.engine.deep_confidence_engine import adjust_confidence  # NEU
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.error_reporter import report_error
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

async def analyse_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles /analyse command.
    Delivers real-time premium market analysis for a specific symbol.
    """
    chat_id = update.effective_chat.id
    user_name = update.effective_user.first_name or "Trader"
    lang = get_language(chat_id) or "en"

    try:
        # Check if a symbol is provided
        if not context.args:
            await update.message.reply_text(
                get_text("analysis_no_symbol", lang),
                parse_mode="Markdown"
            )
            logger.warning(f"[Analyse] No symbol provided by {user_name} (Chat ID: {chat_id})")
            return

        symbol = context.args[0].upper()
        result = await analyze_symbol(symbol)

        if not result:
            await update.message.reply_text(
                f"⚠️ *No data available for* `{symbol}`.",
                parse_mode="Markdown"
            )
            logger.warning(f"[Analyse] No data found for {symbol}")
            return

        # Deep Confidence Boosting
        raw_confidence = result.get("avg_confidence", 0)
        adjusted_confidence = adjust_confidence(raw_confidence)

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
            f"*Adjusted Confidence:* `{adjusted_confidence:.2f}%`\n"
            f"*Suggested Holding:* {result.get('suggested_holding', '-')}\n\n"
            f"_🧠 Stay sharp. Mastery is a daily habit._"
        )

        await update.message.reply_text(message, parse_mode="Markdown")
        logger.info(f"[Analyse] Sent deep analysis for {symbol} to {user_name} (Chat ID: {chat_id})")

    except Exception as error:
        await report_error(context.bot, chat_id, error, context_info="Analyse Command Error")
        logger.error(f"[Analyse] Exception: {error}")
