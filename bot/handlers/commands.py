from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.language import get_language
from bot.engine.analysis_engine import analyze_symbol
from bot.utils.i18n import get_text
import logging

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Startet den Bot und begrüßt den User."""
    user = update.effective_user.first_name or "Trader"
    lang = get_language(update)  # Bestimmt die Sprache des Benutzers
    greeting = get_text("start", lang).format(user=user)  # Begrüßung basierend auf der Sprache
    help_text = get_text("help", lang)  # Hilfetext basierend auf der Sprache
    await update.message.reply_text(f"{greeting}\n\n{help_text}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gibt eine Übersicht aller verfügbaren Befehle zurück."""
    lang = get_language(update)  # Bestimmt die Sprache des Benutzers
    help_text = get_text("help", lang)  # Hilfetext basierend auf der Sprache
    await update.message.reply_text(help_text)

async def analyse_symbol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Analysiert ein einzelnes Symbol und gibt Bewertung zurück."""
    lang = get_language(update)  # Bestimmt die Sprache des Benutzers
    if not context.args:  # Überprüfen, ob ein Symbol übergeben wurde
        await update.message.reply_text(get_text("analysis_no_symbol", lang))  # Fehlermeldung, wenn kein Symbol angegeben wurde
        return

    symbol = context.args[0].upper()  # Symbol wird in Großbuchstaben konvertiert

    try:
        result = await analyze_symbol(symbol)  # Die Symbolanalyse durchführen
        if isinstance(result, str):  # Falls das Ergebnis ein String ist, wird es direkt zurückgegeben
            await update.message.reply_text(result, parse_mode="Markdown")
        else:
            response = f"Symbol: {symbol}\n"  # Ausgabe der Analyse-Ergebnisse
            response += f"Signal: {result['signal']}\n"
            response += f"RSI: {result['rsi']}\n"
            response += f"Trend: {result['trend']}\n"
            response += f"Pattern: {result['pattern']}\n"
            response += f"Stars: {result['stars']}/5"
            await update.message.reply_text(response, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"[Analyse Fehler] {symbol}: {e}")  # Loggt den Fehler, falls die Analyse fehlschlägt
        await update.message.reply_text(get_text("analysis_error", lang).format(symbol=symbol))  # Fehlermeldung bei Fehler

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Setzt manuell die Sprache auf 'de' oder 'en'."""
    if not context.args:
        await update.message.reply_text("Please provide a language code (e.g. 'de' or 'en').")
        return

    choice = context.args[0].lower()
    if choice in ("de", "deutsch"):  # Wenn 'de' oder 'deutsch' gewählt wird
        lang = "de"
    elif choice in ("en", "english"):  # Wenn 'en' oder 'english' gewählt wird
        lang = "en"
    else:
        await update.message.reply_text("Unknown language. Options: 'de', 'en'.")
        return

    context.user_data["lang"] = lang  # Speichert die Sprache des Benutzers
    confirmation = get_text("set_language", lang)  # Bestätigungstext je nach Sprache
    await update.message.reply_text(confirmation)
