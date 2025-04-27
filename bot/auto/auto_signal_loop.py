"""
Automatisierter Ultra Echtzeit-Signal-Loop inkl. Move-Alert.
Nur Premium-Qualität – Keine Masse, keine Fehler.
"""

import asyncio
import logging
from telegram import Bot
from bot.engine.analysis_engine import analyze_symbol
from bot.engine.move_alert_engine import detect_move_alert
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
    Startet die kontinuierliche Echtzeitanalyse und Move-Alert Erkennung.
    Erwartet Telegram Bot Instanz aus ApplicationContext.
    """

    chat_id = int(config["TELEGRAM_CHAT_ID"])
    logger.info("[Auto Signal] Ultra-Loop gestartet... (Live Analyse läuft)")

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

                    valid_patterns = [p for p in result.get("patterns", []) if "⭐" in p and p.count("⭐") >= 3]

                    # Move Alert Analyse (parallel)
                    move_alert = await detect_move_alert(result.get("df"))

                    if move_alert:
                        move_type = move_alert["type"]
                        move_percent = move_alert["move_percent"]

                        if move_type == "full":
                            move_message = (
                                f"🚨 *Starker 1-Minuten-Move erkannt!*\n\n"
                                f"*Symbol:* `{symbol}`\n"
                                f"*Bewegung:* `{move_percent:.2f}%`\n"
                                f"_A.R.K. überwacht die Märkte 24/7._"
                            )
                        else:
                            move_message = (
                                f"⚠️ *Frühwarnung: Bewegung detected*\n\n"
                                f"*Symbol:* `{symbol}`\n"
                                f"*Bewegung:* `{move_percent:.2f}%`\n"
                                f"_A.R.K. hält dich auf dem Laufenden._"
                            )

                        await bot.send_message(
                            chat_id=chat_id,
                            text=move_message,
                            parse_mode="Markdown",
                            disable_web_page_preview=True
                        )
                        logger.info(f"[Move Alert] Move erkannt für {symbol} → {move_percent:.2f}%")

                        # Kurze Pause nach Move Alert, damit kein Spam
                        await asyncio.sleep(2)

                    # Nur Signale ab 3 Sternen senden
                    if not valid_patterns:
                        continue

                    update_session_tracker(len(valid_patterns))

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
                    logger.info(f"[Auto Signal] Premium-Signal gesendet für {symbol}.")

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
