"""
A.R.K. Ultra Auto Signal Loop – Hyper Premium Engine 2025.
Fully Boosted, AI-Tuned, News-Integrated, Crash-Protected.
"""

import asyncio
import logging
import time
from telegram import Bot
from bot.engine.analysis_engine import analyze_symbol
from bot.engine.move_alert_engine import detect_move_alert
from bot.engine.news_alert_engine import detect_breaking_news, format_breaking_news
from bot.engine.deep_confidence_engine import adjust_confidence
from bot.utils.ultra_signal_builder import build_ultra_signal
from bot.utils.session_tracker import update_session_tracker
from bot.utils.error_reporter import report_error
from bot.utils.market_time import is_trading_day, is_trading_hours
from bot.utils.news_health_checker import check_finnhub_health
from bot.config.settings import get_settings
from bot.utils.logger import setup_logger

# === Load Watchdog safely without direct circular import ===
import bot.auto.watchdog_state as watchdog_state

# Setup Logger
logger = setup_logger(__name__)
config = get_settings()

async def auto_signal_loop():
    bot = Bot(token=config["BOT_TOKEN"])
    chat_id = int(config["TELEGRAM_CHAT_ID"])
    symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
    lang = config.get("BOT_LANGUAGE", "en")

    max_api_calls = 140
    signal_interval = config.get("SIGNAL_CHECK_INTERVAL_SEC", 60)
    boost_interval = 20
    boost_mode_active = False
    boost_end_time = None

    calls = 0
    start_minute = time.time()

    if not symbols:
        logger.error("❌ [AutoSignal] No symbols configured! Exiting...")
        return

    logger.info("🚀 [AutoSignal] Ultra Monitoring Activated.")

    last_news_check = None

    try:
        while True:
            # === Refresh Watchdog Heartbeat ===
            watchdog_state.refresh_watchdog()

            now = time.time()

            if now - start_minute >= 60:
                calls = 0
                start_minute = now

            if not is_trading_day() or not is_trading_hours():
                logger.info("⏳ [Market] Closed. Sleeping 5 min.")
                await asyncio.sleep(300)
                continue

            await check_finnhub_health()

            logger.info(f"🔍 [Scan] Scanning {len(symbols)} symbols...")

            for symbol in symbols:
                try:
                    if calls >= max_api_calls:
                        logger.warning("⚠️ [API] Max API calls hit. Cooling down...")
                        await asyncio.sleep(10)
                        calls = 0
                        start_minute = time.time()

                    result = await analyze_symbol(symbol)
                    calls += 1

                    if not result:
                        continue

                    move_alert = await detect_move_alert(result.get("df"))
                    if move_alert:
                        await send_move_alert(bot, chat_id, symbol, move_alert, lang)

                        if move_alert.get("move_percent", 0) >= 2.5:
                            boost_mode_active = True
                            boost_end_time = now + 300
                            logger.info(f"⚡ [BOOST] Boost activated by move in {symbol}")

                    valid_patterns = [
                        p for p in result.get("patterns", [])
                        if "⭐" in p and p.count("⭐") >= 3
                    ]

                    raw_confidence = result.get("avg_confidence", 0)
                    confidence = adjust_confidence(raw_confidence)

                    if valid_patterns and confidence >= 58:
                        update_session_tracker(len(valid_patterns), confidence)

                        message = build_ultra_signal(
                            symbol=symbol,
                            move=result.get("move"),
                            volume_spike=result.get("volume_spike"),
                            atr_breakout=result.get("atr_breakout"),
                            risk_reward=result.get("risk_reward"),
                            lang=lang
                        )

                        if message:
                            await bot.send_message(
                                chat_id=chat_id,
                                text=message,
                                parse_mode="Markdown",
                                disable_web_page_preview=True
                            )
                            logger.info(f"✅ [Signal] Signal sent for {symbol} | Confidence {confidence:.1f}%")

                    await asyncio.sleep(1.1)

                except Exception as e_symbol:
                    logger.error(f"❌ [AutoSignal] Error for {symbol}: {e_symbol}")
                    await report_error(bot, chat_id, e_symbol, context_info=f"AutoSignal Symbol Error: {symbol}")

            # === Breaking News Detection ===
            try:
                if last_news_check is None or now - last_news_check >= 300:
                    news_list = await detect_breaking_news()
                    if news_list:
                        news_message = await format_breaking_news(news_list, lang)
                        if news_message:
                            await bot.send_message(
                                chat_id=chat_id,
                                text=news_message,
                                parse_mode="Markdown",
                                disable_web_page_preview=True
                            )
                            logger.info("📰 [News] Breaking News sent.")

                            boost_mode_active = True
                            boost_end_time = time.time() + 300

                    last_news_check = now

            except Exception as e_news:
                logger.error(f"❌ [NewsDetection] Error: {e_news}")
                await report_error(bot, chat_id, e_news, context_info="Breaking News Detection Failure")

            # === Sleep Control ===
            sleep_interval = boost_interval if boost_mode_active and time.time() < boost_end_time else signal_interval

            if boost_mode_active and time.time() >= boost_end_time:
                boost_mode_active = False
                logger.info("⚡ [BOOST] Boost Mode ended.")

            logger.info(f"⏳ [AutoSignal] Cycle complete. Sleeping {sleep_interval}s...")
            await asyncio.sleep(sleep_interval)

    except Exception as e_loop:
        logger.critical(f"🔥 [AutoSignalLoop] Fatal crash: {e_loop}")
        await report_error(bot, chat_id, e_loop, context_info="Fatal Crash in AutoSignalLoop")
        await asyncio.sleep(120)

async def send_move_alert(bot: Bot, chat_id: int, symbol: str, move_alert: dict, lang: str = "en"):
    move_type = move_alert.get("type", "early")
    move_percent = move_alert.get("move_percent", 0.0)

    if lang == "de":
        text = (
            f"🚨 *Starke Marktbewegung*\n\n"
            f"*Symbol:* `{symbol}`\n"
            f"*Bewegung:* `{move_percent:.2f}%`\n"
            f"_A.R.K. erkennt Veränderungen sofort._"
        ) if move_type == "full" else (
            f"⚠️ *Frühe Marktbewegung*\n\n"
            f"*Symbol:* `{symbol}`\n"
            f"*Bewegung:* `{move_percent:.2f}%`\n"
            f"_Wachsamkeit führt zu Siegen._"
        )
    else:
        text = (
            f"🚨 *Strong Market Move*\n\n"
            f"*Symbol:* `{symbol}`\n"
            f"*Movement:* `{move_percent:.2f}%`\n"
            f"_A.R.K. detects real shifts instantly._"
        ) if move_type == "full" else (
            f"⚠️ *Early Market Move*\n\n"
            f"*Symbol:* `{symbol}`\n"
            f"*Movement:* `{move_percent:.2f}%`\n"
            f"_First movers take the prize._"
        )

    await bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
    logger.info(f"📈 [MoveAlert] {symbol} moved {move_percent:.2f}%")
