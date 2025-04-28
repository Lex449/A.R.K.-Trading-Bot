"""
A.R.K. Ultra Auto Signal Loop – 2025 Hyper Premium Edition.
Boost Mode | Deep Confidence AI | Adaptive Trading Intelligence
"""

import asyncio
import logging
import time
from telegram import Bot
from bot.engine.analysis_engine import analyze_symbol
from bot.engine.move_alert_engine import detect_move_alert
from bot.engine.news_alert_engine import detect_breaking_news, format_breaking_news
from bot.engine.deep_confidence_engine import adjust_confidence  # << NEU
from bot.utils.ultra_signal_builder import build_ultra_signal
from bot.utils.session_tracker import update_session_tracker
from bot.utils.error_reporter import report_error
from bot.utils.market_time import is_trading_day, is_trading_hours
from bot.utils.news_health_checker import check_finnhub_health
from bot.config.settings import get_settings
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)
config = get_settings()

async def auto_signal_loop():
    bot = Bot(token=config["BOT_TOKEN"])
    chat_id = int(config["TELEGRAM_CHAT_ID"])
    symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
    language = config.get("BOT_LANGUAGE", "en")

    max_api_calls_per_minute = 140
    signal_interval_sec = config.get("SIGNAL_CHECK_INTERVAL_SEC", 60)
    boost_interval_sec = 20  # Boost Interval
    boost_mode_active = False
    boost_mode_end_time = None

    calls_this_minute = 0
    minute_start_time = time.time()

    if not symbols:
        logger.error("❌ [AutoSignal] No symbols configured! Exiting.")
        return

    logger.info("🚀 [AutoSignal] Hyper Monitoring Activated...")

    last_news_check = None

    try:
        while True:
            # Reset API counter every minute
            if time.time() - minute_start_time >= 60:
                calls_this_minute = 0
                minute_start_time = time.time()

            # Check if Market is Open
            if not is_trading_day() or not is_trading_hours():
                logger.info("⏳ [Market] Closed. Sleeping 5 min.")
                await asyncio.sleep(300)
                continue

            await check_finnhub_health()

            logger.info(f"🔍 [Scan] Scanning {len(symbols)} symbols...")

            for symbol in symbols:
                try:
                    if calls_this_minute >= max_api_calls_per_minute:
                        logger.warning("⚠️ [API Limit] Max API calls reached. Cooling down 10s.")
                        await asyncio.sleep(10)
                        calls_this_minute = 0
                        minute_start_time = time.time()

                    result = await analyze_symbol(symbol)
                    calls_this_minute += 1

                    if not result:
                        continue

                    move_alert = await detect_move_alert(result.get("df"))
                    if move_alert:
                        await send_move_alert(bot, chat_id, symbol, move_alert, language)

                        if move_alert.get("move_percent", 0) >= 2.5:
                            boost_mode_active = True
                            boost_mode_end_time = time.time() + 300  # 5 Minuten Boost
                            logger.info(f"⚡ [BOOST] Boost Mode activated due to strong move in {symbol}.")

                    valid_patterns = [
                        p for p in result.get("patterns", [])
                        if "⭐" in p and p.count("⭐") >= 3
                    ]

                    # === Deep Learning Confidence Adjustment ===
                    raw_confidence = result.get("avg_confidence", 0)
                    confidence = adjust_confidence(raw_confidence)

                    if valid_patterns and confidence >= 58:
                        update_session_tracker(len(valid_patterns), confidence)

                        signal_message = build_ultra_signal(
                            symbol=symbol,
                            move=result.get("move"),
                            volume_spike=result.get("volume_spike"),
                            atr_breakout=result.get("atr_breakout"),
                            risk_reward=result.get("risk_reward"),
                            lang=language
                        )

                        if signal_message:
                            await bot.send_message(
                                chat_id=chat_id,
                                text=signal_message,
                                parse_mode="Markdown",
                                disable_web_page_preview=True
                            )
                            logger.info(f"✅ [Signal] Premium signal sent for {symbol} | Confidence: {confidence:.2f}%")

                    await asyncio.sleep(1.1)  # Respect Telegram Rate Limit

                except Exception as symbol_error:
                    logger.error(f"❌ [AutoSignal] Error for {symbol}: {symbol_error}")
                    await report_error(bot, chat_id, symbol_error, context_info=f"AutoSignal for {symbol}")

            # === Breaking News Check ===
            try:
                now = time.time()
                if last_news_check is None or (now - last_news_check) >= 300:
                    breaking_news = await detect_breaking_news()

                    if breaking_news:
                        news_message = await format_breaking_news(breaking_news, lang=language)

                        if news_message:
                            await bot.send_message(
                                chat_id=chat_id,
                                text=news_message,
                                parse_mode="Markdown",
                                disable_web_page_preview=True
                            )
                            logger.info("📰 [NewsAlert] Breaking News sent.")

                            boost_mode_active = True
                            boost_mode_end_time = time.time() + 300
                            logger.info("📰 [BOOST] Boost Mode activated after Breaking News.")

                    last_news_check = now

            except Exception as news_error:
                logger.error(f"⚠️ [NewsDetection] Error: {news_error}")
                await report_error(bot, chat_id, news_error, context_info="NewsDetection Failure")

            # Decide Sleep Interval
            sleep_time = boost_interval_sec if boost_mode_active and time.time() < boost_mode_end_time else signal_interval_sec

            if boost_mode_active and time.time() >= boost_mode_end_time:
                boost_mode_active = False
                logger.info("⚡ [BOOST] Boost Mode ended, normal cycle resumed.")

            logger.info(f"⏳ [AutoSignal] Cycle complete. Sleeping {sleep_time} seconds...")
            await asyncio.sleep(sleep_time)

    except Exception as loop_error:
        logger.critical(f"🔥 [AutoSignalLoop] Fatal crash: {loop_error}")
        await report_error(bot, chat_id, loop_error, context_info="AutoSignalLoop Fatal Crash")
        await asyncio.sleep(120)

async def send_move_alert(bot: Bot, chat_id: int, symbol: str, move_alert: dict, language: str = "en"):
    """
    Sends early/strong move alerts.
    """
    move_type = move_alert.get("type", "early")
    move_percent = move_alert.get("move_percent", 0.0)

    if language.lower() == "de":
        text = (
            f"🚨 *Starke Marktbewegung!*\n\n"
            f"*Symbol:* `{symbol}`\n"
            f"*Bewegung:* `{move_percent:.2f}%`\n"
            f"_A.R.K. erkennt Marktveränderungen in Echtzeit._"
        ) if move_type == "full" else (
            f"⚠️ *Frühe Bewegungswarnung*\n\n"
            f"*Symbol:* `{symbol}`\n"
            f"*Bewegung:* `{move_percent:.2f}%`\n"
            f"_A.R.K. überwacht den Markt kontinuierlich._"
        )
    else:
        text = (
            f"🚨 *Strong Market Move!*\n\n"
            f"*Symbol:* `{symbol}`\n"
            f"*Movement:* `{move_percent:.2f}%`\n"
            f"_A.R.K. detects market changes in real-time._"
        ) if move_type == "full" else (
            f"⚠️ *Early Move Warning*\n\n"
            f"*Symbol:* `{symbol}`\n"
            f"*Movement:* `{move_percent:.2f}%`\n"
            f"_Smart traders act before the herd._"
        )

    await bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
    logger.info(f"📈 [MoveAlert] {symbol} moved {move_percent:.2f}%")
