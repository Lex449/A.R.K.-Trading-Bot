# bot/auto/auto_signal_loop.py

"""
A.R.K. Auto Signal Loop – Ultra Premium Surveillance Mode.
Dynamic API Balancing, Signal Purification, Real-Time Early Trend Detection.
"""

import asyncio
import logging
import time
from telegram import Bot
from bot.engine.analysis_engine import analyze_symbol
from bot.engine.move_alert_engine import detect_move_alert
from bot.engine.news_alert_engine import detect_breaking_news, format_breaking_news
from bot.utils.ultra_signal_builder import build_ultra_signal
from bot.utils.session_tracker import update_session_tracker
from bot.utils.error_reporter import report_error
from bot.utils.market_time import is_trading_day, is_trading_hours
from bot.utils.news_health_checker import check_finnhub_health
from bot.config.settings import get_settings

# Logger Setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Load Config
config = get_settings()

async def auto_signal_loop(bot: Bot):
    """
    Masterclass Surveillance Engine.
    Adapts live to API capacity, trading hours and news events.
    """

    chat_id = int(config["TELEGRAM_CHAT_ID"])
    symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
    signal_interval_sec = config.get("SIGNAL_CHECK_INTERVAL_SEC", 60)
    language = config.get("BOT_LANGUAGE", "en")

    max_api_calls_per_minute = config.get("MAX_SIGNALS_PER_HOUR", 150) // 60
    calls_this_minute = 0
    minute_start_time = time.time()

    if not symbols:
        logger.error("❌ [AutoSignal] No symbols configured. Loop aborted.")
        return

    logger.info(f"🚀 [AutoSignal] Ultra-Precision Scan launched on {len(symbols)} symbols...")

    last_news_check = None

    try:
        while True:
            # Reset API Counter every minute
            if time.time() - minute_start_time >= 60:
                calls_this_minute = 0
                minute_start_time = time.time()

            # Market Check
            if not is_trading_day() or not is_trading_hours():
                logger.info("⏳ [Market] Closed or holiday detected. Sleeping 5 minutes.")
                await asyncio.sleep(300)
                continue

            await check_finnhub_health()

            logger.info(f"🔎 [Scan] Scanning {len(symbols)} symbols this cycle...")

            for symbol in symbols:
                try:
                    if calls_this_minute >= max_api_calls_per_minute:
                        logger.warning("⚠️ [API Throttle] Max API calls hit. Cooling down 10 seconds...")
                        await asyncio.sleep(10)
                        calls_this_minute = 0
                        minute_start_time = time.time()

                    # Analyze Symbol
                    result = await analyze_symbol(symbol)
                    calls_this_minute += 1

                    if not result:
                        continue

                    # Move Alert
                    move_alert = await detect_move_alert(result.get("df"))
                    if move_alert:
                        await send_move_alert(bot, chat_id, symbol, move_alert, language)

                    # Premium Signal Filter
                    valid_patterns = [
                        p for p in result.get("patterns", [])
                        if "⭐" in p and p.count("⭐") >= 3
                    ]

                    avg_confidence = result.get("avg_confidence", 0)

                    if valid_patterns and avg_confidence >= 58:
                        update_session_tracker(len(valid_patterns), avg_confidence)

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
                            logger.info(f"✅ [Signal] Sent high-confidence signal for {symbol}")

                    await asyncio.sleep(1.0)  # Telegram Anti-Spam Respect

                except Exception as symbol_error:
                    logger.error(f"❌ [SymbolScan] Error analyzing {symbol}: {symbol_error}")
                    await report_error(bot, chat_id, symbol_error, context_info=f"AutoSignal Symbol Scan: {symbol}")

            # Breaking News Check (every 5 min)
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
                            logger.info("📰 [BreakingNews] Sent to channel.")

                    last_news_check = now

            except Exception as news_error:
                logger.error(f"⚠️ [BreakingNews] Error: {news_error}")
                await report_error(bot, chat_id, news_error, context_info="Breaking News Handler")

            logger.info("⏳ [AutoSignal] Scan cycle complete. Sleeping before next cycle...")
            await asyncio.sleep(signal_interval_sec)

    except Exception as loop_error:
        logger.critical(f"🔥 [AutoSignal] Fatal crash in main loop: {loop_error}")
        await report_error(bot, chat_id, loop_error, context_info="AutoSignal Loop Failure")
        await asyncio.sleep(120)

async def send_move_alert(bot: Bot, chat_id: int, symbol: str, move_alert: dict, language: str = "en"):
    """
    Dispatches early or strong move alerts.
    """

    move_type = move_alert.get("type", "early")
    move_percent = move_alert.get("move_percent", 0.0)

    if language.lower() == "de":
        text = (
            f"🚨 *Starke Marktbewegung erkannt!*\n\n"
            f"*Symbol:* `{symbol}`\n"
            f"*Bewegung:* `{move_percent:.2f}%`\n"
            f"_A.R.K. überwacht die Märkte live._"
        ) if move_type == "full" else (
            f"⚠️ *Frühe Bewegungswarnung erkannt!*\n\n"
            f"*Symbol:* `{symbol}`\n"
            f"*Bewegung:* `{move_percent:.2f}%`\n"
            f"_Frühe Trends erkennen. Schnell agieren._"
        )
    else:
        text = (
            f"🚨 *Strong Move Detected!*\n\n"
            f"*Symbol:* `{symbol}`\n"
            f"*Movement:* `{move_percent:.2f}%`\n"
            f"_ARK monitors and reacts live._"
        ) if move_type == "full" else (
            f"⚠️ *Early Move Warning!*\n\n"
            f"*Symbol:* `{symbol}`\n"
            f"*Movement:* `{move_percent:.2f}%`\n"
            f"_Early action creates big wins._"
        )

    await bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
    logger.info(f"📈 [MoveAlert] {symbol} moved {move_percent:.2f}%")
