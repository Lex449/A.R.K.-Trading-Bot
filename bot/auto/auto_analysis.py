# bot/auto/auto_analysis.py

"""
A.R.K. Auto Market Scanner Ultra 3.0 – Supreme Signal Builder.
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
    Full dynamic scan across all symbols.
    Builds premium signals, updates session stats, manages dispatch timing.
    """

    bot: Bot = context.bot
    chat_id = int(config["TELEGRAM_CHAT_ID"])
    language = config.get("BOT_LANGUAGE", "en")
    symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])

    if not symbols:
        logger.error("❌ [AutoAnalysis] No symbols configured. Scan aborted.")
        return

    logger.info("🚀 [AutoAnalysis] Starting full market scan...")
    await bot.send_message(chat_id=chat_id, text="🔍 *Starting Auto-Analysis...*", parse_mode="Markdown")

    try:
        # === Analyze all symbols ===
        results = await analyze_market(symbols)

        if not results:
            await bot.send_message(chat_id=chat_id, text="ℹ️ *No valid signals found during scan.*", parse_mode="Markdown")
            logger.info("ℹ️ [AutoAnalysis] No signals detected.")
            return

        for result in results:
            try:
                symbol = result.get("symbol")
                action = result.get("combined_action", "Neutral ⚪")
                patterns = result.get("patterns", [])
                confidence = result.get("avg_confidence", 0.0)
                signal_category = result.get("signal_category", "⭐")

                if not symbol or confidence < 60:
                    logger.info(f"[AutoAnalysis] {symbol} → Low confidence ({confidence:.1f}%). Skipping.")
                    continue

                if action not in ["Long 📈", "Short 📉"]:
                    logger.info(f"[AutoAnalysis] {symbol} → No strong action detected ({action}). Skipping.")
                    continue

                # Only allow strong patterns
                valid_patterns = [p for p in patterns if p.get("stars", 0) >= 3]
                if not valid_patterns:
                    logger.info(f"[AutoAnalysis] {symbol} → No valid high-quality patterns. Skipping.")
                    continue

                # Build Ultra Signal
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
                    logger.info(f"✅ [AutoAnalysis] Signal dispatched for {symbol}")

                    # Update session tracker
                    update_session_tracker(
                        signal_strength=len(valid_patterns),
                        avg_confidence=confidence
                    )

                await asyncio.sleep(1.0)  # Telegram API protection

            except Exception as symbol_error:
                logger.error(f"❌ [AutoAnalysis] Error dispatching signal for {symbol}: {symbol_error}")
                await report_error(bot, chat_id, symbol_error, context_info=f"AutoAnalysis Error ({symbol})")

        await bot.send_message(chat_id=chat_id, text="✅ *Auto-Analysis completed successfully!*", parse_mode="Markdown")
        logger.info("✅ [AutoAnalysis] Full scan completed.")

    except Exception as critical_error:
        logger.critical(f"🔥 [AutoAnalysis] Fatal global error: {critical_error}")
        await report_error(bot, chat_id, critical_error, context_info="AutoAnalysis Global Error")
