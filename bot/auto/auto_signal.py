import os
import asyncio
import logging
from telegram import Bot
from bot.engine.analysis_engine import analyze_symbol
from bot.engine.risk_manager import assess_signal_risk
from bot.utils.session_tracker import update_session_tracker
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings

# Setup Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Load Settings
config = get_settings()

async def auto_signal_loop():
    """
    Continuously monitors symbols and sends trading signals ONLY when relevant conditions are met.
    """

    bot = Bot(token=config["BOT_TOKEN"])
    chat_id = int(config["TELEGRAM_CHAT_ID"])

    try:
        await bot.delete_webhook()
    except Exception as e:
        logger.warning(f"Failed to delete webhook: {str(e)}")

    while True:
        symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
        if not symbols:
            logger.error("No symbols configured for auto-analysis.")
            await asyncio.sleep(config.get("SIGNAL_CHECK_INTERVAL_SEC", 60))
            continue

        for symbol in symbols:
            try:
                result = await analyze_symbol(symbol)

                # Relevanzprüfung
                if not result:
                    continue

                if result['signal'] == "Hold" or result['pattern'] == "No Pattern":
                    logger.info(f"No actionable pattern for {symbol}. Skipping.")
                    continue

                # Risk Check + Session Update
                risk_message, is_warning = await assess_signal_risk(result)
                update_session_tracker(result['stars'])

                # Signal Message
                message = (
                    f"📢 *New Trading Signal*\n\n"
                    f"*Symbol:* `{symbol}`\n"
                    f"*Action:* {result['signal']}\n"
                    f"*Short-Term Trend:* {result['short_term_trend']}\n"
                    f"*Mid-Term Trend:* {result['mid_term_trend']}\n"
                    f"*RSI:* {result['rsi']}\n"
                    f"*Pattern:* {result['pattern']}\n"
                    f"*Candlestick Formation:* {result['candlestick']}\n"
                    f"*Quality Rating:* {result['stars']} ⭐\n"
                    f"*Suggested Holding:* {result['suggested_holding']}\n\n"
                    f"{risk_message}\n"
                    f"⚡ *Stay sharp. No financial advice.*"
                )

                await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
                logger.info(f"Signal sent for {symbol} – {result['signal']} with {result['pattern']}")
                await asyncio.sleep(1.5)  # Respect Telegram API rate limits

            except Exception as e:
                await report_error(bot, chat_id, e, context_info=f"AutoSignal error with {symbol}")
                logger.error(f"AutoSignal Error for {symbol}: {e}")

        logger.info("Auto signal round completed. Waiting for next scan...")
        await asyncio.sleep(config.get("SIGNAL_CHECK_INTERVAL_SEC", 60))
