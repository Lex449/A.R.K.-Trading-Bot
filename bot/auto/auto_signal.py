# bot/auto/auto_signal.py

import asyncio
import logging
from telegram import Bot
from bot.engine.analysis_engine import analyze_symbol
from bot.engine.risk_manager import assess_signal_risk
from bot.utils.session_tracker import update_session_tracker
from bot.utils.error_reporter import report_error
from bot.utils.market_time import is_trading_day, is_trading_hours
from bot.config.settings import get_settings
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# Load configuration
config = get_settings()

async def auto_signal_loop():
    """
    Analysiert fortlaufend konfigurierte Symbole
    und sendet automatisch Trading-Signale während gültiger Handelszeiten.
    """
    bot = Bot(token=config["BOT_TOKEN"])
    chat_id = int(config["TELEGRAM_CHAT_ID"])

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("[Auto Signal] Webhook gelöscht (falls vorhanden).")
    except Exception as e:
        logger.warning(f"[Auto Signal] Fehler beim Löschen des Webhooks: {e}")

    logger.info("[Auto Signal] Starte Haupt-Signal-Loop.")

    while True:
        try:
            # Market Timing Check
            if not is_trading_day() or not is_trading_hours():
                logger.info("[Auto Signal] Markt geschlossen. Pause 5 Minuten.")
                await asyncio.sleep(300)
                continue

            symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
            if not symbols:
                logger.error("[Auto Signal] Keine Symbole konfiguriert! Pause 1 Minute.")
                await asyncio.sleep(config.get("SIGNAL_CHECK_INTERVAL_SEC", 60))
                continue

            for symbol in symbols:
                try:
                    result = await analyze_symbol(symbol)

                    if not result:
                        logger.warning(f"[Auto Signal] Keine Daten für {symbol}. Übersprungen.")
                        continue

                    if result.get('signal') == "Hold" or result.get('pattern') == "No Pattern":
                        logger.info(f"[Auto Signal] {symbol} → Hold oder kein Pattern erkannt. Übersprungen.")
                        continue

                    # Risk Assessment
                    risk_message, _ = await assess_signal_risk(result)

                    # Session Update
                    update_session_tracker(result.get("stars", 0))

                    # Build Signal Message
                    message = (
                        f"⚡ *Auto Trading Signal*\n\n"
                        f"*Symbol:* `{symbol}`\n"
                        f"*Richtung:* {result['signal']} {'📈' if result['signal'] == 'Buy' else '📉'}\n"
                        f"*Short-Term Trend:* {result.get('short_term_trend', '-')}\n"
                        f"*Mid-Term Trend:* {result.get('mid_term_trend', '-')}\n"
                        f"*RSI:* {result.get('rsi', '-')}\n"
                        f"*Pattern:* {result.get('pattern', '-')}\n"
                        f"*Candlestick:* {result.get('candlestick', '-')}\n"
                        f"*Qualitätsrating:* {'⭐' * result.get('stars', 0)}\n"
                        f"*Empfohlene Haltedauer:* {result.get('suggested_holding', '-')}\n\n"
                        f"{risk_message}\n"
                        f"_Hinweis: Eigenverantwortung beim Handeln._"
                    )

                    await bot.send_message(
                        chat_id=chat_id,
                        text=message,
                        parse_mode="Markdown",
                        disable_web_page_preview=True
                    )
                    logger.info(f"[Auto Signal] Signal gesendet für {symbol}.")
                    await asyncio.sleep(1.5)

                except Exception as symbol_error:
                    logger.error(f"[Auto Signal] Fehler bei {symbol}: {symbol_error}")
                    await report_error(bot, chat_id, symbol_error, context_info=f"AutoSignal für {symbol}")

            logger.info("[Auto Signal] Zyklus abgeschlossen. Pause bis nächste Prüfung.")
            await asyncio.sleep(config.get("SIGNAL_CHECK_INTERVAL_SEC", 60))

        except Exception as loop_error:
            logger.critical(f"[Auto Signal Loop] Schwerer Fehler: {loop_error}")
            await report_error(bot, chat_id, loop_error, context_info="Fataler Fehler in auto_signal_loop")
            await asyncio.sleep(300)
