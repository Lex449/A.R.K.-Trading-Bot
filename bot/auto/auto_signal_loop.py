"""
A.R.K. Auto Signal Loop – FINAL NASA EDITION 2025  
24/7 Scanner mit API-Tracking, Confidenzfilter, Signal-Dispatch, 60s Loop.
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
from bot.utils.api_bridge import record_call, monitor as usage_monitor
from bot.config.settings import get_settings

logger = setup_logger(__name__)
config = get_settings()
RUNNING = True
MIN_CONFIDENCE = 60.0

def build_signal_bar(conf: float, bars: int = 20) -> str:
    filled = floor(conf / 100 * bars)
    return "█" * filled + "░" * (bars - filled)

async def auto_signal_loop(application):
    logger.info("🚀 [AutoSignalLoop] Loop started.")

    symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
    chat_id = int(config.get("TELEGRAM_CHAT_ID", 0))
    interval = config.get("SIGNAL_CHECK_INTERVAL_SEC", 60)

    if not symbols:
        logger.critical("❌ [AutoSignalLoop] No symbols found in .env")
        return

    while RUNNING:
        try:
            await send_heartbeat(application)

            if not await check_connection():
                logger.warning("⚠️ [AutoSignalLoop] Telegram disconnected. Retrying in 30s...")
                await asyncio.sleep(30)
                continue

            for symbol in symbols:
                try:
                    logger.debug(f"🔍 Analyzing {symbol}...")
                    start = time.perf_counter()
                    result = await analyze_symbol(symbol, chat_id=chat_id, silent=True)
                    duration = time.perf_counter() - start

                    record_call(symbol)

                    if not result:
                        logger.info(f"⛔ No valid result for {symbol}")
                        continue

                    action = result.get("combined_action", "Neutral ⚪")
                    confidence = result.get("avg_confidence", 0.0)

                    if action not in ["Long 📈", "Short 📉"] or confidence < MIN_CONFIDENCE:
                        continue

                    lang = get_language(chat_id) or "en"
                    score = result.get("signal_score", 0)
                    rating = result.get("signal_category", "N/A")
                    price = result.get("last_price", "n/a")
                    bar = build_signal_bar(confidence)
                    runtime = f"{duration:.2f}s"
                    total = usage_monitor.get_call_count()
                    avg = usage_monitor.get_average_confidence()

                    text = (
                        f"📡 *A.R.K. Live Signal!*\n\n"
                        f"*Symbol:* `{symbol}`\n"
                        f"*Direction:* {action}\n"
                        f"*Confidence:* `{confidence:.1f}%`\n"
                        f"*Signal Score:* `{score}/100`\n"
                        f"*Rating:* {rating}\n"
                        f"*Price:* `${price}`\n"
                        f"*Signal Bar:* [{bar}]\n"
                        f"⚙️ Runtime: {runtime} – Signal #{total} today\n"
                        f"_Ø Confidence: {avg:.1f}%_\n\n"
                        f"_Market is moving. Are you ready?_"
                    )

                    await application.bot.send_message(
                        chat_id=chat_id,
                        text=text,
                        parse_mode="Markdown",
                        disable_web_page_preview=True
                    )

                    logger.info(f"✅ Signal sent for {symbol} ({action})")

                except Exception as symbol_error:
                    logger.error(f"❌ Error analyzing {symbol}: {symbol_error}")

            logger.info("✅ Cycle complete. Sleeping...")
            await asyncio.sleep(interval)

        except Exception as e:
            logger.critical(f"🔥 Fatal loop error: {e}")
            await asyncio.sleep(60)

async def stop_auto_signal_loop():
    global RUNNING
    RUNNING = False
    logger.info("🛑 [AutoSignalLoop] Stopped manually.")
