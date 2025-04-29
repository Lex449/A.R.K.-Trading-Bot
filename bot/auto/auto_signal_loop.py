# bot/auto/auto_signal_loop.py

"""
A.R.K. Auto Signal Loop – Real-Time Signal Scanner 2025.
Analyzes markets 24/7, monitors heartbeat, watchdogs connection, bilingual output.
"""

import asyncio
from bot.auto.heartbeat_manager import send_heartbeat
from bot.auto.connection_watchdog import check_connection
from bot.engine.analysis_engine import analyze_market
from bot.utils.logger import setup_logger
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.config.settings import get_settings

# Setup structured logger
logger = setup_logger(__name__)
config = get_settings()

# Signal Loop Control
RUNNING = True

async def auto_signal_loop(application):
    """
    Core background loop that continuously analyzes market conditions
    and sends real-time trade signals.
    """

    logger.info("🚀 [AutoSignalLoop] Starting auto signal loop...")

    while RUNNING:
        try:
            # Heartbeat pulse
            await send_heartbeat(application)

            # Connection watchdog
            connection_ok = await check_connection()
            if not connection_ok:
                logger.warning("⚠️ [AutoSignalLoop] Connection issue detected!")
                await asyncio.sleep(30)
                continue  # Skip this cycle if connection unstable

            # Perform Market Analysis
            logger.info("📈 [AutoSignalLoop] Performing live market analysis...")
            analysis_results = await analyze_market()

            if analysis_results:
                for result in analysis_results:
                    try:
                        chat_id = int(config["TELEGRAM_CHAT_ID"])
                        lang = get_language(chat_id) or "en"

                        # Build bilingual message
                        signal_text = get_text("signal_detected", lang).format(
                            symbol=result["symbol"],
                            signal=result["signal"],
                            confidence=result["confidence"],
                            rating=result["stars"]
                        )

                        await application.bot.send_message(
                            chat_id=chat_id,
                            text=signal_text,
                            parse_mode="Markdown"
                        )

                        logger.info(f"✅ [AutoSignalLoop] Signal sent: {result['symbol']} ({result['signal']})")

                    except Exception as e:
                        logger.error(f"❌ [AutoSignalLoop] Error sending signal: {e}")

            else:
                logger.info("ℹ️ [AutoSignalLoop] No strong signals detected this cycle.")

        except Exception as outer_error:
            logger.error(f"🔥 [AutoSignalLoop] Critical error: {outer_error}")

        await asyncio.sleep(config.get("AUTO_SIGNAL_INTERVAL", 60))  # Default: every 60 seconds

async def stop_auto_signal_loop():
    """
    Gracefully stops the auto signal loop.
    """
    global RUNNING
    RUNNING = False
    logger.info("🛑 [AutoSignalLoop] Stopping auto signal loop...")
