# bot/auto/auto_signal_loop.py

"""
Automatisierter Echtzeit-Signal-Loop für Premium Trading Signale.
Ultra-Masterclass Build – Nur Qualität, keine Masse.
Optimiert für 1x Bot-Instance – keine 409 Conflicts mehr.
"""

import asyncio
import logging
from telegram import Bot
from bot.engine.analysis_engine import analyze_symbol
from bot.engine.risk_manager import assess_signal_risk
from bot.utils.signal_builder import build_signal_message
from bot.utils.session_tracker import update_session_tracker
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings
from bot.utils.market_time import is_trading_day, is_trading_hours

# Setup structured logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Load Config
config = get_settings()

async def auto_signal_loop(bot: Bot):
    """
    Startet die kontinuierliche Echtzeitanalyse und Signalversand.
    Erwartet bereits bestehenden Telegram Bot aus ApplicationContext.
    """

    chat_id = int(config["TELEGRAM_CHAT_ID"])
    logger.info("[Auto Signal] Starte Ultra-Auto-Loop... (kein Webhook Eingriff)")

    while True:
        try:
            if not is_trading_day():
                logger.info("[Auto Signal] Kein Handelstag. Sleep 5min.")
                await asyncio.sleep(300)
                continue

            if not is_trading_hours():
                logger.info("[Auto Signal] Markt geschlossen. Sleep 5min.")
                await asyncio.sleep(300)
                continue

            symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
            if not symbols:
                logger.error("[Auto Signal] Keine Symbole konfiguriert!")
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
                        continue  # Kein starkes Pattern vorhanden → weiter

                    # Session Tracker aktualisieren
                    update_session_tracker(len(valid_patterns))

                    # Signaltext bauen
                    signal_message = build_signal_message(
                        symbol=symbol,
                        patterns=valid_patterns,
                        combined_action=result.get("combined_action", "Neutral ⚪"),
                        avg_confidence=result.get("avg_confidence", 0)
                    )

                    if not signal_message:
                        continue

                    await bot.send_message(
                        chat_id=chat_id,
                        text=signal_message,
                        parse_mode="Markdown",
                        disable_web_page_preview=True
                    )
                    logger.info(f"[Auto Signal] Signal gesendet für {symbol}.")

                    await asyncio.sleep(1.5)

                except Exception as symbol_error:
                    logger.error(f"[Auto Signal] Fehler bei {symbol}: {symbol_error}")
                    await report_error(bot, chat_id, symbol_error, context_info=f"Auto Signal {symbol}")

            logger.info("[Auto Signal] Zyklus abgeschlossen. Sleep bis nächste Prüfung.")
            await asyncio.sleep(config.get("SIGNAL_CHECK_INTERVAL_SEC", 60))

        except Exception as loop_error:
            logger.critical(f"[Auto Signal Loop] Schwerer Fehler: {loop_error}")
            await report_error(bot, chat_id, loop_error, context_info="Auto Signal Main Loop Critical Error")
            await asyncio.sleep(60)
