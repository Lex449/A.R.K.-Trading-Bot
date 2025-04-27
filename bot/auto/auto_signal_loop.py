# bot/auto/auto_signal_loop.py

import asyncio
import logging
from telegram import Bot
from bot.engine.analysis_engine import analyze_symbol
from bot.engine.risk_manager import assess_signal_risk
from bot.utils.session_tracker import update_session_tracker
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings
from bot.utils.market_time import is_trading_day, is_trading_hours

# Setup Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Load Config
config = get_settings()

async def auto_signal_loop():
    bot = Bot(token=config["BOT_TOKEN"])
    chat_id = int(config["TELEGRAM_CHAT_ID"])

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("[Auto Signal] Webhook gelöscht (falls vorhanden).")
    except Exception as e:
        logger.warning(f"[Auto Signal] Fehler beim Löschen des Webhooks: {str(e)}")

    logger.info("[Auto Signal] Starte automatisierten Signal-Loop...")

    while True:
        try:
            if not is_trading_day():
                logger.info("[Auto Signal] Kein Handelstag. Pause 5 min.")
                await asyncio.sleep(300)
                continue

            if not is_trading_hours():
                logger.info("[Auto Signal] Markt geschlossen. Pause 5 min.")
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

                    if not result or result.get("stars", 0) < 3:
                        continue  # Nur Signale ab 3 Sterne senden

                    # Risk Assessment
                    risk_message, _ = await assess_signal_risk(result)

                    # Update Session Stats
                    update_session_tracker(result["stars"])

                    # Build Signal Message
                    signal_text = (
                        f"⚡ *Live Trading Signal!*\n\n"
                        f"*Symbol:* `{symbol}`\n"
                        f"*Richtung:* {'Long 📈' if result['signal'] == 'Buy' else 'Short 📉'}\n"
                        f"*Confidence:* {result['confidence']}%\n"
                        f"*Rating:* {'⭐' * result['stars']}\n"
                        f"*Pattern:* {result['pattern']}\n"
                        f"*Candlestick:* {result['candlestick']}\n"
                        f"*Empfohlene Haltedauer:* {result['suggested_holding']}\n\n"
                        f"{risk_message}\n"
                        f"_Hinweis: Keine Finanzberatung._"
                    )

                    await bot.send_message(
                        chat_id=chat_id,
                        text=signal_text,
                        parse_mode="Markdown",
                        disable_web_page_preview=True
                    )
                    await asyncio.sleep(1.5)

                except Exception as e:
                    await report_error(bot, chat_id, e, context_info=f"Auto Signal für {symbol}")
                    logger.error(f"[Auto Signal] Fehler bei {symbol}: {e}")

            logger.info("[Auto Signal] Zyklus abgeschlossen. Schlafmodus bis nächste Prüfung.")
            await asyncio.sleep(config.get("SIGNAL_CHECK_INTERVAL_SEC", 60))

        except Exception as e:
            logger.critical(f"[Auto Signal Loop] Kritischer Fehler: {e}")
            await report_error(bot, chat_id, e, context_info="Auto Signal Main Loop")
            await asyncio.sleep(60)
