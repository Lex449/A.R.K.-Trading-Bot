import asyncio
import logging
from telegram import Bot
from telegram.ext import ContextTypes
from bot.engine.analysis_engine import analyze_symbol
from bot.engine.risk_manager import assess_signal_risk
from bot.utils.session_tracker import update_session_tracker
from bot.utils.error_reporter import report_error
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.autoscaler import run_autoscaler
from bot.config.settings import get_settings

# Setup Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Load configuration
config = get_settings()

async def daily_analysis_job(context: ContextTypes.DEFAULT_TYPE):
    """
    Executes a refined daily analysis of all monitored symbols,
    filtering only actionable trading opportunities.
    """
    bot: Bot = context.bot
    chat_id = int(config["TELEGRAM_CHAT_ID"])
    lang = get_language(chat_id) or "en"

    await bot.send_message(chat_id=chat_id, text="📊 *Starting daily advanced market analysis...*", parse_mode="Markdown")

    try:
        await run_autoscaler(bot, chat_id)
    except Exception as e:
        await report_error(bot, chat_id, e, context_info="Autoscaler Error")
        logger.error(f"Autoscaler error: {e}")

    symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
    if not symbols:
        await bot.send_message(chat_id=chat_id, text="❌ No symbols defined for analysis.", parse_mode="Markdown")
        return

    for symbol in symbols:
        try:
            result = await analyze_symbol(symbol)

            if not result:
                continue

            if result['signal'] == "Hold" or result['pattern'] == "No Pattern":
                logger.info(f"No actionable setup for {symbol}. Skipping.")
                continue

            # Risk Check + Session Update
            risk_message, is_warning = await assess_signal_risk(result)
            update_session_tracker(result['stars'])

            # Prepare final analysis message
            message = (
                f"📈 *Daily Analysis Signal*\n\n"
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
                f"⚡ *Stay sharp. No financial advice.*"
            )

            await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
            logger.info(f"Sent daily analysis for {symbol} – {result['signal']} with {result['pattern']}")
            await asyncio.sleep(1.5)

        except Exception as e:
            await report_error(bot, chat_id, e, context_info=f"Analysis error for {symbol}")
            logger.error(f"Error analyzing {symbol}: {e}")

    await bot.send_message(chat_id=chat_id, text="✅ *Daily analysis completed successfully!*", parse_mode="Markdown")
