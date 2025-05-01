"""
A.R.K. Auto Signal Loop – Final Boss Ultra Premium Build 2025  
Smart Parallel US Market Scanner mit Deep Diagnostics, Rejection Insights und Live Signal Protocols.  
Built to uncover every failure point – you never miss a trade again.  
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

# === Setup ===
logger = setup_logger(__name__)
config = get_settings()
RUNNING = True
MIN_CONFIDENCE = 50.0

def build_signal_bar(conf: float, bars: int = 20) -> str:
    filled = floor(conf / 100 * bars)
    return "█" * filled + "░" * (bars - filled)

async def auto_signal_loop(application):
    logger.info("🚀 [AutoSignalLoop] Ultra Loop gestartet.")

    symbols_raw = config.get("AUTO_SIGNAL_SYMBOLS", "")
    symbols = [s.strip().upper() for s in symbols_raw.split(",") if s.strip()]
    chat_id = int(config.get("TELEGRAM_CHAT_ID", 0))
    interval = config.get("SIGNAL_CHECK_INTERVAL_SEC", 60)

    if not symbols:
        logger.critical("❌ [AutoSignalLoop] Keine Symbole gefunden. Check .env → AUTO_SIGNAL_SYMBOLS.")
        return

    logger.info(f"📊 [AutoSignalLoop] {len(symbols)} Symbole geladen: {symbols[:5]}...")

    notified = False

    while RUNNING:
        try:
            await send_heartbeat(application)

            if not await check_connection():
                logger.warning("⚠️ [AutoSignalLoop] Telegram-Verbindung gestört. Retry in 30s.")
                await asyncio.sleep(30)
                continue

            logger.info(f"📡 [AutoSignalLoop] Analyse-Zyklus gestartet: {len(symbols)} Symbole...")

            tasks = [analyze_and_dispatch(application, symbol, chat_id) for symbol in symbols]
            await asyncio.gather(*tasks)

            logger.info("✅ [AutoSignalLoop] Zyklus abgeschlossen. Pause beginnt...")

            # === Einmalige Aktivierungsbenachrichtigung ===
            if not notified:
                await application.bot.send_message(
                    chat_id=chat_id,
                    text="✅ *Auto Signal Loop aktiviert* – alle 60 Sekunden wird nun geprüft.\n\n_Silent Mode aktiv. Signale nur bei hoher Qualität._",
                    parse_mode="Markdown"
                )
                notified = True

        except Exception as e:
            logger.exception(f"🔥 [AutoSignalLoop] Totalabbruch: {e}")

        await asyncio.sleep(interval)

async def analyze_and_dispatch(application, symbol, chat_id):
    try:
        logger.debug(f"🔍 Beginne Analyse: {symbol}")
        start = time.perf_counter()
        result = await analyze_symbol(symbol, chat_id=chat_id)
        runtime = time.perf_counter() - start
        record_call(symbol)

        if result is None:
            logger.info(f"⚠️ [AutoSignalLoop] Kein verwertbares Signal: {symbol}")
            return

        action = result.get("combined_action", "Neutral ⚪")
        confidence = result.get("avg_confidence", 0.0)
        score = result.get("signal_score", 0)
        rating = result.get("signal_category", "N/A")
        price = result.get("last_price", "n/a")

        if action not in ["Long 📈", "Short 📉"]:
            logger.info(f"⛔ Kein Signal bei {symbol} → Action: {action}")
            return

        if confidence < MIN_CONFIDENCE:
            logger.info(f"⛔ Confidence zu niedrig für {symbol}: {confidence:.1f}%")
            return

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

        logger.info(f"✅ [AutoSignalLoop] Signal gesendet: {symbol} ({action})")

    except Exception as e:
        logger.exception(f"❌ Analysefehler bei {symbol}: {e}")

async def stop_auto_signal_loop():
    global RUNNING
    RUNNING = False
    logger.info("🛑 [AutoSignalLoop] Manuell gestoppt.")
