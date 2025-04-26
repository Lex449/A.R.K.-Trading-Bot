import asyncio
import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.engine.analysis_engine import analyze_symbol
from bot.engine.risk_manager import assess_signal_risk
from bot.utils.session_tracker import update_session_tracker
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Load configuration
config = get_settings()

async def signal_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler for /signal command.
    Analyzes all configured symbols and sends filtered trading signals to Telegram.
    """
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text="🚀 *Scanning for high-probability trading signals...*", parse_mode="Markdown")

    symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
    if not symbols:
        await context.bot.send_message(chat_id=chat_id, text="❌ No symbols configured for signal analysis.", parse_mode="Markdown")
        return

    profitable_signals_found = False

    for symbol in symbols:
        try:
            result = await analyze_symbol(symbol)

            if not result:
                logger.warning(f"No data for {symbol}")
                continue

            # Only show signals with >= 3 Stars
            if result["stars"] >= 3:
                profitable_signals_found = True

                # Risk Management and Session Tracking
                risk_message, is_warning = await assess_signal_risk(result)
                update_session_tracker(result['stars'])

                # Signal Message
                message = (
                    f"📈 *Trading Signal*\n\n"
                    f"*Symbol:* `{symbol}`\n"
                    f"*Action:* {result['signal']}\n"
                    f"*Short-Term Trend:* {result['short_term_trend']}\n"
                    f"*Mid-Term Trend:* {result['mid_term_trend']}\n"
                    f"*RSI:* {result['rsi']}\n"
                    f"*Pattern Detected:* {result['pattern']}\n"
                    f"*Candlestick Formation:* {result['candlestick']}\n"
                    f"*Quality Rating:* {result['stars']} ⭐\n"
                    f"*Suggested Holding:* {result['suggested_holding']}\n\n"
                    f"{risk_message}\n"
                    f"⚡ Always manage your risk wisely. _No financial advice._"
                )

                await context.bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
                await asyncio.sleep(1.2)

        except Exception as e:
            await report_error(context.bot, chat_id, e, context_info=f"Error during signal analysis for {symbol}")
            logger.error(f"Signal analysis error for {symbol}: {e}")

    if not profitable_signals_found:
        await context.bot.send_message(chat_id=chat_id, text="⚠️ *No strong signals (≥ 3⭐) detected at the moment.*", parse_mode="Markdown")
    else:
        await context.bot.send_message(chat_id=chat_id, text="✅ *Signal scan completed. Stay sharp!*", parse_mode="Markdown")
