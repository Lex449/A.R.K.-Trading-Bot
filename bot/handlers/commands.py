# bot/handlers/commands.py

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
    lang = get_language(update)
    greeting = get_text("start", lang).format(user=user)
    help_text = get_text("help", lang)
    await update.message.reply_text(f"{greeting}\n\n{help_text}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gibt eine Übersicht aller verfügbaren Befehle zurück."""
    lang = get_language(update)
    help_text = get_text("help", lang)
    await update.message.reply_text(help_text)

async def analyse_symbol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Analysiert ein einzelnes Symbol und gibt Bewertung zurück."""
    lang = get_language(update)
    if not context.args:
        await update.message.reply_text(get_text("analysis_no_symbol", lang))
        return

    symbol = context.args[0].upper()

    try:
        result = await analyze_symbol(symbol, lang=lang)
        await update.message.reply_text(result, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"[Analyse Fehler] {symbol}: {e}")
        await update.message.reply_text(get_text("analysis_error", lang).format(symbol=symbol))

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Setzt manuell die Sprache auf 'de' oder 'en'."""
    if not context.args:
        await update.message.reply_text("Please provide a language code (e.g. 'de' or 'en').")
        return

    choice = context.args[0].lower()
    if choice in ("de", "deutsch"):
        lang = "de"
    elif choice in ("en", "englisch"):
        lang = "en"
    else:
        await update.message.reply_text("Unknown language. Options: 'de', 'en'.")
        return

    context.user_data["lang"] = lang
    confirmation = get_text("set_language", lang)
    await update.message.reply_text(confirmation)
