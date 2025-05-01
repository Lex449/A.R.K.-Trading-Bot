"""
A.R.K. Auto Market Scanner – Full Coverage Loop v3.1  
Scannt ALLE Symbole aus .env alle 60 Sekunden – mit voller API-Nutzung.  
Kompatibel mit Railway + Application-Kontext.  
Made in Bali! Engineered with German Precision.
"""

import asyncio
from telegram.ext import Application
from bot.engine.analysis_engine import analyze_symbol
from bot.utils.ultra_signal_builder import build_ultra_signal
from bot.utils.session_tracker import update_session_tracker
from bot.utils.error_reporter import report_error
from bot.utils.logger import setup_logger
from bot.config.settings import get_settings

logger = setup_logger(__name__)
config = get_settings()

async def auto_analysis(application: Application):
    """
    Führt eine komplette Analyse aller Symbole aus AUTO_SIGNAL_SYMBOLS durch.
    """
    bot = application.bot
    chat_id = int(config["TELEGRAM_CHAT_ID"])
    language = config.get("BOT_LANGUAGE", "en")
    symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])

    if not symbols:
        logger.error("❌ [AutoAnalysis] Keine Symbole konfiguriert.")
        return

    logger.info(f"🔁 [AutoAnalysis] Starte Vollscan für {len(symbols)} Symbole...")

    for symbol in symbols:
        try:
            result = await analyze_symbol(symbol, chat_id=chat_id, silent=True)
            if not result:
                logger.info(f"⏩ [AutoAnalysis] {symbol} – Keine verwertbare Analyse.")
                continue

            action = result.get("combined_action", "Neutral ⚪")
            patterns = result.get("patterns", [])
            confidence = result.get("avg_confidence", 0.0)

            if confidence < 40 or action not in ["Long 📈", "Short 📉"]:
                logger.info(f"⏩ [AutoAnalysis] {symbol} – Confidence zu niedrig oder neutral.")
                continue

            valid_patterns = [p for p in patterns if p.get("stars", 0) >= 3]
            if not valid_patterns:
                logger.info(f"⏩ [AutoAnalysis] {symbol} – Keine starken Patterns.")
                continue

            # Signal erstellen
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
                logger.info(f"✅ [AutoAnalysis] Signal gesendet: {symbol} ({action})")

                update_session_tracker(
                    signal_strength=len(valid_patterns),
                    avg_confidence=confidence
                )

            await asyncio.sleep(1.0)

        except Exception as symbol_error:
            logger.error(f"❌ [AutoAnalysis] Fehler bei {symbol}: {symbol_error}")
            await report_error(bot, chat_id, symbol_error, context_info=f"AutoAnalysis Symbol Error ({symbol})")

    logger.info("✅ [AutoAnalysis] Vollscan abgeschlossen.")
