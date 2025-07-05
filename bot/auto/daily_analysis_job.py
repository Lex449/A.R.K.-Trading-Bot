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

logger = setup_logger(__name__)
settings = get_settings()

bot_token = settings["BOT_TOKEN"]
chat_id   = int(settings["TELEGRAM_CHAT_ID"])
symbols   = settings.get("AUTO_SIGNAL_SYMBOLS", [])
language  = settings.get("BOT_LANGUAGE", "en")

async def daily_analysis_job(context: ContextTypes.DEFAULT_TYPE = None):
    """Executes a full market scan once daily and sends only high-quality trade alerts."""
    bot = Bot(token=bot_token)
    logger.info("🚀 [DailyAnalysis] Starting full market analysis...")

    if not symbols:
        logger.error("❌ [DailyAnalysis] No symbols configured – aborting.")
        return

    try:
        for symbol in symbols:
            analysis = await analyze_symbol(symbol)
            if not analysis:
                continue
            signal_text = build_ultra_signal(analysis, language=language)
            await bot.send_message(chat_id=chat_id, text=signal_text, parse_mode="HTML")

        update_session_tracker("daily_analysis_completed")
        logger.info("✅ [DailyAnalysis] Completed without errors.")

    except Exception as e:
        await report_error(e, context="daily_analysis_job")
        logger.exception("🔥 [DailyAnalysis] Unhandled exception.")
