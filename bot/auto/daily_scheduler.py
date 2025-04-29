# bot/auto/daily_scheduler.py

"""
A.R.K. Daily Analysis Scheduler – Premium Smart Scan System.
Full market deep analysis once per day.
"""

import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from telegram import Bot
from bot.engine.analysis_engine import analyze_symbol
from bot.utils.ultra_signal_builder import build_ultra_signal
from bot.utils.session_tracker import update_session_tracker
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings
from bot.utils.logger import setup_logger

# === Setup ===
logger = setup_logger(__name__)
config = get_settings()

# === Scheduler Instanz ===
daily_scheduler = AsyncIOScheduler()

def start_daily_analysis_scheduler(application, chat_id: int):
    """
    Schedules the full daily analysis scan at a fixed time every day.
    """
    try:
        daily_scheduler.remove_all_jobs()

        # Trigger um jeden Tag zur definierten Zeit zu scannen (z.B. 15:30 UTC = NYSE-Open)
        daily_scheduler.add_job(
            daily_analysis_job,
            trigger=CronTrigger(hour=15, minute=30),  # 15:30 UTC
            args=[application, chat_id],
            id=f"daily_analysis_{chat_id}",
            replace_existing=True,
            name=f"Daily Full Market Analysis for {chat_id}"
        )

        if not daily_scheduler.running:
            daily_scheduler.start()

        logger.info(f"✅ [DailyScheduler] Daily Analysis Job scheduled for chat_id {chat_id}.")

    except Exception as e:
        logger.error(f"❌ [DailyScheduler Error] Failed to start daily analysis scheduler: {e}")

async def daily_analysis_job(application, chat_id: int):
    """
    Executes a full market analysis and sends premium signals.
    """
    bot: Bot = application.bot
    symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
    language = config.get("BOT_LANGUAGE", "en")

    if not symbols:
        logger.warning("❌ [DailyAnalysis] No symbols configured. Aborting daily analysis.")
        return

    logger.info(f"📈 [DailyAnalysis] Starting full market scan for {len(symbols)} symbols.")
    await bot.send_message(chat_id=chat_id, text="📊 *Starting Full Daily Market Scan...*", parse_mode="Markdown")

    try:
        for symbol in symbols:
            try:
                result = await analyze_symbol(symbol)

                if not result:
                    logger.info(f"⏩ [DailyAnalysis] No data for {symbol}. Skipping.")
                    continue

                valid_patterns = [
                    p for p in result.get("patterns", [])
                    if "⭐" in p and p.count("⭐") >= 3
                ]

                confidence = result.get("avg_confidence", 0)

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
                        logger.info(f"✅ [DailyAnalysis] Signal sent for {symbol}")

                await asyncio.sleep(1.2)  # Spam-Schutz

            except Exception as symbol_error:
                logger.error(f"❌ [DailyAnalysis] Error with {symbol}: {symbol_error}")
                await report_error(bot, chat_id, symbol_error, context_info=f"DailyAnalysis Symbol {symbol}")

        await bot.send_message(chat_id=chat_id, text="✅ *Daily Market Scan Completed Successfully!*", parse_mode="Markdown")
        logger.info("✅ [DailyAnalysis] Full daily market scan completed.")

    except Exception as global_error:
        logger.critical(f"🔥 [DailyAnalysis Fatal Error] {global_error}")
        await report_error(bot, chat_id, global_error, context_info="DailyAnalysis Global Crash")
