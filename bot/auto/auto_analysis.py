import asyncio
import logging
from telegram import Bot
from telegram.ext import ContextTypes
from bot.engine.analysis_engine import analyze_symbol
from bot.utils.signal_builder import build_signal_message
from bot.utils.session_tracker import update_session_tracker
from bot.utils.error_reporter import report_error
from bot.utils.logger import setup_logger
from bot.config.settings import get_settings

# Logger Setup
logger = setup_logger(__name__)

# Config Load
config = get_settings()

async def daily_analysis_job(context: ContextTypes.DEFAULT_TYPE):
    """
    Daily ultra-market analysis for all symbols.
    Only strong signals will be sent as a compact daily report.
    """

    bot: Bot = context.bot
    chat_id = int(config["TELEGRAM_CHAT_ID"])

    try:
        logger.info("[Daily Analysis] Starting full market analysis.")
        await bot.send_message(chat_id=chat_id, text="📊 *Starting full daily analysis...*", parse_mode="Markdown")

        symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
        if not symbols:
            logger.error("[Daily Analysis] No symbols configured.")
            await bot.send_message(chat_id=chat_id, text="❌ *No symbols defined for analysis.*", parse_mode="Markdown")
            return

        for symbol in symbols:
            try:
                result = await analyze_symbol(symbol)

                if not result:
                    logger.warning(f"[Daily Analysis] No analysis data for {symbol}.")
                    continue

                if result.get('pattern_count', 0) == 0:
                    logger.info(f"[Daily Analysis] {symbol} → No patterns found. Skipping.")
                    continue

                avg_confidence = result.get("avg_confidence", 0)
                if avg_confidence < 55:
                    logger.info(f"[Daily Analysis] {symbol} → Confidence {avg_confidence} too low. Skipping.")
                    continue

                # Session Tracker Update
                update_session_tracker(result.get("pattern_count", 0))

                # Build Signal Message
                signal_message = build_signal_message(
                    symbol=symbol,
                    patterns=result.get("patterns", []),
                    combined_action=result.get("combined_action", "Neutral ⚪"),
                    avg_confidence=result.get("avg_confidence", 0),
                    indicator_score=result.get("indicator_score", 0),
                    trend_direction=result.get("trend_direction", "Neutral ⚪"),
                )

                if not signal_message:
                    continue

                await bot.send_message(
                    chat_id=chat_id,
                    text=signal_message,
                    parse_mode="Markdown",
                    disable_web_page_preview=True
                )
                logger.info(f"[Daily Analysis] Daily signal sent for {symbol}.")

                await asyncio.sleep(1.5)  # API protection

            except Exception as symbol_error:
                logger.error(f"[Daily Analysis] Error for {symbol}: {symbol_error}")
                await report_error(bot, chat_id, symbol_error, context_info=f"Daily Analysis {symbol}")

        await bot.send_message(chat_id=chat_id, text="✅ *Daily analysis completed!*", parse_mode="Markdown")
        logger.info("[Daily Analysis] Analysis job completed.")

    except Exception as e:
        logger.critical(f"[Daily Analysis Fatal Error] {e}")
        await report_error(bot, chat_id, e, context_info="Fatal error in daily analysis")
