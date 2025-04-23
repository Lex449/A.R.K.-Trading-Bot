from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.utils.analysis import analyse_market
from bot.utils.formatter import format_signal
from bot.config.settings import get_settings

# Asynchroner Signal-Handler für den /signal Befehl
async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Dieser Handler wird aufgerufen, wenn der Benutzer den /signal-Befehl ausführt."""
    
    # Informiere den Benutzer, dass die Analyse gestartet wird
    await update.message.reply_text("📡 Analysiere Märkte...")

    symbols = ["US100/USDT", "US30/USDT", "US500/USDT"]  # Märkte, die analysiert werden sollen
    results = []  # Ergebnisse der Analyse

    # Analyse jedes Symbols
    for symbol in symbols:
        try:
            result = analyse_market(symbol)  # Marktanalyse durchführen

            if result:
                # Wenn eine Analyse erfolgreich war, wird sie formatiert und der Liste hinzugefügt
                trend = result["trend"]
                confidence = result["confidence"]
                pattern = result["pattern"]
                formatted_signal = format_signal(symbol, trend, confidence, pattern)
                results.append(formatted_signal)
            else:
                results.append(f"⚠️ Keine Analyse-Daten für {symbol}")

        except Exception as e:
            # Fehlerbehandlung bei der Analyse jedes Symbols
            print(f"[ERROR] Fehler bei der Analyse von {symbol}: {e}")
            results.append(f"⚠️ Fehler bei der Analyse von {symbol}")

    # Alle Signale in einer Nachricht zusammenfassen
    message = "\n\n".join(results)

    # Sende das Ergebnis der Analyse zurück an den Benutzer
    await update.message.reply_markdown(message)

# CommandHandler für den /signal Befehl
signal_handler = CommandHandler("signal", signal)
