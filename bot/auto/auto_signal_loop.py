# bot/auto/auto_signal_loop.py

import asyncio
from telegram import Bot
from bot.engine.analysis_engine import analyze_symbol
from bot.engine.risk_manager import assess_signal_risk
from bot.utils.session_tracker import update_session_tracker
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings
from bot.utils.market_time import is_trading_day, is_trading_hours
import logging

# Setup Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Load Config
config = get_settings()

async def auto_signal_loop():
    bot = Bot(token=config["BOT_TOKEN"])
    chat_id = int(config["TELEGRAM_CHAT_ID"])

    try:
        await bot.delete_webhook()
        logger.info("[Auto Signal] Deleted existing webhook (if any).")
    except Exception as e:
        logger.warning(f"[Auto Signal] Webhook deletion failed: {str(e)}")

    logger.info("[Auto Signal] Starting main auto-signal loop.")

    while True:
        try:
            # Check trading day
            if not is_trading_day():
                logger.info("[Auto Signal] Not a trading day. Sleeping...")
                await asyncio.sleep(300)
                continue

            # Check trading hours
            if not is_trading_hours():
                logger.info("[Auto Signal] Market closed. Sleeping...")
                await asyncio.sleep(300)
                continue

            symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
            if not symbols:
                logger.error("[Auto Signal] No symbols configured.")
                await asyncio.sleep(300)
                continue

            for symbol in symbols:
                try:
                    result = await analyze_symbol(symbol)

                    if not result or result["stars"] < 3:
                        continue  # Only proceed if star rating is high enough

                    # Optional Risk Assessment
                    risk_message, _ = await assess_signal_risk(result)

                    # Update Session Tracker
                    update_session_tracker(result["stars"])

                    # Build Signal Message
                    signal_text = (
                        f"⚡ *Live Trading Signal Detected!*\n\n"
                        f"*Symbol:* `{symbol}`\n"
                        f"*Action:* {'Long 📈' if result['signal'] == 'Buy' else 'Short 📉'}\n"
                        f"*Confidence:* {result['confidence']}%\n"
                        f"*Rating:* {'⭐' * result['stars']}\n"
                        f"*Pattern:* {result['pattern']}\n"
                        f"*Candlestick:* {result['candlestick']}\n"
                        f"*Suggested Holding:* {result['suggested_holding']}\n\n"
                        f"{risk_message}\n"
                        f"⚡ _No financial advice. Act smart!_"
                    )

                    await bot.send_message(chat_id=chat_id, text=signal_text, parse_mode="Markdown")
                    await asyncio.sleep(1.5)  # Tiny delay between messages

                except Exception as e:
                    await report_error(bot, chat_id, e, context_info=f"AutoSignal for {symbol}")
                    logger.error(f"[Auto Signal] Error with {symbol}: {e}")

            logger.info("[Auto Signal] Cycle complete. Sleeping before next check.")
            await asyncio.sleep(config.get("SIGNAL_CHECK_INTERVAL_SEC", 60))

        except Exception as e:
            logger.critical(f"[Auto Signal Loop] Critical Error: {e}")
            await report_error(bot, chat_id, e, context_info="Auto Signal Main Loop")
            await asyncio.sleep(60)
