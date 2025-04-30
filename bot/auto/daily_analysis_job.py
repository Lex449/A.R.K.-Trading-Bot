"""
A.R.K. Daily Ultra Market Analysis – Premium Masterclass.
Performs elite signal scan with pattern validation, risk logic, trend synergy, and full session integration.
Made in Bali. Engineered with German Precision.
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

# Setup logger and config
logger = setup_logger(__name__)
config = get_settings()

bot_token = config["TELEGRAM_TOKEN"]
chat_id = int(config["TELEGRAM_CHAT_ID"])
symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
language = config.get("BOT_LANGUAGE", "en")

async def daily_analysis_job(context: ContextTypes.DEFAULT_TYPE = None):
    """
    Executes a full market scan once daily and sends only high-quality trade alerts.
    """
    bot = Bot(token=bot_token)

    logger.info("🚀 [DailyAnalysis] Starting full market analysis...")

    if not symbols:
        logger.error("❌ [DailyAnalysis] No symbols configured. Scan aborted.")
        return

    try:
        await bot.send_message(
            chat_id=chat_id,
            text="📊 *Daily Ultra Market Scan started...*\n_Only strongest signals will be shown._",
            parse_mode="Markdown"
        )

        for symbol in symbols:
            try:
                result = await analyze_symbol(symbol)

                if not result:
                    logger.warning(f"⚠️ [DailyAnalysis] No result for {symbol}. Skipping.")
                    continue

                patterns = result.get("patterns", [])
                confidence = result.get("avg_confidence", 0.0)

                valid_patterns = [p for p in patterns if "⭐" in p and p.count("⭐") >= 3]

                if not valid_patterns or confidence < 58:
                    logger.info(f"ℹ️ [DailyAnalysis] {symbol}: Skipped (Confidence: {confidence:.1f}%)")
                    continue

                # Track session metrics
                update_session_tracker(valid_patterns_count=len(valid_patterns), avg_confidence=confidence)

                # Build ultra signal message
                signal_message = build_ultra_signal(
                    symbol=symbol,
                    move=result.get("combined_action", "Unknown"),
                    volume_spike=result.get("volume_info", {}).get("volume_increase_percent", 0.0),
                    atr_breakout=result.get("trend_info", {}).get("slope", 0.0),
                    risk_reward=result.get("risk_reward_info", {}).get("risk_reward_ratio", "–"),
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

                await asyncio.sleep(1.2)  # Rate limit protection

            except Exception as symbol_error:
                logger.error(f"❌ [DailyAnalysis] Error on {symbol}: {symbol_error}")
                await report_error(bot, chat_id, symbol_error, context_info=f"Daily Analysis {symbol}")

        await bot.send_message(
            chat_id=chat_id,
            text="✅ *Daily scan complete.*\n_Stay sharp. Stay disciplined._",
            parse_mode="Markdown"
        )
        logger.info("✅ [DailyAnalysis] Scan completed successfully.")

    except Exception as e:
        logger.critical(f"🔥 [DailyAnalysis Crash] {e}")
        await report_error(bot, chat_id, e, context_info="Daily Market Analysis – Global Crash")
