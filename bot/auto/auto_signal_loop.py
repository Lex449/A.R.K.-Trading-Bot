# bot/auto/auto_signal_loop.py

import asyncio
import logging
from datetime import datetime
from telegram import Bot
from bot.engine.analysis_engine import analyze_symbol
from bot.engine.risk_manager import assess_signal_risk
from bot.utils.session_tracker import update_session_tracker
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings
from bot.utils.market_time import is_trading_day, is_trading_hours, is_15min_before_market_open, is_15min_before_market_close, is_friday_close

# Setup Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Load config
config = get_settings()

async def auto_signal_loop():
    bot = Bot(token=config["BOT_TOKEN"])
    chat_id = int(config["TELEGRAM_CHAT_ID"])

    try:
        await bot.delete_webhook()
    except Exception as e:
        logger.warning(f"Failed to delete webhook: {str(e)}")

    last_open_alert = False
    last_close_alert = False
    last_friday_alert = False

    while True:
        now = datetime.utcnow()

        if not is_trading_day():
            logger.info("Today is not a trading day.")
            await asyncio.sleep(300)
            continue

        if is_15min_before_market_open() and not last_open_alert:
            await bot.send_message(chat_id=chat_id, text="⏳ *15 Minutes until US Markets Open!*", parse_mode="Markdown")
            last_open_alert = True

        if is_15min_before_market_close() and not last_close_alert:
            await bot.send_message(chat_id=chat_id, text="⏳ *15 Minutes until US Markets Close!*", parse_mode="Markdown")
            last_close_alert = True

        if is_friday_close() and not last_friday_alert:
            await bot.send_message(chat_id=chat_id, text="✅ *Trading week completed! Great job!*", parse_mode="Markdown")
            last_friday_alert = True

        if not is_trading_hours():
            logger.info("Currently outside of trading hours.")
            await asyncio.sleep(300)
            continue

        symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
        if not symbols:
            logger.error("No symbols configured.")
            await asyncio.sleep(300)
            continue

        for symbol in symbols:
            try:
                result = await analyze_symbol(symbol)

                if not result:
                    await asyncio.sleep(1)
                    continue

                if result['signal'] == "Hold":
                    logger.info(f"No actionable signal for {symbol}.")
                    continue

                risk_message, is_warning = await assess_signal_risk(result)
                update_session_tracker(result['stars'])

                # Formatted Signal
                signal_message = (
                    f"📈 *Live Trading Signal*\n\n"
                    f"*Symbol:* `{symbol}`\n"
                    f"*Action:* {result['signal']}\n"
                    f"*Trend:* {result['short_term_trend']} ➡ {result['mid_term_trend']}\n"
                    f"*RSI:* {result['rsi']}\n"
                    f"*Pattern:* {result['pattern']}\n"
                    f"*Candlestick:* {result['candlestick']}\n"
                    f"*Quality:* {result['stars']} ⭐\n"
                    f"*Holding:* {result['suggested_holding']}\n\n"
                    f"{risk_message}\n"
                    f"⚡ No financial advice. Act smart!"
                )

                await bot.send_message(chat_id=chat_id, text=signal_message, parse_mode="Markdown")
                await asyncio.sleep(1.5)

            except Exception as e:
                await report_error(bot, chat_id, e, context_info=f"AutoSignal {symbol}")
                logger.error(f"AutoSignal Error: {e}")

        logger.info("Auto Signal Loop completed.")
        await asyncio.sleep(config.get("SIGNAL_CHECK_INTERVAL_SEC", 60))
