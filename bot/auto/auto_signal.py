# bot/auto/auto_signal.py

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
from bot.utils.market_time import is_trading_day, is_trading_hours

# === Setup Logging ===
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# === Load Configuration ===
config = get_settings()

async def daily_analysis_job(context: ContextTypes.DEFAULT_TYPE):
    """
    Executes a refined daily analysis of all monitored symbols,
    filtering only actionable trading opportunities.
    Sends high-quality signals once daily during trading days.
    """
    bot: Bot = context.bot
    chat_id = int(config["TELEGRAM_CHAT_ID"])
    lang = get_language(chat_id) or "en"

    logger.info("Starting daily analysis job...")

    if not is_trading_day():
        logger.info("Not a trading day. Skipping analysis.")
        return

    if not is_trading_hours():
        logger.info("Not within trading hours. Skipping analysis.")
        return

    await bot.send_message(chat_id=chat_id, text="📊 *Daily market scan started...*", parse_mode="Markdown")

    try:
        await run_autoscaler(bot, chat_id)
    except Exception as e:
        await report_error(bot, chat_id, e, context_info="Autoscaler Error")
        logger.error(f"Autoscaler error: {e}")

    symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
    if not symbols:
        await bot.send_message(chat_id=chat_id, text="❌ No symbols configured for analysis.", parse_mode="Markdown")
        return

    for symbol in symbols:
        try:
            result = await analyze_symbol(symbol)

            if not result:
                continue

            if result['signal'] == "Hold" or result['pattern'] == "No Pattern":
                logger.info(f"No actionable signal for {symbol}. Skipping.")
                continue

            risk_message, is_warning = await assess_signal_risk(result)
            update_session_tracker(result['stars'])

            signal_text = (
                f"📈 *Daily Analysis Result*\n\n"
                f"*Symbol:* `{symbol}`\n"
                f"*Action:* {result['signal']}\n"
                f"*Trend:* {result['short_term_trend']} ➡ {result['mid_term_trend']}\n"
                f"*RSI:* {result['rsi']}\n"
                f"*Pattern:* {result['pattern']}\n"
                f"*Candlestick:* {result['candlestick']}\n"
                f"*Quality:* {result['stars']} ⭐\n"
                f"*Holding Recommendation:* {result['suggested_holding']}\n\n"
                f"{risk_message}\n"
                f"⚡ _Stay focused. No financial advice._"
            )

            await bot.send_message(chat_id=chat_id, text=signal_text, parse_mode="Markdown")
            logger.info(f"Signal sent for {symbol} – {result['signal']} [{result['stars']}⭐]")
            await asyncio.sleep(1.5)

        except Exception as e:
            await report_error(bot, chat_id, e, context_info=f"Analysis error for {symbol}")
            logger.error(f"Error analyzing {symbol}: {e}")

    await bot.send_message(chat_id=chat_id, text="✅ *Daily market scan completed successfully!*", parse_mode="Markdown")
    logger.info("Daily analysis completed.")
