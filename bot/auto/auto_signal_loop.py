# bot/auto/auto_signal_loop.py

"""
A.R.K. Ultra Auto Signal Loop – Hyper Premium Engine 2025.
Fully Boosted, AI-Tuned, Crash-Protected, 24/7 Stability Mode.
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
from bot.config.settings import get_settings
from bot.utils.logger import setup_logger

# === Setup ===
logger = setup_logger(__name__)
config = get_settings()

async def auto_signal_loop():
    """
    Main loop that scans markets, generates signals and monitors critical events.
    """
    bot = Bot(token=config["BOT_TOKEN"])
    chat_id = int(config["TELEGRAM_CHAT_ID"])
    symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
    language = config.get("BOT_LANGUAGE", "en")

    max_api_calls = 140
    signal_interval = config.get("SIGNAL_CHECK_INTERVAL_SEC", 60)
    boost_mode = False
    boost_end_time = None
    last_news_check = 0
    calls = 0
    start_time = time.time()

    if not symbols:
        logger.critical("❌ [AutoSignal] No symbols configured. Exiting AutoSignal Loop.")
        return

    logger.info("🚀 [AutoSignal] Ultra Monitoring System activated.")

    try:
        while True:
            now = time.time()

            # Reset API count every minute
            if now - start_time >= 60:
                calls = 0
                start_time = now

            if not is_trading_day() or not is_trading_hours():
                logger.info("⏳ [AutoSignal] Market closed. Sleeping 5 minutes...")
                await asyncio.sleep(300)
                continue

            logger.info(f"🔍 [AutoSignal] Scanning {len(symbols)} symbols...")

            for symbol in symbols:
                try:
                    if calls >= max_api_calls:
                        logger.warning("⚠️ [AutoSignal] API limit hit. Cooling down...")
                        await asyncio.sleep(10)
                        calls = 0
                        start_time = time.time()

                    result = await analyze_symbol(symbol)
                    calls += 1

                    if not result:
                        continue

                    move_alert = await detect_move_alert(result.get("df"))
                    if move_alert:
                        await send_move_alert(bot, chat_id, symbol, move_alert, language)

                        if move_alert.get("move_percent", 0) >= 2.5:
                            boost_mode = True
                            boost_end_time = now + 300  # Boost 5 Minuten
                            logger.info(f"⚡ [BOOST] Activated due to {symbol} move.")

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
                            lang=language
                        )

                        if message:
                            await bot.send_message(
                                chat_id=chat_id,
                                text=message,
                                parse_mode="Markdown",
                                disable_web_page_preview=True
                            )
                            logger.info(f"✅ [AutoSignal] Signal sent for {symbol} | Confidence {confidence:.1f}%")

                    await asyncio.sleep(1.1)

                except Exception as e:
                    logger.error(f"❌ [AutoSignal] Error processing {symbol}: {e}")
                    await report_error(bot, chat_id, e, context_info=f"AutoSignal Symbol Error: {symbol}")

            # === Breaking News Section ===
            try:
                if now - last_news_check >= 300:
                    news_list = await detect_breaking_news()
                    if news_list:
                        news_message = await format_breaking_news(news_list, language)
                        if news_message:
                            await bot.send_message(
                                chat_id=chat_id,
                                text=news_message,
                                parse_mode="Markdown",
                                disable_web_page_preview=True
                            )
                            logger.info("📰 [AutoSignal] Breaking news alert sent.")

                        boost_mode = True
                        boost_end_time = now + 300

                    last_news_check = now

            except Exception as news_error:
                logger.error(f"❌ [AutoSignal] News detection error: {news_error}")
                await report_error(bot, chat_id, news_error, context_info="Breaking News Error")

            # === Sleep Management ===
            sleep_interval = 20 if boost_mode and time.time() < boost_end_time else signal_interval

            if boost_mode and time.time() >= boost_end_time:
                boost_mode = False
                logger.info("⚡ [BOOST] Boost mode ended.")

            logger.info(f"⏳ [AutoSignal] Cycle complete. Sleeping {sleep_interval}s...")
            await asyncio.sleep(sleep_interval)

    except Exception as loop_error:
        logger.critical(f"🔥 [AutoSignal] Fatal Loop Crash: {loop_error}")
        await report_error(bot, chat_id, loop_error, context_info="Fatal AutoSignal Crash")
        await asyncio.sleep(120)  # Pause 2 Minuten bei schweren Fehlern

async def send_move_alert(bot: Bot, chat_id: int, symbol: str, move_alert: dict, lang: str = "en"):
    """
    Sends an alert if a strong market move is detected.
    """
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
            f"_Wachsamkeit führt zu Gewinnen._"
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
