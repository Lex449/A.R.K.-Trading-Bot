# bot/auto/auto_signal.py

import asyncio
from telegram import Bot
from bot.engine.analysis_engine import analyze_symbol
from bot.engine.risk_manager import assess_signal_risk
from bot.utils.session_tracker import update_session_tracker
from bot.utils.error_reporter import report_error
from bot.utils.market_time import is_trading_day, is_trading_hours
from bot.config.settings import get_settings
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# Load configuration once
config = get_settings()

async def auto_signal_loop():
    """
    Continuously analyzes configured symbols and sends trading signals automatically,
    but only during valid US trading hours and trading days.
    """
    bot = Bot(token=config["BOT_TOKEN"])
    chat_id = int(config["TELEGRAM_CHAT_ID"])

    try:
        await bot.delete_webhook()
        logger.info("[Auto Signal] Deleted existing webhook (if any).")
    except Exception as e:
        logger.warning(f"[Auto Signal] Failed to delete webhook: {str(e)}")

    logger.info("[Auto Signal] Starting main auto-signal loop.")

    while True:
        try:
            # Market Timing Check
            if not is_trading_day() or not is_trading_hours():
                logger.info("[Auto Signal] Market closed. Sleeping for 5 minutes.")
                await asyncio.sleep(300)  # Sleep 5 minutes during closed market
                continue

            symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
            if not symbols:
                logger.error("[Auto Signal] No symbols configured! Sleeping...")
                await asyncio.sleep(config.get("SIGNAL_CHECK_INTERVAL_SEC", 60))
                continue

            for symbol in symbols:
                try:
                    result = await analyze_symbol(symbol)

                    if not result:
                        logger.warning(f"[Auto Signal] No data for {symbol}. Skipped.")
                        continue

                    if result['signal'] == "Hold" or result['pattern'] == "No Pattern":
                        logger.info(f"[Auto Signal] {symbol} → Hold or no pattern. Skipped.")
                        continue

                    # Risk Assessment
                    risk_message, is_warning = await assess_signal_risk(result)
                    update_session_tracker(result["stars"])

                    # Prepare and send signal
                    message = (
                        f"📈 *Auto Trading Signal*\n\n"
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
                        f"⚡ _Always manage your risk wisely._"
                    )

                    await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
                    logger.info(f"[Auto Signal] Signal sent for {symbol}.")
                    await asyncio.sleep(1.5)  # kleine Pause zwischen den Symbolen

                except Exception as symbol_error:
                    logger.error(f"[Auto Signal Error] Symbol {symbol}: {str(symbol_error)}")
                    await report_error(bot, chat_id, symbol_error, context_info=f"AutoSignal for {symbol}")

            logger.info("[Auto Signal] Round completed. Sleeping before next cycle.")
            await asyncio.sleep(config.get("SIGNAL_CHECK_INTERVAL_SEC", 60))

        except Exception as loop_error:
            logger.critical(f"[Auto Signal Loop Fatal Error] {str(loop_error)}")
            await report_error(bot, chat_id, loop_error, context_info="Fatal error in auto_signal_loop")
            await asyncio.sleep(300)  # Sleep 5 minutes after fatal error
