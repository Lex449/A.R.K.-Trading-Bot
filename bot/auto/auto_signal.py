# bot/auto/auto_signal.py

import asyncio
import logging
from telegram import Bot
from bot.engine.analysis_engine import analyze_symbol
from bot.engine.risk_manager import assess_signal_risk
from bot.utils.session_tracker import update_session_tracker
from bot.utils.error_reporter import report_error
from bot.utils.market_time import is_trading_day, is_trading_hours
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.config.settings import get_settings

# Setup Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Load configuration
config = get_settings()

async def auto_signal_loop():
    """
    Continuously analyzes and sends signals during market hours only.
    """
    bot = Bot(token=config["BOT_TOKEN"])
    chat_id = int(config["TELEGRAM_CHAT_ID"])

    try:
        await bot.delete_webhook()
    except Exception as e:
        logger.warning(f"Failed to delete webhook: {str(e)}")

    while True:
        # Nur prüfen, wenn Markt offen
        if not is_trading_day() or not is_trading_hours():
            logger.info("⏳ Market closed. Bot is sleeping...")
            await asyncio.sleep(300)  # 5 Minuten schlafen wenn geschlossen
            continue

        symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
        if not symbols:
            logger.error("❌ No symbols configured for auto-analysis.")
            await asyncio.sleep(config.get("SIGNAL_CHECK_INTERVAL_SEC", 60))
            continue

        for symbol in symbols:
            try:
                result = await analyze_symbol(symbol)

                if not result:
                    logger.info(f"No data for {symbol}.")
                    continue

                # Nur echte Trading-Setups senden
                if result['signal'] == "Hold" or result['pattern'] == "No Pattern":
                    logger.info(f"No actionable setup for {symbol}. Skipping.")
                    continue

                # Risk Check + Session Update
                risk_message, is_warning = await assess_signal_risk(result)
                update_session_tracker(result['stars'])

                # Prepare Signal Message
                message = (
                    f"📈 *Auto Trading Signal*\n\n"
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
                logger.info(f"Sent auto-signal for {symbol} – {result['signal']} with {result['pattern']}")
                await asyncio.sleep(1.5)  # Respect Telegram API Rate Limit

            except Exception as e:
                await report_error(bot, chat_id, e, context_info=f"AutoSignal error with {symbol}")
                logger.error(f"AutoSignal Error for {symbol}: {e}")

        logger.info("✅ Auto-signal round completed. Waiting for next cycle...")
        await asyncio.sleep(config.get("SIGNAL_CHECK_INTERVAL_SEC", 60))  # Standardmäßig 60 Sekunden pausieren
