# bot/auto/auto_signal_loop.py

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
from bot.utils.logger import setup_logger

# Logger Setup
logger = setup_logger(__name__)

# Load Config
config = get_settings()

async def auto_signal_loop():
    """
    A.R.K. Ultra Auto Signal Loop – 2025 Hyper Premium Edition.
    Intelligent API Control | Priority Signals | Adaptive Market Boosting
    """

    bot = Bot(token=config["BOT_TOKEN"])
    chat_id = int(config["TELEGRAM_CHAT_ID"])
    symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
    language = config.get("BOT_LANGUAGE", "en")

    max_api_calls_per_minute = 140
    signal_interval_sec = config.get("SIGNAL_CHECK_INTERVAL_SEC", 60)
    calls_this_minute = 0
    minute_start_time = time.time()

    if not symbols:
        logger.error("❌ [AutoSignal] No symbols configured! Exiting.")
        return

    logger.info("🚀 [AutoSignal] Hyper Monitoring Activated...")

    last_news_check = None

    try:
        while True:
            if time.time() - minute_start_time >= 60:
                calls_this_minute = 0
                minute_start_time = time.time()

            # Check Market Open
            if not is_trading_day() or not is_trading_hours():
                logger.info("⏳ [Market] Closed. Sleeping 5 min.")
                await asyncio.sleep(300)
                continue

            await check_finnhub_health()

            logger.info(f"🔍 [Scan] Scanning {len(symbols)} symbols...")

            for symbol in symbols:
                try:
                    if calls_this_minute >= max_api_calls_per_minute:
                        logger.warning("⚠️ [API Limit] API Max Calls reached. Cooling down 10s.")
                        await asyncio.sleep(10)
                        calls_this_minute = 0
                        minute_start_time = time.time()

                    # Symbol Analysis
                    result = await analyze_symbol(symbol)
                    calls_this_minute += 1

                    if not result:
                        continue

                    move_alert = await detect_move_alert(result.get("df"))
                    if move_alert:
                        await send_move_alert(bot, chat_id, symbol, move_alert, language)

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
                            logger.info(f"✅ [Signal] Sent premium trading signal for {symbol}")

                    await asyncio.sleep(1.1)  # Telegram Rate Limit respect

                except Exception as symbol_error:
                    logger.error(f"❌ [AutoSignal] Error for {symbol}: {symbol_error}")
                    await report_error(bot, chat_id, symbol_error, context_info=f"AutoSignal {symbol}")

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
                    last_news_check = now

            except Exception as news_error:
                logger.error(f"⚠️ [NewsDetection] Error: {news_error}")
                await report_error(bot, chat_id, news_error, context_info="NewsDetection Failure")

            logger.info("⏳ [AutoSignal] Cycle complete. Sleeping...")
            await asyncio.sleep(signal_interval_sec)

    except Exception as loop_error:
        logger.critical(f"🔥 [AutoSignalLoop] Fatal crash: {loop_error}")
        await report_error(bot, chat_id, loop_error, context_info="AutoSignalLoop Fatal Crash")
        await asyncio.sleep(120)

async def send_move_alert(bot: Bot, chat_id: int, symbol: str, move_alert: dict, language: str = "en"):
    """
    Sends market movement alerts.
    """
    move_type = move_alert.get("type", "early")
    move_percent = move_alert.get("move_percent", 0.0)

    if language.lower() == "de":
        text = (
            f"🚨 *Starke Marktbewegung!*\n\n"
            f"*Symbol:* `{symbol}`\n"
            f"*Bewegung:* `{move_percent:.2f}%`\n"
            f"_A.R.K. überwacht die Märkte in Echtzeit._"
        ) if move_type == "full" else (
            f"⚠️ *Frühe Bewegungswarnung*\n\n"
            f"*Symbol:* `{symbol}`\n"
            f"*Bewegung:* `{move_percent:.2f}%`\n"
            f"_Frühe Trendumkehr möglich._"
        )
    else:
        text = (
            f"🚨 *Strong Market Move!*\n\n"
            f"*Symbol:* `{symbol}`\n"
            f"*Movement:* `{move_percent:.2f}%`\n"
            f"_A.R.K. is monitoring markets real-time._"
        ) if move_type == "full" else (
            f"⚠️ *Early Move Warning*\n\n"
            f"*Symbol:* `{symbol}`\n"
            f"*Movement:* `{move_percent:.2f}%`\n"
            f"_Early trend shift possible._"
        )

    await bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
    logger.info(f"📈 [MoveAlert] {symbol} moved {move_percent:.2f}%")
