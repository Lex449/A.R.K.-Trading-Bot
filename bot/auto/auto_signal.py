import asyncio
import logging
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

# Load configuration
config = get_settings()

async def auto_signal_loop():
    """
    Continuously analyzes configured symbols
    and sends trading signals during valid trading hours.
    """
    bot = Bot(token=config["BOT_TOKEN"])
    chat_id = int(config["TELEGRAM_CHAT_ID"])

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("[Auto Signal] Webhook deleted (if present).")
    except Exception as e:
        logger.warning(f"[Auto Signal] Error deleting webhook: {e}")

    logger.info("[Auto Signal] Starting main signal loop.")

    while True:
        try:
            # Market Timing Check
            if not is_trading_day() or not is_trading_hours():
                logger.info("[Auto Signal] Market closed. Pausing for 5 minutes.")
                await asyncio.sleep(300)
                continue

            symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
            if not symbols:
                logger.error("[Auto Signal] No symbols configured! Pausing for 1 minute.")
                await asyncio.sleep(config.get("SIGNAL_CHECK_INTERVAL_SEC", 60))
                continue

            for symbol in symbols:
                try:
                    result = await analyze_symbol(symbol)

                    if not result:
                        logger.warning(f"[Auto Signal] No data for {symbol}. Skipping.")
                        continue

                    if result.get('signal') == "Hold" or result.get('pattern') == "No Pattern":
                        logger.info(f"[Auto Signal] {symbol} → Hold or no pattern recognized. Skipping.")
                        continue

                    # Risk Assessment
                    risk_message, _ = await assess_signal_risk(result)

                    # Session Update
                    update_session_tracker(result.get("stars", 0))

                    # Build Signal Message
                    message = (
                        f"⚡ *Auto Trading Signal*\n\n"
                        f"*Symbol:* `{symbol}`\n"
                        f"*Direction:* {result['signal']} {'📈' if result['signal'] == 'Buy' else '📉'}\n"
                        f"*Short-Term Trend:* {result.get('short_term_trend', '-')}\n"
                        f"*Mid-Term Trend:* {result.get('mid_term_trend', '-')}\n"
                        f"*RSI:* {result.get('rsi', '-')}\n"
                        f"*Pattern:* {result.get('pattern', '-')}\n"
                        f"*Candlestick:* {result.get('candlestick', '-')}\n"
                        f"*Quality Rating:* {'⭐' * result.get('stars', 0)}\n"
                        f"*Suggested Holding Duration:* {result.get('suggested_holding', '-')}\n\n"
                        f"{risk_message}\n"
                        f"_Note: Act responsibly when trading._"
                    )

                    await bot.send_message(
                        chat_id=chat_id,
                        text=message,
                        parse_mode="Markdown",
                        disable_web_page_preview=True
                    )
                    logger.info(f"[Auto Signal] Signal sent for {symbol}.")
                    await asyncio.sleep(1.5)

                except Exception as symbol_error:
                    logger.error(f"[Auto Signal] Error for {symbol}: {symbol_error}")
                    await report_error(bot, chat_id, symbol_error, context_info=f"AutoSignal for {symbol}")

            logger.info("[Auto Signal] Cycle completed. Pausing until next check.")
            await asyncio.sleep(config.get("SIGNAL_CHECK_INTERVAL_SEC", 60))

        except Exception as loop_error:
            logger.critical(f"[Auto Signal Loop] Critical error: {loop_error}")
            await report_error(bot, chat_id, loop_error, context_info="Fatal error in auto_signal_loop")
            await asyncio.sleep(300)
