# bot/engine/auto_signal_loop.py

"""
A.R.K. Auto Signal Loop – Ultra Wall Street Surveillance.
Bugatti Pur Sport Version. No compromise. Full throttle precision.
"""

import asyncio
import logging
from telegram import Bot
from bot.engine.analysis_engine import analyze_symbol
from bot.engine.move_alert_engine import detect_move_alert
from bot.utils.ultra_signal_builder import build_ultra_signal
from bot.utils.session_tracker import update_session_tracker
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings
from bot.utils.market_time import is_trading_day, is_trading_hours

# Setup structured logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Load Configuration
config = get_settings()

async def auto_signal_loop(bot: Bot):
    """
    Runs the nonstop ultra-premium trading surveillance loop.
    Combines volatility, movement, ATR, and risk/reward detections into Bugatti-class signals.
    """

    chat_id = int(config["TELEGRAM_CHAT_ID"])
    logger.info("🚀 [Auto Signal Loop] Ultra-Premium Monitoring initialized...")

    try:
        symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
        signal_interval_sec = config.get("SIGNAL_CHECK_INTERVAL_SEC", 60)
        language = config.get("BOT_LANGUAGE", "en")

        if not symbols:
            logger.error("❌ [Auto Signal Loop] No symbols configured. Exiting loop.")
            return

        while True:
            # === Check Market State ===
            if not is_trading_day() or not is_trading_hours():
                logger.info("⏳ [Auto Signal Loop] Market closed or holiday. Sleeping 5 min.")
                await asyncio.sleep(300)
                continue

            logger.info(f"🔎 [Auto Signal Loop] Scanning {len(symbols)} symbols...")

            for symbol in symbols:
                try:
                    # Analyze Symbol
                    result = await analyze_symbol(symbol)
                    if not result:
                        continue

                    # Move Detection (early move)
                    move_alert = await detect_move_alert(result.get("df"))
                    if move_alert:
                        await send_move_alert(bot, chat_id, symbol, move_alert, language)

                    # Ultra Signal Build (only if valid pattern + strong confidence)
                    valid_patterns = [
                        p for p in result.get("patterns", [])
                        if "⭐" in p and p.count("⭐") >= 3
                    ]

                    if valid_patterns and result.get("avg_confidence", 0) >= 60:
                        update_session_tracker(len(valid_patterns), result.get("avg_confidence", 0))

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
                            logger.info(f"✅ [Auto Signal] Sent premium trading signal for {symbol}")

                    await asyncio.sleep(1.5)  # Respect Telegram rate limits

                except Exception as symbol_error:
                    logger.error(f"❌ [Auto Signal] Error for {symbol}: {symbol_error}")
                    await report_error(bot, chat_id, symbol_error, context_info=f"Auto Signal Symbol: {symbol}")

            logger.info("⏳ [Auto Signal Loop] Scan cycle completed. Sleeping before next cycle...")
            await asyncio.sleep(signal_interval_sec)

    except Exception as loop_error:
        logger.critical(f"🔥 [Auto Signal Loop] Fatal error: {loop_error}")
        await report_error(bot, chat_id, loop_error, context_info="Auto Signal Main Loop Failure")
        await asyncio.sleep(120)

async def send_move_alert(bot: Bot, chat_id: int, symbol: str, move_alert: dict, language: str = "en"):
    """
    Sends a market movement alert based on detected abnormal moves.
    """

    move_type = move_alert.get("type", "early")
    move_percent = move_alert.get("move_percent", 0.0)

    if language.lower() == "de":
        if move_type == "full":
            text = (
                f"🚨 *Starke Bewegung erkannt!*\n\n"
                f"*Symbol:* `{symbol}`\n"
                f"*Bewegung:* `{move_percent:.2f}%`\n"
                f"_A.R.K. überwacht die Märkte 24/7. Handeln mit Weitsicht._"
            )
        else:
            text = (
                f"⚠️ *Frühe Bewegungswarnung*\n\n"
                f"*Symbol:* `{symbol}`\n"
                f"*Bewegung:* `{move_percent:.2f}%`\n"
                f"_Schlaue Trader handeln, wenn andere zögern._"
            )
    else:
        if move_type == "full":
            text = (
                f"🚨 *Strong Move Detected!*\n\n"
                f"*Symbol:* `{symbol}`\n"
                f"*Movement:* `{move_percent:.2f}%`\n"
                f"_A.R.K. monitors markets 24/7. Prepare wisely._"
            )
        else:
            text = (
                f"⚠️ *Early Move Warning*\n\n"
                f"*Symbol:* `{symbol}`\n"
                f"*Movement:* `{move_percent:.2f}%`\n"
                f"_Smart traders act when others hesitate._"
            )

    await bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
    logger.info(f"📈 [Move Alert] {symbol} moved {move_percent:.2f}%")
