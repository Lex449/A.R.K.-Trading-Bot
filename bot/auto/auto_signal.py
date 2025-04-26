import os
import asyncio
import logging
from telegram import Bot
from bot.engine.analysis_engine import analyze_symbol
from bot.engine.risk_manager import assess_signal_risk
from bot.utils.session_tracker import update_session_tracker
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings
import datetime

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Load configuration
config = get_settings()

async def auto_signal_loop():
    """
    Continuously sends trading signals automatically at configured intervals, only when markets are open and quality is high.
    """
    bot = Bot(token=config["BOT_TOKEN"])
    chat_id = int(config["TELEGRAM_CHAT_ID"])

    try:
        await bot.delete_webhook()
    except Exception as e:
        logger.warning(f"Failed to delete webhook: {str(e)}")

    while True:
        # Check if today is Saturday or Sunday (weekend)
        current_day = datetime.datetime.utcnow().weekday()
        if current_day >= 5:  # 5 = Saturday, 6 = Sunday
            logger.info("Market closed (weekend). Skipping signal scan...")
            await asyncio.sleep(3600)  # Sleep 1 hour, then recheck
            continue

        symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
        if not symbols:
            logger.error("No symbols configured for auto-analysis.")
            await asyncio.sleep(config.get("SIGNAL_CHECK_INTERVAL_SEC", 60))
            continue

        for symbol in symbols:
            try:
                result = await analyze_symbol(symbol)

                if not result:
                    await bot.send_message(chat_id=chat_id, text=f"⚠️ No data available for {symbol}.", parse_mode="Markdown")
                    continue

                # Apply 3-star quality filter
                if result["stars"] < 3:
                    logger.info(f"Skipping {symbol} due to low rating ({result['stars']} stars).")
                    continue

                # Risk Management and Session Tracking
                risk_message, is_warning = await assess_signal_risk(result)
                update_session_tracker(result['stars'])

                # Signal Message
                message = (
                    f"📈 *Auto Trading Signal*\n\n"
                    f"*Symbol:* {symbol}\n"
                    f"*Action:* {result['signal']}\n"
                    f"*Short-Term Trend:* {result['short_term_trend']}\n"
                    f"*Mid-Term Trend:* {result['mid_term_trend']}\n"
                    f"*RSI:* {result['rsi']}\n"
                    f"*Pattern Detected:* {result['pattern']}\n"
                    f"*Candlestick Formation:* {result['candlestick']}\n"
                    f"*Quality Rating:* {result['stars']} ⭐\n"
                    f"*Suggested Holding:* {result['suggested_holding']}\n\n"
                    f"{risk_message}\n"
                    f"🔎 Always manage your risk. No financial advice."
                )

                await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
                await asyncio.sleep(1.5)  # Respect Telegram API limits

            except Exception as e:
                await report_error(bot, chat_id, e, context_info=f"AutoSignal error with {symbol}")
                logger.error(f"AutoSignal Error for {symbol}: {e}")

        logger.info("Auto signal round completed. Waiting for next scan...")
        await asyncio.sleep(config.get("SIGNAL_CHECK_INTERVAL_SEC", 60))
