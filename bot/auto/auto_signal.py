import os
import json
import asyncio
from telegram import Bot
from telegram.ext import ContextTypes  # Sicherstellen, dass dieser Import vorhanden ist
from bot.engine.analysis_engine import analyze_symbol, format_symbol  # Stelle sicher, dass format_symbol korrekt verwendet wird
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.autoscaler import run_autoscaler
from bot.config.settings import get_settings
import logging

# Konfiguration laden
config = get_settings()

logger = logging.getLogger(__name__)

async def auto_signal_loop():
    """
    Diese Funktion kümmert sich um das automatische Senden von Signalen
    in regelmäßigen Abständen (z.B. alle 60 Sekunden).
    """
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    chat_id = int(config["TELEGRAM_CHAT_ID"])

    if bot is None:
        logger.error("Bot-Instanz konnte nicht abgerufen werden.")
        return

    # Lösche den Webhook zu Beginn, um Konflikte zu vermeiden
    await bot.delete_webhook()

    while True:
        symbols = config["AUTO_SIGNAL_SYMBOLS"]
        if not symbols:
            logger.error("Keine Symbole für Auto-Analyse definiert.")
            return

        for symbol in symbols:
            try:
                formatted_symbol = format_symbol(symbol)  # Formatierung des Symbols
                logger.info(f"Starte Analyse für Symbol: {formatted_symbol}")

                result = await analyze_symbol(formatted_symbol)  # Analyse aufrufen

                if isinstance(result, str):
                    await bot.send_message(chat_id=chat_id, text=result, parse_mode="Markdown")
                else:
                    response = f"Symbol: {formatted_symbol}\n"
                    response += f"Signal: {result['signal']}\n"
                    response += f"RSI: {result['rsi']}\n"
                    response += f"Trend: {result['trend']}\n"
                    response += f"Pattern: {result['pattern']}\n"
                    response += f"Stars: {result['stars']}/5"
                    await bot.send_message(chat_id=chat_id, text=response, parse_mode="Markdown")

                await asyncio.sleep(1.5)  # Zeitverzögerung, um API-Limits zu respektieren

            except Exception as e:
                logger.error(f"Fehler bei der Analyse von {symbol}: {e}")
                await bot.send_message(chat_id=chat_id, text=f"⚠️ Fehler bei {symbol}: {e}")

        await asyncio.sleep(60)  # Pause zwischen den Runden
