# bot/auto/auto_signal.py

import os
import asyncio
import logging
from datetime import datetime
from telegram import Bot
from bot.engine.analysis_engine import analyze_symbol
from bot.engine.risk_manager import assess_signal_risk
from bot.utils.session_tracker import update_session_tracker
from bot.utils.error_reporter import report_error
from bot.utils.market_time import is_trading_day, is_trading_hours, is_market_opening_soon
from bot.config.settings import get_settings

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Load configuration
config = get_settings()

# State to avoid multiple opening warnings
market_open_warning_sent = False

async def auto_signal_loop():
    """
    Continuously sends trading signals automatically at configured intervals,
    respecting US market open/close times and holidays.
    """
    global market_open_warning_sent

    bot = Bot(token=config["BOT_TOKEN"])
    chat_id = int(config["TELEGRAM_CHAT_ID"])

    try:
        await bot.delete_webhook()
    except Exception as e:
        logger.warning(f"Failed to delete webhook: {str(e)}")

    while True:
        now = datetime.now()

        if not is_trading_day():
            logger.info(f"Today ({now.strftime('%A')}) is not a trading day. Sleeping...")
            await asyncio.sleep(300)  # 5 Minuten schlafen
            continue

        if is_market_opening_soon() and not market_open_warning_sent:
            try:
                await bot.send_message(
                    chat_id=chat_id,
                    text="⚡️ *Attention:* US Markets will open in 15 minutes! Prepare yourself.",
                    parse_mode="Markdown"
                )
                logger.info("Market opening warning sent.")
                market_open_warning_sent = True
            except Exception as e:
                logger.error(f"Failed to send market opening warning: {e}")

        if not is_trading_hours():
            logger.info("Outside of trading hours. Waiting...")
            await asyncio.sleep(300)  # 5 Minuten schlafen
            continue

        # Reset the market opening warning after opening
        if market_open_warning_sent and datetime.now().hour >= 10:
            market_open_warning_sent = False

        symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
        if not symbols:
            logger.error("No symbols configured for auto-analysis.")
            await asyncio.sleep(config.get("SIGNAL_CHECK_INTERVAL_SEC", 60))
            continue

        logger.info(f"Starting signal scan for {len(symbols)} symbols...")

        for symbol in symbols:
            try:
                result = await analyze_symbol(symbol)

                if not result:
                    await bot.send_message(chat_id=chat_id, text=f"⚠️ No data available for {symbol}.", parse_mode="Markdown")
                    continue

                # Only proceed with signals rated 3 stars or higher
                if result['stars'] < 3:
                    logger.info(f"Skipped {symbol}: Signal quality below 3 stars.")
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
                await asyncio.sleep(1.5)  # Telegram API respektieren

            except Exception as e:
                await report_error(bot, chat_id, e, context_info=f"AutoSignal error with {symbol}")
                logger.error(f"AutoSignal Error for {symbol}: {e}")

        logger.info("✅ Auto signal round completed. Waiting for next scan...")
        await asyncio.sleep(config.get("SIGNAL_CHECK_INTERVAL_SEC", 60))
