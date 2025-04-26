# bot/handlers/signal.py

import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from bot.engine.analysis_engine import analyze_symbol
from bot.engine.risk_manager import assess_signal_risk
from bot.utils.session_tracker import update_session_tracker
from bot.utils.logger import setup_logger
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings

# Setup structured logger
logger = setup_logger(__name__)

# Load configuration
config = get_settings()

async def signal_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler for /signal command.
    Scans the configured top assets and posts active trading signals.
    """
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"

    logger.info(f"Signal scan triggered by {user} (Chat ID: {chat_id})")
    await context.bot.send_message(chat_id=chat_id, text="🚀 *Scanning for fresh signals...*", parse_mode="Markdown")

    symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
    if not symbols:
        logger.warning(f"No symbols configured for signal analysis.")
        await context.bot.send_message(chat_id=chat_id, text="❌ No symbols configured for analysis.", parse_mode="Markdown")
        return

    for symbol in symbols:
        try:
            result = await analyze_symbol(symbol)

            if not result:
                continue

            if result['signal'] == "Hold" or result['pattern'] == "No Pattern":
                logger.info(f"No active trade setup for {symbol}. Skipping.")
                continue

            # Risk Management
            risk_message, is_warning = await assess_signal_risk(result)
            update_session_tracker(result['stars'])

            message = (
                f"📈 *Trading Signal*\n\n"
                f"*Symbol:* `{symbol}`\n"
                f"*Action:* {result['signal']}\n"
                f"*Short-Term Trend:* {result['short_term_trend']}\n"
                f"*Mid-Term Trend:* {result['mid_term_trend']}\n"
                f"*RSI:* {result['rsi']}\n"
                f"*Pattern:* {result['pattern']}\n"
                f"*Candlestick Formation:* {result['candlestick']}\n"
                f"*Quality Rating:* {result['stars']} ⭐\n"
                f"*Suggested Holding:* {result['suggested_holding']}\n\n"
                f"{risk_message}\n"
                f"🔎 _Manage risk wisely. No financial advice._"
            )

            await context.bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
            await asyncio.sleep(1.5)

        except Exception as e:
            await report_error(context.bot, chat_id, e, context_info=f"Signal Handler Error for {symbol}")
            logger.error(f"Error in signal analysis for {symbol}: {e}")

    logger.info(f"Signal scan completed for user {user}.")
