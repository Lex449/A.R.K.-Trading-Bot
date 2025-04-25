from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.i18n import get_text
from bot.engine.analysis import analyze_symbol as engine_analyze
import logging

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler für den /start-Befehl."""
    user = update.effective_user.first_name or ""
    lang = context.user_data.get("lang") or update.effective_user.language_code
    if lang not in ("de", "en"):
        lang = "de" if lang.startswith("de") else "en"
    greeting = get_text("start", lang).format(user=user)
    help_text = get_text("help", lang)
    await update.message.reply_text(f"{greeting}\n\n{help_text}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler für den /help-Befehl."""
    lang = context.user_data.get("lang") or update.effective_user.language_code
    if lang not in ("de", "en"):
        lang = "de" if lang.startswith("de") else "en"
    help_text = get_text("help", lang)
    await update.message.reply_text(help_text)

async def analyse_symbol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler für den /analyse-Befehl."""
    lang = context.user_data.get("lang") or update.effective_user.language_code
    if lang not in ("de", "en"):
        lang = "de" if lang.startswith("de") else "en"
    if not context.args:
        text = get_text("analysis_no_symbol", lang)
        await update.message.reply_text(text)
        return
    symbol = context.args[0].upper()
    try:
        result = await engine_analyze(symbol, lang=lang)
        await update.message.reply_text(result)
    except Exception as e:
        logger.error(f"Fehler bei der Analyse von {symbol}: {e}")
        error_text = get_text("analysis_error", lang).format(symbol=symbol)
        await update.message.reply_text(error_text)

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler für den /setlanguage-Befehl."""
    if not context.args:
        await update.message.reply_text("Bitte geben Sie eine Sprache an (z.B. 'de' oder 'en').")
        return
    choice = context.args[0].lower()
    if choice in ("de", "deutsch"):
        lang = "de"
    elif choice in ("en", "englisch"):
        lang = "en"
    else:
        await update.message.reply_text("Unbekannte Sprache. Verfügbare Optionen: 'de', 'en'.")
        return
    context.user_data["lang"] = lang
    confirmation = get_text("set_language", lang)
    await update.message.reply_text(confirmation)