# bot/auto/daily_analysis.py

"""
A.R.K. Daily Ultra Analysis
Premium Build – maximale Signalqualität bei minimalem Spam.
"""

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

# === Logger Setup ===
logger = setup_logger(__name__)

# === Config Load ===
config = get_settings()

async def daily_analysis_job(context: ContextTypes.DEFAULT_TYPE):
    """
    Tägliche Ultra-Marktanalyse für alle Symbole.
    Nur starke Signale werden als kompakter Tagesreport versendet.
    """

    bot: Bot = context.bot
    chat_id = int(config["TELEGRAM_CHAT_ID"])

    try:
        logger.info("[Daily Analysis] Starte vollständige Marktanalyse.")
        await bot.send_message(chat_id=chat_id, text="📊 *Starte vollständige Tagesanalyse...*", parse_mode="Markdown")

        symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
        if not symbols:
            logger.error("[Daily Analysis] Keine Symbole konfiguriert.")
            await bot.send_message(chat_id=chat_id, text="❌ *Keine Symbole für Analyse definiert.*", parse_mode="Markdown")
            return

        for symbol in symbols:
            try:
                result = await analyze_symbol(symbol)

                if not result:
                    logger.warning(f"[Daily Analysis] Keine Analyse-Daten für {symbol}.")
                    continue

                if result.get('pattern_count', 0) == 0:
                    logger.info(f"[Daily Analysis] {symbol} → Keine Muster erkannt. Überspringe.")
                    continue

                avg_confidence = result.get("avg_confidence", 0)
                if avg_confidence < 55:
                    logger.info(f"[Daily Analysis] {symbol} → Confidence {avg_confidence} zu niedrig. Überspringe.")
                    continue

                # Session Tracker aktualisieren
                update_session_tracker(result.get("pattern_count", 0))

                # Signaltext bauen
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
                logger.info(f"[Daily Analysis] Tages-Signal für {symbol} gesendet.")

                await asyncio.sleep(1.5)  # API-Protection

            except Exception as symbol_error:
                logger.error(f"[Daily Analysis] Fehler bei {symbol}: {symbol_error}")
                await report_error(bot, chat_id, symbol_error, context_info=f"Daily Analysis {symbol}")

        await bot.send_message(chat_id=chat_id, text="✅ *Tagesanalyse abgeschlossen!*", parse_mode="Markdown")
        logger.info("[Daily Analysis] Analyse-Job abgeschlossen.")

    except Exception as e:
        logger.critical(f"[Daily Analysis Fatal Error] {e}")
        await report_error(bot, chat_id, e, context_info="Fataler Fehler bei Tagesanalyse")
