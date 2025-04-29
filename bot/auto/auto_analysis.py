# bot/auto/auto_analysis.py

"""
A.R.K. Auto Market Scanner Ultra 4.0 – Supreme Signal Builder.
Scans all configured symbols dynamically and dispatches ultra-premium trading signals.
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

# Setup structured logger
logger = setup_logger(__name__)
config = get_settings()

async def auto_analysis(context: ContextTypes.DEFAULT_TYPE):
    """
    Executes a full dynamic scan across all configured symbols.
    Builds ultra-premium signals, updates session statistics, and dispatches messages.
    """

    bot: Bot = context.bot
    chat_id = int(config["TELEGRAM_CHAT_ID"])
    language = config.get("BOT_LANGUAGE", "en")
    symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])

    if not symbols:
        logger.error("❌ [AutoAnalysis] No symbols configured. Aborting scan.")
        return

    logger.info("🚀 [AutoAnalysis] Starting full dynamic market scan...")
    await bot.send_message(chat_id=chat_id, text="🔍 *Starting Auto-Analysis...*", parse_mode="Markdown")

    try:
        # === Analyze All Configured Symbols ===
        analysis_results = await analyze_market(symbols)

        if not analysis_results:
            await bot.send_message(chat_id=chat_id, text="ℹ️ *No trading signals detected during scan.*", parse_mode="Markdown")
            logger.info("ℹ️ [AutoAnalysis] No valid signals found.")
            return

        for result in analysis_results:
            try:
                symbol = result.get("symbol")
                action = result.get("combined_action", "Neutral ⚪")
                patterns = result.get("patterns", [])
                confidence = result.get("avg_confidence", 0.0)
                signal_category = result.get("signal_category", "⭐")

                if not symbol:
                    logger.warning("[AutoAnalysis] Symbol missing in result. Skipping.")
                    continue

                if confidence < 60:
                    logger.info(f"[AutoAnalysis] {symbol} → Low confidence ({confidence:.1f}%). Skipping.")
                    continue

                if action not in ["Long 📈", "Short 📉"]:
                    logger.info(f"[AutoAnalysis] {symbol} → No strong action detected ({action}). Skipping.")
                    continue

                valid_patterns = [p for p in patterns if p.get("stars", 0) >= 3]
                if not valid_patterns:
                    logger.info(f"[AutoAnalysis] {symbol} → No strong patterns found. Skipping.")
                    continue

                # Build Ultra Signal Message
                signal_message = build_ultra_signal(
                    symbol=symbol,
                    move=action,
                    volume_spike=result.get("volume_info"),
                    atr_breakout=result.get("volatility_info"),
                    risk_reward=result.get("risk_reward_info"),
                    lang=language
                )

                if signal_message:
                    await bot.send_message(
                        chat_id=chat_id,
                        text=signal_message,
                        parse_mode="Markdown",
                        disable_web_page_preview=True
                    )
                    logger.info(f"✅ [AutoAnalysis] Signal dispatched for {symbol}.")

                    # Update Session Statistics
                    update_session_tracker(
                        signal_strength=len(valid_patterns),
                        avg_confidence=confidence
                    )

                await asyncio.sleep(1.0)  # Protection against Telegram flood limits

            except Exception as symbol_error:
                logger.error(f"❌ [AutoAnalysis] Signal dispatch failed for {symbol}: {symbol_error}")
                await report_error(bot, chat_id, symbol_error, context_info=f"AutoAnalysis Error ({symbol})")

        await bot.send_message(chat_id=chat_id, text="✅ *Auto-Analysis Completed Successfully!*", parse_mode="Markdown")
        logger.info("✅ [AutoAnalysis] Full auto scan completed.")

    except Exception as global_error:
        logger.critical(f"🔥 [AutoAnalysis] Fatal Error during scan: {global_error}")
        await report_error(bot, chat_id, global_error, context_info="AutoAnalysis Global Error")
