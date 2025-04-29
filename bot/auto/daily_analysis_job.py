"""
A.R.K. Daily Ultra Market Analysis – Premium Masterclass.
Full intelligent symbol scan, trend boosting, signal optimization.
"""

import asyncio
from telegram import Bot
from telegram.ext import ContextTypes
from bot.engine.analysis_engine import analyze_symbol
from bot.utils.ultra_signal_builder import build_ultra_signal
from bot.utils.session_tracker import update_session_tracker
from bot.utils.error_reporter import report_error
from bot.utils.logger import setup_logger
from bot.config.settings import get_settings

# Setup
logger = setup_logger(__name__)
config = get_settings()

bot_token = config["TELEGRAM_TOKEN"]
chat_id = int(config["TELEGRAM_CHAT_ID"])
symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
language = config.get("BOT_LANGUAGE", "en")

async def daily_analysis_job(context: ContextTypes.DEFAULT_TYPE = None):
    """
    Daily full-market scan for highest probability setups.
    """

    bot = Bot(token=bot_token)

    logger.info("🚀 [DailyAnalysis] Initiating daily full market analysis...")

    if not symbols:
        logger.error("❌ [DailyAnalysis] No symbols configured. Aborting scan.")
        return

    try:
        await bot.send_message(chat_id=chat_id, text="📊 *Starting daily ultra scan...*", parse_mode="Markdown")

        for symbol in symbols:
            try:
                result = await analyze_symbol(symbol)

                if not result:
                    logger.warning(f"⚠️ [DailyAnalysis] No analysis data for {symbol}. Skipping.")
                    continue

                valid_patterns = [
                    p for p in result.get("patterns", [])
                    if "⭐" in p and p.count("⭐") >= 3
                ]
                avg_confidence = result.get("avg_confidence", 0)

                if not valid_patterns or avg_confidence < 58:
                    logger.info(f"ℹ️ [DailyAnalysis] {symbol}: Weak setup ({avg_confidence:.1f}%). Skipping.")
                    continue

                # Update session tracker
                update_session_tracker(
                    signal_count=len(valid_patterns),
                    average_confidence=avg_confidence
                )

                # Build and send ultra signal
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
                    logger.info(f"✅ [DailyAnalysis] High-quality signal sent for {symbol}")

                await asyncio.sleep(1.2)  # API Rate Limit Protection

            except Exception as symbol_error:
                logger.error(f"❌ [DailyAnalysis] Error analyzing {symbol}: {symbol_error}")
                await report_error(bot, chat_id, symbol_error, context_info=f"Daily Analysis {symbol}")

        await bot.send_message(chat_id=chat_id, text="✅ *Daily scan completed successfully!*", parse_mode="Markdown")
        logger.info("✅ [DailyAnalysis] Daily full-market scan complete.")

    except Exception as e:
        logger.critical(f"🔥 [DailyAnalysis Fatal Crash] {e}")
        await report_error(bot, chat_id, e, context_info="Daily Analysis Global Error")
