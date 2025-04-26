# bot/handlers/signal.py

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
    Handler for /signal command.
    Scans configured symbols and sends trading signals to the chat.
    """
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"
    lang = get_language(update)

    try:
        await update.message.reply_text(get_text("signal_start", lang))
        logger.info(f"Signal command triggered by {user} (Chat ID: {chat_id})")

        symbols = context.bot_data.get("symbols", [])
        if not symbols:
            await update.message.reply_text(get_text("signal_no_symbols", lang))
            logger.warning(f"No symbols configured for signals (User: {user})")
            return

        for symbol in symbols:
            result = await analyze_symbol(symbol)

            if not result:
                logger.warning(f"No data for symbol {symbol}")
                continue

            if result['signal'] == "Hold" or result['pattern'] == "No Pattern":
                logger.info(f"Skipping {symbol} (No actionable signal)")
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
                f"⚡ Stay sharp. No financial advice."
            )

            await update.message.reply_text(message, parse_mode="Markdown")
            logger.info(f"Sent trading signal for {symbol}")

    except Exception as e:
        await report_error(context.bot, chat_id, e, context_info="Signal Command Error")
        logger.error(f"Signal command error: {e}")
