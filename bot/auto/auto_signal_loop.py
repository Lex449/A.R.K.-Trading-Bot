"""
A.R.K. Ultra Auto-Signal-Loop
Automatisierte Echtzeit-Signalerkennung – CEO-Niveau.
Premium Qualität – optimiert auf Struktur, Tempo und Präzision.
"""

import asyncio
import logging
from telegram import Bot
from bot.engine.analysis_engine import analyze_symbol
from bot.utils.signal_builder import build_signal_message
from bot.utils.session_tracker import update_session_tracker
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings
from bot.utils.market_time import is_trading_day, is_trading_hours

# Setup Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Load Config
config = get_settings()

async def auto_signal_loop(bot: Bot):
    """
    Startet die kontinuierliche Marktanalyse und automatischen Signalversand.
    Erwartet einen bereits initialisierten Telegram-Bot.
    """
    chat_id = int(config["TELEGRAM_CHAT_ID"])
    logger.info("[Auto Signal] Ultra-Auto-Loop gestartet... (Webhook Drop umgangen)")

    while True:
        try:
            if not is_trading_day():
                logger.info("[Auto Signal] Heute kein Handelstag. Pausiere 5min.")
                await asyncio.sleep(300)
                continue

            if not is_trading_hours():
                logger.info("[Auto Signal] Markt aktuell geschlossen. Pausiere 5min.")
                await asyncio.sleep(300)
                continue

            symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
            if not symbols:
                logger.error("[Auto Signal] Keine Symbole konfiguriert.")
                await asyncio.sleep(300)
                continue

            for symbol in symbols:
                try:
                    result = await analyze_symbol(symbol)

                    if not result:
                        continue

                    # Nur Signale ab 3 Sternen verarbeiten
                    valid_patterns = [p for p in result.get("patterns", []) if "⭐" in p and p.count("⭐") >= 3]

                    if not valid_patterns:
                        continue  # Kein starkes Muster gefunden

                    # Session Tracker Update
                    update_session_tracker(len(valid_patterns))

                    # Ultra-Signal erstellen
                    signal_message = build_signal_message(
                        symbol=symbol,
                        patterns=valid_patterns,
                        combined_action=result.get("combined_action", "Neutral ⚪"),
                        avg_confidence=result.get("avg_confidence", 0),
                        indicator_score=result.get("indicator_score", 0),
                        trend_direction=result.get("trend_direction", "Neutral ⚪")
                    )

                    if not signal_message:
                        continue

                    await bot.send_message(
                        chat_id=chat_id,
                        text=signal_message,
                        parse_mode="Markdown",
                        disable_web_page_preview=True
                    )

                    logger.info(f"[Auto Signal] Signal erfolgreich gesendet für {symbol}.")

                    await asyncio.sleep(1.5)  # Minimale Pausen zwischen Signalen

                except Exception as symbol_error:
                    logger.error(f"[Auto Signal] Fehler bei Analyse von {symbol}: {symbol_error}")
                    await report_error(bot, chat_id, symbol_error, context_info=f"Auto Signal {symbol}")

            logger.info("[Auto Signal] Analyse-Zyklus abgeschlossen. Sleep bis nächste Prüfung...")
            await asyncio.sleep(config.get("SIGNAL_CHECK_INTERVAL_SEC", 60))

        except Exception as loop_error:
            logger.critical(f"[Auto Signal Loop] Schwerer Loop-Fehler: {loop_error}")
            await report_error(bot, chat_id, loop_error, context_info="Auto Signal Main Loop Critical Error")
            await asyncio.sleep(60)
