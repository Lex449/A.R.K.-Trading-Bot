# bot/auto/auto_analysis.py

import os
import json
import asyncio
from telegram import Bot
from telegram.ext import ContextTypes
from bot.engine.analysis_engine import analyze_symbol
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.autoscaler import run_autoscaler
from bot.config.settings import get_settings

config = get_settings()

async def daily_analysis_job(context: ContextTypes.DEFAULT_TYPE):
    """
    Führt täglich eine kompakte Analyse aller überwachten Indizes durch
    und sendet die Ergebnisse automatisch an den Telegram-Chat.
    """
    bot: Bot = context.bot
    chat_id = int(config["TELEGRAM_CHAT_ID"])
    lang = "de"  # Standard (später optional dynamisch je Gruppe)

    await bot.send_message(chat_id=chat_id, text="📊 *Starte tägliche Analyse...*", parse_mode="Markdown")

    try:
        await run_autoscaler(bot, chat_id)
    except Exception as e:
        await bot.send_message(chat_id=chat_id, text=f"⚠️ Fehler beim Autoscaler: {e}")

    symbols = config["AUTO_SIGNAL_SYMBOLS"]
    if not symbols:
        await bot.send_message(chat_id=chat_id, text="❌ Keine Symbole für Auto-Analyse definiert.")
        return

    for symbol in symbols:
        try:
            result = await analyze_symbol(symbol, lang=lang)
            await bot.send_message(chat_id=chat_id, text=result, parse_mode="Markdown")
            await asyncio.sleep(1.5)  # Telegram Throttle-Puffer
        except Exception as e:
            await bot.send_message(chat_id=chat_id, text=f"⚠️ Fehler bei {symbol}: {e}")

    await bot.send_message(chat_id=chat_id, text="✅ *Tägliche Analyse abgeschlossen!*", parse_mode="Markdown")
