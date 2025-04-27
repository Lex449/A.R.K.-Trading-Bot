"""
A.R.K. Signal Command – Premium Ultra Build.
Detects real trading opportunities across configured symbols.
"""

from telegram import Update
from telegram.ext import ContextTypes
from bot.engine.analysis_engine import analyze_symbol
from bot.engine.risk_manager import assess_signal_risk
from bot.utils.session_tracker import update_session_tracker
from bot.utils.error_reporter import report_error
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

async def signal_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the /signal command.
    Sends live trading signals based on configured symbol list.
    """
    chat_id = update.effective_chat.id
    user_name = update.effective_user.first_name or "Trader"
    language = get_language(chat_id) or "en"

    try:
        # Welcome Message
        await update.message.reply_text(get_text("signal_start", language))
        logger.info(f"[Signal] Command triggered by {user_name} (Chat ID: {chat_id})")

        # Load symbols
        symbols = context.bot_data.get("symbols", [])
        if not symbols:
            await update.message.reply_text(get_text("signal_no_symbols", language))
            logger.warning(f"[Signal] No symbols configured (User: {user_name})")
            return

        signal_count = 0

        # Analyze each symbol
        for symbol in symbols:
            result = await analyze_symbol(symbol)

            if not result:
                logger.info(f"[Signal] No analysis result for {symbol}. Skipping.")
                continue

            if result.get('signal') == "Hold" or result.get('pattern') == "No Pattern":
                logger.info(f"[Signal] {symbol} – Hold/No Pattern. Skipping.")
                continue

            # Risk Management & Tracking
            risk_message, _ = await assess_signal_risk(result)
            update_session_tracker(result.get("stars", 0))

            # Build Signal Message
            signal_message = (
                f"📈 *Trading Signal*\n\n"
                f"*Symbol:* `{symbol}`\n"
                f"*Action:* {result.get('signal', 'Neutral')}\n"
                f"*Short-Term Trend:* {result.get('short_term_trend', '-')}\n"
                f"*Mid-Term Trend:* {result.get('mid_term_trend', '-')}\n"
                f"*RSI:* {result.get('rsi', '-')}\n"
                f"*Pattern:* {result.get('pattern', '-')}\n"
                f"*Candlestick:* {result.get('candlestick', '-')}\n"
                f"*Rating:* {result.get('stars', 0)} ⭐\n"
                f"*Suggested Holding:* {result.get('suggested_holding', '-')}\n\n"
                f"{risk_message}\n"
                f"_⚡ Precision before quantity. Stay sharp._"
            )

            await update.message.reply_text(signal_message, parse_mode="Markdown")
            logger.info(f"[Signal] Signal sent for {symbol}")

            signal_count += 1

        if signal_count == 0:
            await update.message.reply_text(get_text("signal_no_valid", language))
            logger.info(f"[Signal] No actionable signals found (User: {user_name})")

    except Exception as error:
        logger.error(f"[Signal Command Error] {error}")
        await report_error(context.bot, chat_id, error, context_info="Signal Command Failure")
