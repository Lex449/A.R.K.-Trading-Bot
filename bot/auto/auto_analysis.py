"""
A.R.K. Auto Market Scanner – Silent Premium Edition v2.0  
Scannt alle konfigurierten Symbole alle 60s – völlig lautlos, außer bei validen Signalen.  
Maximale Effizienz, kein Spam.  
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

logger = setup_logger(__name__)
config = get_settings()

async def auto_analysis(context: ContextTypes.DEFAULT_TYPE):
    """
    Führt einen vollständigen dynamischen Marktscan durch – nur Ausgabe bei Signalen.
    """
    bot: Bot = context.bot
    chat_id = int(config["TELEGRAM_CHAT_ID"])
    language = config.get("BOT_LANGUAGE", "en")
    symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])

    if not symbols:
        logger.error("❌ [AutoAnalysis] Keine Symbole konfiguriert.")
        return

    logger.info("🔄 [AutoAnalysis] Markt-Scan gestartet...")

    try:
        analysis_results = await analyze_market(symbols)

        if not analysis_results:
            logger.info("ℹ️ [AutoAnalysis] Keine Analyseergebnisse erhalten.")
            return

        found_valid_signals = False

        for result in analysis_results:
            try:
                symbol = result.get("symbol")
                action = result.get("combined_action", "Neutral ⚪")
                patterns = result.get("patterns", [])
                confidence = result.get("avg_confidence", 0.0)
                signal_category = result.get("signal_category", "⭐")

                if not symbol or confidence < 60 or action not in ["Long 📈", "Short 📉"]:
                    continue

                valid_patterns = [p for p in patterns if p.get("stars", 0) >= 3]
                if not valid_patterns:
                    continue

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
                    logger.info(f"✅ [AutoAnalysis] Signal versendet: {symbol} ({action})")
                    found_valid_signals = True

                    update_session_tracker(
                        signal_strength=len(valid_patterns),
                        avg_confidence=confidence
                    )

                await asyncio.sleep(1.0)

            except Exception as symbol_error:
                logger.error(f"❌ [AutoAnalysis] Fehler bei {symbol}: {symbol_error}")
                await report_error(bot, chat_id, symbol_error, context_info=f"AutoAnalysis Symbol Error ({symbol})")

        if found_valid_signals:
            logger.info("✅ [AutoAnalysis] Scan abgeschlossen mit gültigen Signalen.")
        else:
            logger.info("ℹ️ [AutoAnalysis] Kein gültiges Signal im Scan gefunden.")

    except Exception as global_error:
        logger.critical(f"🔥 [AutoAnalysis] Fataler Scanfehler: {global_error}")
        await report_error(bot, chat_id, global_error, context_info="AutoAnalysis Global Error")
