from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.language import get_language
from bot.engine.analysis_engine import analyze_symbol
from bot.utils.i18n import get_text
import logging

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Startet den Bot und begrüßt den User mit einer individuell gestalteten Nachricht."""
    user = update.effective_user.first_name or "Trader"
    lang = get_language(update)  # Bestimmt die Sprache des Benutzers
    greeting = get_text("start", lang).format(user=user)  # Dynamische Begrüßung basierend auf der Sprache
    help_text = get_text("help", lang)  # Hilfe-Bereich in der jeweiligen Sprache

    # Logge die Benutzerinteraktion für späteres Debugging
    logger.info(f"Start command initiated by {user} ({lang})")
    await update.message.reply_text(f"{greeting}\n\n{help_text}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gibt eine vollständige Übersicht der verfügbaren Befehle zurück."""
    lang = get_language(update)  # Bestimmt die Sprache des Benutzers
    help_text = get_text("help", lang)  # Hilfe-Text je nach Sprache

    # Logge den Befehl zur Nachverfolgung
    logger.info(f"Help command invoked by {update.effective_user.first_name}")
    await update.message.reply_text(help_text)

async def analyse_symbol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Analysiert das angegebene Symbol und gibt die Ergebnisse zurück."""
    lang = get_language(update)  # Bestimmt die Sprache des Benutzers

    # Überprüfe, ob ein Symbol angegeben wurde
    if not context.args:
        logger.warning(f"No symbol provided in /analyse by {update.effective_user.first_name}")
        await update.message.reply_text(get_text("analysis_no_symbol", lang))  # Fehlermeldung, wenn kein Symbol übergeben wurde
        return

    symbol = context.args[0].upper()  # Konvertiere das Symbol in Großbuchstaben

    try:
        result = await analyze_symbol(symbol)  # Analysiere das Symbol
        if isinstance(result, str):  # Falls das Ergebnis ein String ist, direkt zurückgeben
            await update.message.reply_text(result, parse_mode="Markdown")
        else:
            # Formatiere und sende die Analyseergebnisse
            response = (f"Symbol: {symbol}\n"
                        f"Signal: {result['signal']}\n"
                        f"RSI: {result['rsi']}\n"
                        f"Trend: {result['trend']}\n"
                        f"Pattern: {result['pattern']}\n"
                        f"Stars: {result['stars']}/5")
            await update.message.reply_text(response, parse_mode="Markdown")
            logger.info(f"Analysis completed for {symbol} by {update.effective_user.first_name}")
    except Exception as e:
        logger.error(f"[Analysis Error] {symbol}: {e}")  # Logge alle Analysefehler
        await update.message.reply_text(get_text("analysis_error", lang).format(symbol=symbol))  # Fehlermeldung im Fehlerfall

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Setzt die Sprache des Benutzers auf 'de' oder 'en'."""
    if not context.args:
        await update.message.reply_text("Please provide a language code (e.g. 'de' or 'en').")
        return

    choice = context.args[0].lower()
    if choice in ("de", "deutsch"):  # Setzt die Sprache auf Deutsch
        lang = "de"
    elif choice in ("en", "english"):  # Setzt die Sprache auf Englisch
        lang = "en"
    else:
        await update.message.reply_text("Unknown language. Options: 'de', 'en'.")
        return

    # Speichert die gewählte Sprache
    context.user_data["lang"] = lang  
    confirmation = get_text("set_language", lang)  # Bestätigungstext basierend auf der Sprache
    logger.info(f"Language change request from {update.effective_user.first_name} to {lang}")
    await update.message.reply_text(confirmation)
