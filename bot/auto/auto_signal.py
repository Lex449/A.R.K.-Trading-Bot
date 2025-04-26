import os
import asyncio
import logging
from telegram import Bot
from bot.engine.analysis_engine import analyze_symbol
from bot.utils.autoscaler import run_autoscaler
from bot.config.settings import get_settings

# Load configuration
config = get_settings()
logger = logging.getLogger(__name__)

async def auto_signal_loop():
    """
    Continuously sends trading signals automatically at configured intervals.
    """
    bot = Bot(token=config["BOT_TOKEN"])
    chat_id = int(config["TELEGRAM_CHAT_ID"])

    if not bot:
        logger.error("Bot instance could not be initialized.")
        return

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
                logger.info(f"Analyzing symbol: {symbol}")

                result = await analyze_symbol(symbol)

                if not result:
                    await bot.send_message(chat_id=chat_id, text=f"⚠️ No data available for {symbol}.", parse_mode="Markdown")
                    continue

                message = (
                    f"📈 *Auto Signal*\n\n"
                    f"*Symbol:* {symbol}\n"
                    f"*Action:* {result['signal']}\n"
                    f"*Short-Term Trend:* {result['short_term_trend']}\n"
                    f"*Mid-Term Trend:* {result['mid_term_trend']}\n"
                    f"*RSI:* {result['rsi']}\n"
                    f"*Pattern Detected:* {result['pattern']}\n"
                    f"*Candlestick Formation:* {result['candlestick']}\n"
                    f"*Quality Rating:* {result['stars']} ⭐\n"
                    f"*Suggested Holding:* {result['suggested_holding']}\n\n"
                    f"🔎 Always manage your risk. No financial advice."
                )

                await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
                await asyncio.sleep(1.5)  # Telegram rate limit

            except Exception as e:
                logger.error(f"Error analyzing {symbol}: {str(e)}")
                await bot.send_message(chat_id=chat_id, text=f"⚠️ Error analyzing {symbol}: {str(e)}", parse_mode="Markdown")

        logger.info("Auto signal round completed. Waiting for next scan...")
        await asyncio.sleep(config.get("SIGNAL_CHECK_INTERVAL_SEC", 60))
