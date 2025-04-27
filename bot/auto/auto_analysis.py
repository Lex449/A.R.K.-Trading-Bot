# bot/auto/auto_analysis.py

import asyncio
import logging
from telegram import Bot
from telegram.ext import ContextTypes
from bot.engine.analysis_engine import analyze_symbol
from bot.engine.risk_manager import assess_signal_risk
from bot.utils.session_tracker import update_session_tracker
from bot.utils.error_reporter import report_error
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.autoscaler import run_autoscaler
from bot.config.settings import get_settings
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# Load configuration
config = get_settings()

async def daily_analysis_job(context: ContextTypes.DEFAULT_TYPE):
    """
    Führt eine tägliche Marktanalyse aller konfigurierten Symbole aus.
    Sendet nur echte Buy/Sell-Signale – Hold/No Pattern werden übersprungen.
    """
    bot: Bot = context.bot
    chat_id = int(config["TELEGRAM_CHAT_ID"])
    lang = get_language(chat_id) or "en"

    try:
        logger.info("[Auto Analysis] Starte tägliche Analyse.")
        await bot.send_message(chat_id=chat_id, text="📊 *Starte vollständige Tagesanalyse...*", parse_mode="Markdown")

        # Optional: Autoscaler Trigger
        try:
            await run_autoscaler(bot, chat_id)
        except Exception as e:
            logger.warning(f"[Autoscaler Error] {e}")
            await report_error(bot, chat_id, e, context_info="Autoscaler während täglicher Analyse")

        symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
        if not symbols:
            logger.error("[Auto Analysis] Keine Symbole konfiguriert.")
            await bot.send_message(chat_id=chat_id, text="❌ *Keine Symbole für Analyse definiert.*", parse_mode="Markdown")
            return

        for symbol in symbols:
            try:
                result = await analyze_symbol(symbol)

                if not result:
                    logger.warning(f"[Auto Analysis] Keine Daten für {symbol}.")
                    continue

                if result.get('signal') == "Hold" or result.get('pattern') == "No Pattern":
                    logger.info(f"[Auto Analysis] {symbol} → Hold oder No Pattern. Übersprungen.")
                    continue

                # Risk Management und Session Tracking
                risk_message, _ = await assess_signal_risk(result)
                update_session_tracker(result.get("stars", 0))

                # Signal-Nachricht bauen
                message = (
                    f"📈 *Daily Analysis Signal*\n\n"
                    f"*Symbol:* `{symbol}`\n"
                    f"*Richtung:* {result['signal']} {'📈' if result['signal'] == 'Buy' else '📉'}\n"
                    f"*Short-Term Trend:* {result.get('short_term_trend', '-')}\n"
                    f"*Mid-Term Trend:* {result.get('mid_term_trend', '-')}\n"
                    f"*RSI:* {result.get('rsi', '-')}\n"
                    f"*Pattern:* {result.get('pattern', '-')}\n"
                    f"*Candlestick:* {result.get('candlestick', '-')}\n"
                    f"*Rating:* {'⭐' * result.get('stars', 0)}\n"
                    f"*Empfohlene Haltedauer:* {result.get('suggested_holding', '-')}\n\n"
                    f"{risk_message}\n"
                    f"_Hinweis: Risiko immer eigenständig steuern._"
                )

                await bot.send_message(
                    chat_id=chat_id,
                    text=message,
                    parse_mode="Markdown",
                    disable_web_page_preview=True
                )
                logger.info(f"[Auto Analysis] Signal gesendet für {symbol}.")

                await asyncio.sleep(1.5)  # kleine Pause gegen API-Spam

            except Exception as symbol_error:
                logger.error(f"[Auto Analysis] Fehler bei {symbol}: {symbol_error}")
                await report_error(bot, chat_id, symbol_error, context_info=f"Auto Analysis Error {symbol}")

        await bot.send_message(chat_id=chat_id, text="✅ *Tagesanalyse erfolgreich abgeschlossen!*", parse_mode="Markdown")
        logger.info("[Auto Analysis] Tagesanalyse erfolgreich abgeschlossen.")

    except Exception as e:
        logger.critical(f"[Auto Analysis Fatal Error] {e}")
        await report_error(bot, chat_id, e, context_info="Fataler Fehler in Daily Analysis")
