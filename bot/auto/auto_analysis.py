# bot/auto/daily_analysis_job.py

"""
A.R.K. Daily Ultra Market Analysis – Premium Masterclass.
Full symbol scan with intelligent filtering, scoring, trend boosting.
"""

import asyncio
import logging
from telegram import Bot
from telegram.ext import ContextTypes
from bot.engine.analysis_engine import analyze_symbol
from bot.utils.ultra_signal_builder import build_ultra_signal
from bot.utils.session_tracker import update_session_tracker
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings
from bot.utils.logger import setup_logger

# Logger Setup
logger = setup_logger(__name__)

# Config Load
config = get_settings()

async def daily_analysis_job(context: ContextTypes.DEFAULT_TYPE):
    """
    Daily full-market scan for high probability trades.
    Intelligent premium signal extraction.
    """

    bot: Bot = context.bot
    chat_id = int(config["TELEGRAM_CHAT_ID"])
    symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
    language = config.get("BOT_LANGUAGE", "en")

    if not symbols:
        logger.error("❌ [DailyAnalysis] No symbols configured. Aborting daily scan.")
        return

    logger.info("🚀 [DailyAnalysis] Starting full market daily scan...")
    await bot.send_message(chat_id=chat_id, text="📊 *Starting full daily market scan...*", parse_mode="Markdown")

    try:
        for symbol in symbols:
            try:
                result = await analyze_symbol(symbol)

                if not result:
                    logger.warning(f"[DailyAnalysis] No analysis data for {symbol}. Skipping.")
                    continue

                valid_patterns = [
                    p for p in result.get("patterns", [])
                    if "⭐" in p and p.count("⭐") >= 3
                ]

                avg_confidence = result.get("avg_confidence", 0)

                if not valid_patterns or avg_confidence < 58:
                    logger.info(f"[DailyAnalysis] {symbol} → No valid patterns or low confidence ({avg_confidence:.1f}%). Skipping.")
                    continue

                # Session Tracker Update
                update_session_tracker(len(valid_patterns), avg_confidence)

                # Build Signal
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
                    logger.info(f"✅ [DailyAnalysis] High-Quality Signal sent for {symbol}")

                await asyncio.sleep(1.2)  # API Spam Protection

            except Exception as symbol_error:
                logger.error(f"❌ [DailyAnalysis] Error processing {symbol}: {symbol_error}")
                await report_error(bot, chat_id, symbol_error, context_info=f"Daily Analysis {symbol}")

        await bot.send_message(chat_id=chat_id, text="✅ *Daily scan completed successfully!*", parse_mode="Markdown")
        logger.info("✅ [DailyAnalysis] Full daily market analysis completed.")

    except Exception as e:
        logger.critical(f"🔥 [DailyAnalysis Fatal Error] {e}")
        await report_error(bot, chat_id, e, context_info="Daily Analysis Global Crash")
