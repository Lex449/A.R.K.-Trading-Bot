# bot/auto/auto_signal_loop.py

"""
A.R.K. Auto Signal Loop – Ultra Smart US Market Scanner 2025 Final Edition
Analyzes only during US trading hours, monitors system heartbeat, sends bilingual trading signals.
Built for: Maximum Stability, Minimal Downtime, Institutional Scalability.
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
    Core background loop that continuously analyzes market conditions
    and dispatches signals during active US market sessions.
    """

    logger.info("🚀 [AutoSignalLoop] Initializing ultra-stable signal scanner...")

    while RUNNING:
        try:
            # === Heartbeat Check ===
            await send_heartbeat(application)

            # === Connection Watchdog ===
            connection_ok = await check_connection()
            if not connection_ok:
                logger.warning("⚠️ [AutoSignalLoop] Connection unstable. Retrying in 30 seconds...")
                await asyncio.sleep(30)
                continue

            # === Market Session Check ===
            if not is_us_market_open():
                logger.info("⏳ [AutoSignalLoop] US Market currently closed. Pausing analysis.")
                await asyncio.sleep(120)
                continue

            # === Market Analysis ===
            logger.info("📈 [AutoSignalLoop] Running live market analysis...")
            analysis_results = await analyze_market()

            if analysis_results:
                for result in analysis_results:
                    try:
                        chat_id = int(config["TELEGRAM_CHAT_ID"])
                        lang = get_language(chat_id) or "en"

                        # Signal Text
                        signal_text = get_text("signal_detected", lang).format(
                            symbol=result["symbol"],
                            signal=result["combined_action"],
                            confidence=result["avg_confidence"],
                            rating=result["signal_category"]
                        )

                        await application.bot.send_message(
                            chat_id=chat_id,
                            text=signal_text,
                            parse_mode="Markdown"
                        )

                        logger.info(f"✅ [AutoSignalLoop] Signal sent: {result['symbol']} ({result['combined_action']})")

                    except Exception as signal_error:
                        logger.error(f"❌ [AutoSignalLoop] Signal dispatch failed: {signal_error}")

            else:
                logger.info("ℹ️ [AutoSignalLoop] No valid trading signals detected in this cycle.")

        except Exception as critical_error:
            logger.error(f"🔥 [AutoSignalLoop] Critical runtime error: {critical_error}")

        # Sleep until next scan
        await asyncio.sleep(config.get("SIGNAL_CHECK_INTERVAL_SEC", 60))

async def stop_auto_signal_loop():
    """
    Gracefully stops the auto signal loop.
    """
    global RUNNING
    RUNNING = False
    logger.info("🛑 [AutoSignalLoop] Signal loop termination initiated successfully.")
