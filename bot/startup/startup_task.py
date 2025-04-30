"""
A.R.K. Auto-Analysis Scheduler – Silent Loop Edition
Startet alle 60 Sekunden einen vollständigen Markt-Scan – nur bei validem Signal wird gepostet.
Made in Bali. Engineered with German Precision.
"""

from telegram.ext import JobQueue, ContextTypes
from bot.engine.analysis_engine import analyze_market
from bot.utils.ultra_signal_builder import build_ultra_signal
from bot.utils.session_tracker import update_session_tracker
from bot.utils.logger import setup_logger
from bot.utils.api_bridge import record_call
from bot.config.settings import get_settings

logger = setup_logger(__name__)
settings = get_settings()

def start_auto_analysis_scheduler(job_queue: JobQueue):
    job_queue.run_repeating(
        auto_analysis_silent,
        interval=60,  # alle 60 Sekunden
        first=10,
        name="auto_analysis_scheduler"
    )
    logger.info("✅ [Scheduler] Silent Auto-Analysis Scheduler aktiviert.")

async def auto_analysis_silent(context: ContextTypes.DEFAULT_TYPE):
    bot = context.bot
    chat_id = int(settings["TELEGRAM_CHAT_ID"])
    symbols = settings.get("AUTO_SIGNAL_SYMBOLS", [])
    language = settings.get("BOT_LANGUAGE", "en")

    if not symbols:
        logger.warning("⚠️ [AutoAnalysis] Keine Symbole konfiguriert.")
        return

    try:
        results = await analyze_market(symbols)
        if not results:
            logger.info("ℹ️ [AutoAnalysis] Keine validen Signale erkannt.")
            return

        for result in results:
            try:
                action = result.get("combined_action", "Neutral ⚪")
                confidence = result.get("avg_confidence", 0.0)
                patterns = result.get("patterns", [])

                if action not in ["Long 📈", "Short 📉"] or confidence < 60:
                    continue

                valid_patterns = [p for p in patterns if p.get("stars", 0) >= 3]
                if not valid_patterns:
                    continue

                msg = build_ultra_signal(
                    symbol=result["symbol"],
                    move=action,
                    volume_spike=result.get("volume_info"),
                    atr_breakout=result.get("volatility_info"),
                    risk_reward=result.get("risk_reward_info"),
                    lang=language
                )

                if msg:
                    await bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown", disable_web_page_preview=True)
                    update_session_tracker(
                        signal_strength=len(valid_patterns),
                        avg_confidence=confidence
                    )
                    record_call("auto_analysis")

            except Exception as signal_err:
                logger.error(f"❌ [AutoAnalysis] Signalfehler bei {result.get('symbol')}: {signal_err}")

    except Exception as e:
        logger.exception(f"🔥 [AutoAnalysis] Globaler Fehler im Scheduler: {e}")
