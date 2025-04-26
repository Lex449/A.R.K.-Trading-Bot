# bot/handlers/signal.py

from telegram import Update
from telegram.ext import ContextTypes
from bot.engine.analysis_engine import analyze_symbol
from bot.engine.risk_manager import assess_signal_risk
from bot.utils.session_tracker import update_session_tracker
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.error_reporter import report_error
from bot.utils.logger import setup_logger
from bot.config.settings import get_settings

# Setup structured logger
logger = setup_logger(__name__)

# Load config once
config = get_settings()

async def signal_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler for /signal command.
    Scans and sends trading signals for all monitored symbols.
    """
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"
    lang = get_language(chat_id) or "en"

    try:
        symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])

        if not symbols:
            await update.message.reply_text(get_text("signal_no_symbols", lang))
            logger.warning(f"No symbols configured for /signal (User: {user})")
            return

        await update.message.reply_text(get_text("signal_start", lang))
        logger.info(f"/signal triggered by {user}")

        for symbol in symbols:
            result = await analyze_symbol(symbol)

            if not result:
                logger.warning(f"No data for symbol: {symbol}")
                continue

            if result['signal'] == "Hold" or result['pattern'] == "No Pattern":
                logger.info(f"Skipping {symbol}: No strong signal")
                continue

            risk_message, _ = await assess_signal_risk(result)
            update_session_tracker(result["stars"])

            message = (
                f"📈 *Trading Signal*\n\n"
                f"*Symbol:* `{symbol}`\n"
                f"*Action:* {result['signal']}\n"
                f"*Short-Term Trend:* {result['short_term_trend']}\n"
                f"*Mid-Term Trend:* {result['mid_term_trend']}\n"
                f"*RSI:* {result['rsi']}\n"
                f"*Pattern:* {result['pattern']}\n"
                f"*Candlestick:* {result['candlestick']}\n"
                f"*Rating:* {result['stars']} ⭐\n"
                f"*Suggested Holding:* {result['suggested_holding']}\n\n"
                f"{risk_message}\n"
                f"⚡ Stay sharp."
            )

            await update.message.reply_text(message, parse_mode="Markdown")
            logger.info(f"Signal sent for {symbol}")

    except Exception as e:
        await report_error(context.bot, chat_id, e, context_info="Signal Command Error")
        logger.error(f"Critical error in /signal command: {e}")
