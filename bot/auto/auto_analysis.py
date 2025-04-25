import os
import json
import logging
from telegram.ext import ContextTypes
from bot.engine.analysis import analyze_symbol

logger = logging.getLogger(__name__)

async def run_auto_analysis(context: ContextTypes.DEFAULT_TYPE):
    """
    Führt automatisch die Analyse aller Symbolgruppen durch und sendet Ergebnisse an einen Chat.
    Dieser Job wird täglich ausgeführt.
    """
    chat_id = context.job.context
    # Pfad zur Gruppen-Konfigurationsdatei
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config", "groups.json"))
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            groups = json.load(f)
    except Exception as e:
        logger.error("Konnte Gruppen-Konfigurationsdatei nicht laden: %s", e)
        return

    # Jede Gruppe verarbeiten
    for group_name, symbols in groups.items():
        header = f"Automatische Analyse für Gruppe: {group_name}"
        await context.bot.send_message(chat_id=chat_id, text=header)
        for symbol in symbols:
            try:
                result = await analyze_symbol(symbol, lang="de")
                await context.bot.send_message(chat_id=chat_id, text=result)
            except Exception as e:
                logger.error("Fehler bei automatischer Analyse von %s: %s", symbol, e)
                await context.bot.send_message(chat_id=chat_id, text=f"Analyse für {symbol} fehlgeschlagen.")