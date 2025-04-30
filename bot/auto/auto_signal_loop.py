# bot/auto/auto_signal_loop.py

"""
A.R.K. Auto Signal Loop – Final Boss Edition 2025
Smart US Market Scanner mit Confidence-Schranke, Deep Logging und Signal-Visualisierung.

Made in Bali. Engineered with German Precision.
"""

import asyncio
import time
from math import floor
from bot.auto.heartbeat_manager import send_heartbeat
from bot.auto.connection_watchdog import check_connection
from bot.engine.analysis_engine import analyze_symbol
from bot.utils.logger import setup_logger
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.market_session_guard import is_us_market_open, minutes_until_market_open
from bot.utils.api_bridge import record_call, monitor as usage_monitor
from bot.config.settings import get_settings

logger = setup_logger(__name__)
config = get_settings()
RUNNING = True
MIN_CONFIDENCE = 50.0

def build_signal_bar(conf: float, bars: int = 20) -> str:
    filled = floor(conf / 100 * bars)
    return "█" * filled + "░" * (bars - filled)

async def auto_signal_loop(application):
    logger.info("🚀 [AutoSignalLoop] Final Boss Loop started.")
    symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
    chat_id = int(config.get("TELEGRAM_CHAT_ID", 0))

    if not symbols:
        logger.critical("❌ [AutoSignalLoop] No symbols configured.")
        return

    while RUNNING:
        try:
            await send_heartbeat(application)

            if not await check_connection():
                logger.warning("⚠️ Connection lost. Retry in 30s.")
                await asyncio.sleep(30)
                continue

            if not is_us_market_open() and minutes_until_market_open() > 30:
                logger.info("⏳ Market closed. Sleep 2min.")
                await asyncio.sleep(120)
                continue

            logger.info("📡 Analyzing all symbols...")

            for symbol in symbols:
                try:
                    start = time.perf_counter()
                    result = await analyze_symbol(symbol, chat_id=chat_id)
                    runtime = time.perf_counter() - start
                    record_call()

                    if not result:
                        logger.debug(f"⚠️ No data for {symbol}")
                        continue

                    action = result.get("combined_action", "Neutral ⚪")
                    confidence = result.get("avg_confidence", 0.0)
                    score = result.get("signal_score", 0)
                    rating = result.get("signal_category", "N/A")
                    price = result.get("last_price", "n/a")

                    if action not in ["Long 📈", "Short 📉"] or confidence < MIN_CONFIDENCE:
                        logger.debug(f"⏭️ {symbol} skipped – Action: {action}, Confidence: {confidence:.1f}%")
                        continue

                    bar = build_signal_bar(confidence)
                    runtime_tag = f"⚙️ {runtime:.2f}s"
                    total = usage_monitor.get_call_count()
                    avg = usage_monitor.get_average_confidence()

                    lang = get_language(chat_id) or "en"
                    text = (
                        f"📡 *A.R.K. Live Signal!*\n\n"
                        f"*Symbol:* `{symbol}`\n"
                        f"*Direction:* {action}\n"
                        f"*Confidence:* `{confidence:.1f}%`\n"
                        f"*Signal Score:* `{score}/100`\n"
                        f"*Rating:* {rating}\n"
                        f"*Price:* `${price}`\n"
                        f"*Signal Bar:* [{bar}]\n"
                        f"{runtime_tag} – Signal #{total} today\n"
                        f"_Ø Confidence: {avg:.1f}%_\n\n"
                        f"_Markets move fast. Be precise. Be ready._"
                    )

                    await application.bot.send_message(
                        chat_id=chat_id,
                        text=text,
                        parse_mode="Markdown",
                        disable_web_page_preview=True
                    )

                    logger.info(f"✅ Signal sent: {symbol} ({action})")

                except Exception as e:
                    logger.exception(f"❌ [AutoSignalLoop] Error on {symbol}: {e}")

            logger.info("✅ [AutoSignalLoop] Cycle done. Sleeping...")

        except Exception as e:
            logger.exception(f"🔥 [AutoSignalLoop] Loop crashed: {e}")

        await asyncio.sleep(config.get("SIGNAL_CHECK_INTERVAL_SEC", 60))

async def stop_auto_signal_loop():
    global RUNNING
    RUNNING = False
    logger.info("🛑 [AutoSignalLoop] Stopped.")
