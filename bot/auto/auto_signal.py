import os
import asyncio
from telegram import Bot
from bot.engine.analysis_engine import analyze_symbol, format_symbol
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.autoscaler import run_autoscaler
from bot.config.settings import get_settings
import logging

# Konfiguration laden
config = get_settings()

logger = logging.getLogger(__name__)

async def daily_analysis_job(context: ContextTypes.DEFAULT_TYPE):
    """
    Führt täglich eine kompakte Analyse aller überwachten Indizes durch
    und sendet die Ergebnisse automatisch an den Telegram-Chat.
    """
    bot: Bot = context.bot
    chat_id = int(config["TELEGRAM_CHAT_ID"])  # Telegram-Chat-ID aus den Einstellungen
    lang = "de"  # Standard-Sprache (später optional dynamisch je Gruppe)

    # Startnachricht an den Chat senden
    await bot.send_message(chat_id=chat_id, text="📊 *Starte tägliche Analyse...*", parse_mode="Markdown")

    # Autoscaler starten (wenn konfiguriert)
    try:
        await run_autoscaler(bot, chat_id)  # Überprüfung des Autoscalers
    except Exception as e:
        logger.error(f"Fehler beim Autoscaler: {e}")
        await bot.send_message(chat_id=chat_id, text=f"⚠️ Fehler beim Autoscaler: {e}")  # Fehlerprotokollierung

    # Überprüfen, ob Symbole für die Auto-Analyse definiert wurden
    symbols = config["AUTO_SIGNAL_SYMBOLS"]
    if not symbols:
        await bot.send_message(chat_id=chat_id, text="❌ Keine Symbole für Auto-Analyse definiert.")  # Fehlermeldung bei leerer Symbol-Liste
        return

    # Analyse der Symbole
    for symbol in symbols:
        try:
            # Symbol analysieren und Ergebnis zurückgeben
            formatted_symbol = format_symbol(symbol)  # Formatierung des Symbols gemäß TwelveData API
            logger.info(f"Starte Analyse für Symbol: {formatted_symbol}")  # Logge, welches Symbol gerade analysiert wird

            result = await analyze_symbol(formatted_symbol)  # Hier wird die Analyse-Funktion aufgerufen
            
            if isinstance(result, str):
                await bot.send_message(chat_id=chat_id, text=result, parse_mode="Markdown")  # Falls das Ergebnis ein String ist, wird es gesendet
            else:
                # Detaillierte Ausgabe für jedes Symbol
                response = f"Symbol: {formatted_symbol}\n"
                response += f"Signal: {result['signal']}\n"
                response += f"RSI: {result['rsi']}\n"
                response += f"Trend: {result['trend']}\n"
                response += f"Pattern: {result['pattern']}\n"
                response += f"Stars: {result['stars']}/5"
                await bot.send_message(chat_id=chat_id, text=response, parse_mode="Markdown")
            
            # Kurze Pause zwischen den Nachrichten, um das Telegram API-Limit zu respektieren
            await asyncio.sleep(1.5)

        except Exception as e:
            # Fehler beim Abrufen der Analyse-Daten für das Symbol
            logger.error(f"Fehler bei der Analyse von {symbol}: {e}")
            await bot.send_message(chat_id=chat_id, text=f"⚠️ Fehler bei {symbol}: {e}")

    # Abschließende Nachricht nach der Analyse
    await bot.send_message(chat_id=chat_id, text="✅ *Tägliche Analyse abgeschlossen!*", parse_mode="Markdown")
