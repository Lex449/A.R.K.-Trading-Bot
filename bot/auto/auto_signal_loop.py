"""
A.R.K. Auto Signal Loop – Ultra Smart US Market Scanner 2025 Final Elite Edition
Analyzes only during US trading hours, monitors heartbeat, sends bilingual ultra signals.
Built for: Stability, Precision, Institutional Scalability.
"""

import asyncio
from bot.auto.heartbeat_manager import send_heartbeat
from bot.auto.connection_watchdog import check_connection
from bot.engine.analysis_engine import analyze_symbol
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
    during active US trading sessions and dispatches premium signals.
    """

    logger.info("🚀 [AutoSignalLoop] Launching ultra-stable auto signal loop...")

    symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])

    if not symbols:
        logger.error("❌ [AutoSignalLoop] No symbols configured for auto analysis.")
        return

    while RUNNING:
        try:
            # Heartbeat Pulse
            await send_heartbeat(application)

            # Connection Watchdog
            connection_ok = await check_connection()
            if not connection_ok:
                logger.warning("⚠️ [AutoSignalLoop] Connection unstable. Retrying after 30s...")
                await asyncio.sleep(30)
                continue

            # US Market Session Guard
            if not is_us_market_open():
                logger.info("⏳ [AutoSignalLoop] US Market closed. Sleeping...")
                await asyncio.sleep(120)
                continue

            logger.info("📈 [AutoSignalLoop] Performing live symbol analysis...")

            for symbol in symbols:
                try:
                    result = await analyze_symbol(symbol)

                    if result and result.get("combined_action") in ["Long 📈", "Short 📉"]:
                        chat_id = int(config["TELEGRAM_CHAT_ID"])
                        lang = get_language(chat_id) or "en"

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

                        logger.info(f"✅ [AutoSignalLoop] Signal dispatched: {result['symbol']} ({result['combined_action']})")

                except Exception as symbol_error:
                    logger.error(f"❌ [AutoSignalLoop] Error analyzing {symbol}: {symbol_error}")

            logger.info("✅ [AutoSignalLoop] Cycle completed. Sleeping until next scan.")

        except Exception as cycle_error:
            logger.error(f"🔥 [AutoSignalLoop] Critical loop error: {cycle_error}")

        await asyncio.sleep(config.get("SIGNAL_CHECK_INTERVAL_SEC", 60))

async def stop_auto_signal_loop():
    """
    Gracefully stops the auto signal loop.
    """
    global RUNNING
    RUNNING = False
    logger.info("🛑 [AutoSignalLoop] Auto signal loop stopped successfully.")
