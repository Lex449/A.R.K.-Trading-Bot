# bot/auto/auto_analysis.py

"""
A.R.K. Auto Market Scanner Ultra 2.0 – Premium Signal Generator.
Full-symbol dynamic scan with Ultra Signal integration and session tracking.
Made in Bali. Engineered with German Precision.
"""

import asyncio
from telegram import Bot
from telegram.ext import ContextTypes
from bot.engine.analysis_engine import analyze_market
from bot.utils.ultra_signal_builder import build_ultra_signal
from bot.utils.session_tracker import update_session_tracker
from bot.utils.error_reporter import report_error
from bot.utils.logger import setup_logger
from bot.config.settings import get_settings

# Structured Logger Setup
logger = setup_logger(__name__)
config = get_settings()

async def auto_analysis(context: ContextTypes.DEFAULT_TYPE):
    """
    Ultra dynamic auto-scan of configured symbols.
    Full signal building, session tracking, premium output.
    """

    bot: Bot = context.bot
    chat_id = int(config["TELEGRAM_CHAT_ID"])
    language = config.get("BOT_LANGUAGE", "en")
    symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])

    if not symbols:
        logger.error("❌ [AutoAnalysis] No symbols configured. Aborting auto scan.")
        return

    logger.info("🚀 [AutoAnalysis] Starting auto market scan...")
    await bot.send_message(chat_id=chat_id, text="🔍 *Starting auto market scan...*", parse_mode="Markdown")

    try:
        # Analyse all configured symbols at once
        results = await analyze_market(symbols)

        for result in results:
            try:
                symbol = result.get("symbol")
                move = result.get("move")
                patterns = result.get("patterns", [])
                confidence = result.get("avg_confidence", 0)

                if not symbol or confidence < 58:
                    logger.info(f"[AutoAnalysis] {symbol} → Low confidence ({confidence:.1f}%). Skipping.")
                    continue

                valid_patterns = [p for p in patterns if "⭐" in p and p.count("⭐") >= 3]
                if not valid_patterns:
                    logger.info(f"[AutoAnalysis] {symbol} → No valid patterns. Skipping.")
                    continue

                # Ultra Signal Message Build
                signal_message = build_ultra_signal(
                    symbol=symbol,
                    move=move,
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

                    logger.info(f"✅ [AutoAnalysis] Signal sent for {symbol}")

                    # Update Session Tracker
                    update_session_tracker(
                        signal_strength=len(valid_patterns),
                        avg_confidence=confidence
                    )

                await asyncio.sleep(1.0)  # API protection delay

            except Exception as symbol_error:
                logger.error(f"❌ [AutoAnalysis] Error sending signal for {symbol}: {symbol_error}")
                await report_error(bot, chat_id, symbol_error, context_info=f"AutoAnalysis {symbol}")

        await bot.send_message(chat_id=chat_id, text="✅ *Auto scan completed successfully!*", parse_mode="Markdown")
        logger.info("✅ [AutoAnalysis] Full auto market scan completed.")

    except Exception as e:
        logger.critical(f"🔥 [AutoAnalysis Fatal Error] {e}")
        await report_error(bot, chat_id, e, context_info="AutoAnalysis Global Crash")
