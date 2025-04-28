"""
A.R.K. Signal Handler – Precision Signal Dispatch
Handles /signal requests with Deep Confidence Boost and Risk Assessment.
"""

from telegram import Update
from telegram.ext import ContextTypes
from bot.engine.analysis_engine import analyze_symbol
from bot.engine.risk_manager import assess_signal_risk
from bot.engine.deep_confidence_engine import adjust_confidence  # NEU eingebaut
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
    Sends live trading signals based on the configured symbol list.
    """
    chat_id = update.effective_chat.id
    user_name = update.effective_user.first_name or "Trader"
    language = get_language(chat_id) or "en"

    try:
        # Send welcome message
        await update.message.reply_text(get_text("signal_start", language))
        logger.info(f"[Signal] Command triggered by {user_name} (Chat ID: {chat_id})")

        # Get configured symbols
        symbols = context.bot_data.get("symbols", [])
        if not symbols:
            await update.message.reply_text(get_text("signal_no_symbols", language))
            logger.warning(f"[Signal] No symbols configured (User: {user_name})")
            return

        signal_count = 0

        for symbol in symbols:
            result = await analyze_symbol(symbol)

            if not result:
                logger.info(f"[Signal] No data for {symbol}. Skipping.")
                continue

            if result.get('signal') == "Hold" or result.get('pattern') == "No Pattern":
                logger.info(f"[Signal] {symbol} – Hold/No Pattern. Skipping.")
                continue

            # Deep Confidence Engine Integration
            raw_confidence = result.get("avg_confidence", 0)
            confidence = adjust_confidence(raw_confidence)

            # Risk Management
            risk_message, _ = await assess_signal_risk(result)

            # Session Update
            stars = 5 if confidence >= 70 else 4 if confidence >= 65 else 3
            update_session_tracker(stars=stars, confidence=confidence)

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
                f"*Rating:* {stars} ⭐\n"
                f"*Adjusted Confidence:* `{confidence:.1f}%`\n"
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
