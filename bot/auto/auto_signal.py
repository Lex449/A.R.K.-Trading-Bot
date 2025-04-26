# bot/auto/auto_signal.py

import os
import asyncio
import logging
from telegram import Bot
from bot.engine.analysis_engine import analyze_symbol
from bot.engine.risk_manager import assess_signal_risk
from bot.utils.session_tracker import update_session_tracker
from bot.utils.error_reporter import report_error
from bot.utils.market_time import is_trading_day  # Neu: Check ob Handelstag
from bot.config.settings import get_settings

# Setup Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Load Configuration
config = get_settings()

async def auto_signal_loop():
    """
    Kontinuierliche, vollautomatische Generierung von Trading-Signalen – nur an Handelstagen.
    """
    bot = Bot(token=config["BOT_TOKEN"])
    chat_id = int(config["TELEGRAM_CHAT_ID"])

    try:
        await bot.delete_webhook()
    except Exception as e:
        logger.warning(f"[Webhook-Deletion] Fehler: {str(e)}")

    while True:
        if not is_trading_day():
            logger.info("[MARKET CLOSED] Wochenende erkannt. Bot pausiert Auto-Signale...")
            await asyncio.sleep(3600)  # 1 Stunde warten
            continue

        symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
        if not symbols:
            logger.error("[AUTO_SIGNAL] Keine Symbole konfiguriert.")
            await asyncio.sleep(config.get("SIGNAL_CHECK_INTERVAL_SEC", 60))
            continue

        for symbol in symbols:
            try:
                result = await analyze_symbol(symbol)

                if not result:
                    await bot.send_message(chat_id=chat_id, text=f"⚠️ No data available for {symbol}.", parse_mode="Markdown")
                    continue

                # Risk Management und Session Tracking
                risk_message, is_warning = await assess_signal_risk(result)
                update_session_tracker(result['stars'])

                # Nachricht aufbauen
                message = (
                    f"📈 *Auto Trading Signal*\n\n"
                    f"*Symbol:* {symbol}\n"
                    f"*Action:* {result['signal']}\n"
                    f"*Short-Term Trend:* {result['short_term_trend']}\n"
                    f"*Mid-Term Trend:* {result['mid_term_trend']}\n"
                    f"*RSI:* {result['rsi']}\n"
                    f"*Pattern Detected:* {result['pattern']}\n"
                    f"*Candlestick Formation:* {result['candlestick']}\n"
                    f"*Quality Rating:* {result['stars']} ⭐\n"
                    f"*Suggested Holding:* {result['suggested_holding']}\n\n"
                    f"{risk_message}\n"
                    f"🔎 Always manage your risk. No financial advice."
                )

                await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
                await asyncio.sleep(1.5)  # Respektiere Telegram API Limits

            except Exception as e:
                await report_error(bot, chat_id, e, context_info=f"AutoSignal error with {symbol}")
                logger.error(f"[AutoSignal Error] Symbol: {symbol} | Error: {e}")

        logger.info("[AUTO_SIGNAL] Runde abgeschlossen. Warte auf nächsten Scan...")
        await asyncio.sleep(config.get("SIGNAL_CHECK_INTERVAL_SEC", 60))
