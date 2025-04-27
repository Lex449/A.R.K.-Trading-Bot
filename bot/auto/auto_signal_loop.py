"""
A.R.K. Auto Signal Loop – Non-Stop Wall Street Surveillance.
Built for perfection: Signals, Move Alerts, Smart Pause handling.
"""

import asyncio
import logging
from telegram import Bot
from bot.engine.analysis_engine import analyze_symbol
from bot.engine.move_alert_engine import detect_move_alert
from bot.utils.signal_builder import build_signal_message
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
    Continuously monitors the markets and sends trading signals and move alerts.
    """
    chat_id = int(config["TELEGRAM_CHAT_ID"])
    logger.info("🚀 [Auto Signal] Ultra-Loop started. 24/7 Monitoring initiated...")

    try:
        symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
        signal_interval_sec = config.get("SIGNAL_CHECK_INTERVAL_SEC", 60)

        if not symbols:
            logger.error("❌ [Auto Signal] No trading symbols configured.")
            return

        while True:
            # === Marktzeit prüfen ===
            if not is_trading_day() or not is_trading_hours():
                logger.info("⏳ [Auto Signal] Market closed or holiday. Sleeping 5 min.")
                await asyncio.sleep(300)
                continue

            logger.info(f"🔎 [Auto Signal] Scanning {len(symbols)} symbols...")

            for symbol in symbols:
                try:
                    # Analyse Symbol
                    result = await analyze_symbol(symbol)

                    if not result:
                        continue

                    # Move Detection
                    move_alert = await detect_move_alert(result.get("df"))
                    if move_alert:
                        await send_move_alert(bot, chat_id, symbol, move_alert)

                    # Signal Detection
                    valid_patterns = [p for p in result.get("patterns", []) if "⭐" in p and p.count("⭐") >= 3]

                    if valid_patterns:
                        update_session_tracker(len(valid_patterns), result.get("avg_confidence", 0))
                        signal_message = build_signal_message(
                            symbol=symbol,
                            patterns=valid_patterns,
                            combined_action=result.get("combined_action", "Neutral ⚪"),
                            avg_confidence=result.get("avg_confidence", 0),
                            indicator_score=result.get("indicator_score", 0),
                            trend_direction=result.get("trend_direction", "Neutral ⚪")
                        )

                        await bot.send_message(
                            chat_id=chat_id,
                            text=signal_message,
                            parse_mode="Markdown",
                            disable_web_page_preview=True
                        )
                        logger.info(f"✅ [Auto Signal] Signal sent for {symbol}.")

                    await asyncio.sleep(1.5)  # Kleine Pause zwischen Symbolen

                except Exception as symbol_error:
                    logger.error(f"❌ [Auto Signal] Error with symbol {symbol}: {symbol_error}")
                    await report_error(bot, chat_id, symbol_error, context_info=f"Auto Signal Error – {symbol}")

            logger.info("⏳ [Auto Signal] Cycle complete. Sleeping...")
            await asyncio.sleep(signal_interval_sec)

    except Exception as loop_error:
        logger.critical(f"🔥 [Auto Signal] Fatal error: {loop_error}")
        await report_error(bot, chat_id, loop_error, context_info="Auto Signal Main Loop Failure")
        await asyncio.sleep(120)

async def send_move_alert(bot: Bot, chat_id: int, symbol: str, move_alert: dict):
    """
    Sends a market movement alert based on detection.
    """
    move_type = move_alert["type"]
    move_percent = move_alert["move_percent"]

    if move_type == "full":
        text = (
            f"🚨 *Strong Move Alert!*\n\n"
            f"*Symbol:* `{symbol}`\n"
            f"*Movement:* `{move_percent:.2f}%`\n"
            f"_ARK monitors markets 24/7._"
        )
    else:
        text = (
            f"⚠️ *Early Move Detection*\n\n"
            f"*Symbol:* `{symbol}`\n"
            f"*Movement:* `{move_percent:.2f}%`\n"
            f"_Stay sharp. Stay ready._"
        )

    await bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown")
    logger.info(f"📈 [Move Alert] {symbol} moved {move_percent:.2f}%")
