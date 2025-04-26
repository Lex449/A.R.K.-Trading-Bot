# bot/auto/auto_signal_loop.py

import asyncio
from datetime import datetime
from telegram import Bot
from bot.engine.analysis_engine import analyze_symbol
from bot.engine.risk_manager import assess_signal_risk
from bot.utils.session_tracker import update_session_tracker
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings
from bot.utils.market_time import (
    is_trading_day,
    is_trading_hours,
    is_15min_before_market_open,
    is_15min_before_market_close,
    is_friday_close
)
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# Load configuration once
config = get_settings()

async def auto_signal_loop():
    """
    Monitors market times, sends live trading signals for configured symbols,
    and provides market opening/closing alerts.
    """
    bot = Bot(token=config["BOT_TOKEN"])
    chat_id = int(config["TELEGRAM_CHAT_ID"])

    try:
        await bot.delete_webhook()
        logger.info("[AutoSignal] Deleted previous webhook (if any).")
    except Exception as e:
        logger.warning(f"[AutoSignal] Failed to delete webhook: {e}")

    logger.info("[AutoSignal] Auto signal loop started.")

    # Track alert flags per session
    open_alert_sent = False
    close_alert_sent = False
    friday_alert_sent = False

    while True:
        try:
            now = datetime.utcnow()

            # === Pre-Market Checks ===
            if not is_trading_day():
                logger.info("[AutoSignal] Today is not a trading day. Sleeping 5 minutes.")
                await asyncio.sleep(300)
                open_alert_sent = False
                close_alert_sent = False
                friday_alert_sent = False
                continue

            if is_15min_before_market_open() and not open_alert_sent:
                await bot.send_message(chat_id=chat_id, text="⏳ *15 minutes until US markets open!*", parse_mode="Markdown")
                logger.info("[AutoSignal] 15 min before market open alert sent.")
                open_alert_sent = True

            if is_15min_before_market_close() and not close_alert_sent:
                await bot.send_message(chat_id=chat_id, text="⏳ *15 minutes until US markets close!*", parse_mode="Markdown")
                logger.info("[AutoSignal] 15 min before market close alert sent.")
                close_alert_sent = True

            if is_friday_close() and not friday_alert_sent:
                await bot.send_message(chat_id=chat_id, text="✅ *Trading week completed! Great job!*", parse_mode="Markdown")
                logger.info("[AutoSignal] Friday close alert sent.")
                friday_alert_sent = True

            # === Market Hours Check ===
            if not is_trading_hours():
                logger.info("[AutoSignal] Market closed. Sleeping 5 minutes.")
                await asyncio.sleep(300)
                continue

            # === Signal Processing ===
            symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
            if not symbols:
                logger.error("[AutoSignal] No symbols configured for auto-analysis.")
                await asyncio.sleep(300)
                continue

            for symbol in symbols:
                try:
                    result = await analyze_symbol(symbol)

                    if not result:
                        logger.warning(f"[AutoSignal] No result for {symbol}. Skipped.")
                        await asyncio.sleep(1)
                        continue

                    if result['signal'] == "Hold":
                        logger.info(f"[AutoSignal] {symbol}: No actionable signal (Hold). Skipped.")
                        continue

                    risk_message, _ = await assess_signal_risk(result)
                    update_session_tracker(result["stars"])

                    message = (
                        f"📈 *Live Trading Signal*\n\n"
                        f"*Symbol:* `{symbol}`\n"
                        f"*Action:* {result['signal']}\n"
                        f"*Short-Term Trend:* {result['short_term_trend']}\n"
                        f"*Mid-Term Trend:* {result['mid_term_trend']}\n"
                        f"*RSI:* {result['rsi']}\n"
                        f"*Pattern:* {result['pattern']}\n"
                        f"*Candlestick:* {result['candlestick']}\n"
                        f"*Quality Rating:* {result['stars']} ⭐\n"
                        f"*Suggested Holding:* {result['suggested_holding']}\n\n"
                        f"{risk_message}\n"
                        f"⚡ _Always manage your risk. No financial advice._"
                    )

                    await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
                    logger.info(f"[AutoSignal] Sent signal for {symbol}.")
                    await asyncio.sleep(1.5)

                except Exception as symbol_error:
                    await report_error(bot, chat_id, symbol_error, context_info=f"AutoSignal Loop - Symbol {symbol}")
                    logger.error(f"[AutoSignal] Error analyzing {symbol}: {symbol_error}")

            logger.info("[AutoSignal] Round completed. Waiting for next cycle.")
            await asyncio.sleep(config.get("SIGNAL_CHECK_INTERVAL_SEC", 60))

        except Exception as loop_error:
            await report_error(bot, chat_id, loop_error, context_info="AutoSignal Main Loop Error")
            logger.critical(f"[AutoSignal] Fatal error: {loop_error}")
            await asyncio.sleep(300)  # Small break before retrying
