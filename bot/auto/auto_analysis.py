# bot/auto/auto_analysis.py

import os
import json
import asyncio
from bot.engine.analysis_engine import analyze_symbol
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.autoscaler import run_autoscaler
from telegram.ext import ContextTypes

async def daily_analysis_job(context: ContextTypes.DEFAULT_TYPE):
    """
    Wird täglich automatisch ausgelöst:
    Sendet eine kompakte Analyse der wichtigsten Symbole.
    """
    bot = context.bot
    chat_id = int(os.getenv("TELEGRAM_CHAT_ID"))

    # Auto-Scaler zuerst prüfen
    await run_autoscaler(bot, chat_id)

    # Symbole aus Umgebungsvariablen holen
    symbols_env = os.getenv("AUTO_SIGNAL_SYMBOLS", "")
    symbols = [s.strip() for s in symbols_env.split(",") if s.strip()]

    if not symbols:
        await bot.send_message(chat_id=chat_id, text="❌ Keine Symbole für Auto-Analyse definiert.")
        return

    # Sprache erkennen (default Deutsch)
    lang = "de"

    await bot.send_message(chat_id=chat_id, text="📊 Starte tägliche Analyse...")

    # Symbole analysieren
    for symbol in symbols:
        try:
            result = await analyze_symbol(symbol, lang=lang)
            await bot.send_message(chat_id=chat_id, text=result)
            await asyncio.sleep(1.5)  # Kleiner Delay, damit Telegram nicht throttelt
        except Exception as e:
            await bot.send_message(chat_id=chat_id, text=f"⚠️ Fehler bei {symbol}: {e}")

    await bot.send_message(chat_id=chat_id, text="✅ Tägliche Analyse abgeschlossen!")
