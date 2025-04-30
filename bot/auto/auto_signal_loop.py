"""
A.R.K. Auto Signal Loop – Final Boss Edition 2025
Smart US Market Scanner mit Confidence-Schranke, Deep Logging, und dynamischer Signal-Verstärkung.

Optimiert für: Ultra-Stabilität, klare Trade-Signale, 24/7 Premium Monitoring.
Made in Bali. Engineered with German Precision.
"""

import asyncio
from bot.auto.heartbeat_manager import send_heartbeat
from bot.auto.connection_watchdog import check_connection
from bot.engine.analysis_engine import analyze_symbol
from bot.utils.logger import setup_logger
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.market_session_guard import is_us_market_open, minutes_until_market_open
from bot.utils.api_bridge import record_call
from bot.config.settings import get_settings

# === Setup ===
logger = setup_logger(__name__)
config = get_settings()

# === Control Flag ===
RUNNING = True

# === Thresholds ===
MIN_CONFIDENCE = 50.0

async def auto_signal_loop(application):
    logger.info("🚀 [AutoSignalLoop] Initiating Final Boss Auto Loop...")

    symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
    chat_id = int(config.get("TELEGRAM_CHAT_ID", 0))

    if not symbols:
        logger.critical("❌ [AutoSignalLoop] No symbols configured for AUTO_SIGNAL_SYMBOLS.")
        return

    while RUNNING:
        try:
            await send_heartbeat(application)

            if not await check_connection():
                logger.warning("⚠️ [AutoSignalLoop] Lost connection. Retrying in 30s.")
                await asyncio.sleep(30)
                continue

            if not is_us_market_open() and minutes_until_market_open() > 30:
                logger.info("⏳ [AutoSignalLoop] Market closed. Sleeping 2 min.")
                await asyncio.sleep(120)
                continue

            logger.info("📡 [AutoSignalLoop] Starting full symbol analysis...")

            for symbol in symbols:
                try:
                    result = await analyze_symbol(symbol, chat_id=chat_id)
                    record_call()

                    if not result:
                        logger.info(f"❌ [AutoSignalLoop] No result for {symbol}")
                        continue

                    action = result.get("combined_action", "Neutral ⚪")
                    confidence = result.get("avg_confidence", 0.0)
                    score = result.get("signal_score", 0)

                    logger.info(f"🔍 [AutoSignalLoop] {symbol} | Action: {action} | Confidence: {confidence:.1f}% | Score: {score}/100")

                    if action not in ["Long 📈", "Short 📉"] or confidence < MIN_CONFIDENCE:
                        logger.info(f"⚪ [AutoSignalLoop] Skipped – Confidence too low or neutral action.")
                        continue

                    lang = get_language(chat_id) or "en"
                    rating = result.get("signal_category", "N/A")
                    price = result.get("last_price", "n/a")

                    signal_text = (
                        f"📡 *A.R.K. Live Signal!*\n\n"
                        f"*Symbol:* `{symbol}`\n"
                        f"*Direction:* {action}\n"
                        f"*Confidence:* `{confidence:.1f}%`\n"
                        f"*Signal Score:* `{score}/100`\n"
                        f"*Rating:* {rating}\n"
                        f"*Price:* `${price}`\n\n"
                        f"_Markets move fast. Be precise. Be ready._"
                    )

                    await application.bot.send_message(
                        chat_id=chat_id,
                        text=signal_text,
                        parse_mode="Markdown",
                        disable_web_page_preview=True
                    )

                    logger.info(f"✅ [AutoSignalLoop] Signal sent: {symbol} ({action})")

                except Exception as symbol_error:
                    logger.error(f"❌ [AutoSignalLoop] Error while analyzing {symbol}: {symbol_error}")

            logger.info("✅ [AutoSignalLoop] Cycle complete. Cooling down...")

        except Exception as loop_error:
            logger.error(f"🔥 [AutoSignalLoop] Main loop crashed: {loop_error}")

        await asyncio.sleep(config.get("SIGNAL_CHECK_INTERVAL_SEC", 60))


async def stop_auto_signal_loop():
    global RUNNING
    RUNNING = False
    logger.info("🛑 [AutoSignalLoop] Stopped gracefully.")
