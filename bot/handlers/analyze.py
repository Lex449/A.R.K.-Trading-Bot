# bot/handlers/analyze.py

from telegram import Update
from telegram.ext import ContextTypes
from bot.engine.analysis_engine import analyze_symbol
from bot.engine.risk_manager import assess_signal_risk
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.logger import setup_logger
from bot.utils.error_reporter import report_error

# Setup structured logger
logger = setup_logger(__name__)

async def analyze_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler for /analyze command.
    Analyzes a single symbol or multiple symbols from the user's request.
    """
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"
    lang = get_language(chat_id)

    if not context.args:
        logger.warning(f"Analyze command by {user} without parameters.")
        await update.message.reply_text(get_text("analysis_no_symbol", lang))
        return

    for symbol in context.args:
        symbol = symbol.upper().strip()

        logger.info(f"Analyze command: {user} requested analysis for {symbol}")

        try:
            result = await analyze_symbol(symbol)

            if not result:
                await update.message.reply_text(f"⚠️ No data available for `{symbol}`.", parse_mode="Markdown")
                continue

            # Optional Risk Assessment
            risk_message, is_warning = await assess_signal_risk(result)

            message = (
                f"📈 *Symbol Analysis*\n\n"
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
                f"🔎 _Stay focused. No financial advice._"
            )

            await context.bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
            await asyncio.sleep(1.5)

        except Exception as e:
            await report_error(context.bot, chat_id, e, context_info=f"Analyze Command Error for {symbol}")
            logger.error(f"Error analyzing {symbol}: {e}")
