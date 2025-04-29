"""
A.R.K. Auto Signal Loop – Ultra Smart US Market Scanner 2025 Final.
Analyzes only during US trading hours, heartbeat monitor, bilingual signals, ultra risk control.
"""

import asyncio
from bot.auto.heartbeat_manager import send_heartbeat
from bot.auto.connection_watchdog import check_connection
from bot.engine.analysis_engine import analyze_market
from bot.utils.logger import setup_logger
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.market_session_guard import is_us_market_open
from bot.config.settings import get_settings

# Logger & Config
logger = setup_logger(__name__)
config = get_settings()

# Loop Control
RUNNING = True

async def auto_signal_loop(application):
    """
    Core background loop that continuously analyzes live markets
    during US session only and sends premium trading signals.
    """

    logger.info("🚀 [AutoSignalLoop] Preparing ultra market signal loop...")

    while RUNNING:
        try:
            # Heartbeat pulse
            await send_heartbeat(application)

            # Connection watchdog
            connection_ok = await check_connection()
            if not connection_ok:
                logger.warning("⚠️ [AutoSignalLoop] Connection unstable, retrying...")
                await asyncio.sleep(30)
                continue

            # === US Market Guard ===
            if not is_us_market_open():
                logger.info("⏳ [AutoSignalLoop] US Market closed. Analysis paused.")
                await asyncio.sleep(120)  # Sleep 2 minutes during closed hours
                continue

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
                logger.info("ℹ️ [AutoSignalLoop] No valid signals detected this cycle.")

        except Exception as outer_error:
            logger.error(f"🔥 [AutoSignalLoop] Critical auto loop error: {outer_error}")

        await asyncio.sleep(config.get("AUTO_SIGNAL_INTERVAL", 60))  # Cycle interval (default 60 sec)

async def stop_auto_signal_loop():
    """
    Gracefully stops the auto signal loop.
    """
    global RUNNING
    RUNNING = False
    logger.info("🛑 [AutoSignalLoop] Stopping auto signal loop gracefully...")
