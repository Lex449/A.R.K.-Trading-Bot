# bot/auto/daily_analysis_job.py

"""
A.R.K. Ultra Daily Analysis Job
– Motivierende tägliche Marktanalyse auf CEO-Niveau.
– Designed für präzise Chancen und starke Lernkurven.
"""

import asyncio
import logging
from telegram import Bot
from telegram.ext import ContextTypes
from bot.engine.analysis_engine import analyze_symbol
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings
from bot.utils.logger import setup_logger

# Setup Logger
logger = setup_logger(__name__)

# Load Config
config = get_settings()

async def daily_analysis_job(context: ContextTypes.DEFAULT_TYPE):
    """
    Täglicher Ultra-Check aller Symbole mit motivierendem Abschlussbericht.
    """
    bot: Bot = context.bot
    chat_id = int(config["TELEGRAM_CHAT_ID"])

    try:
        logger.info("[Daily Analysis] Starting daily ultra-analysis...")
        await bot.send_message(chat_id=chat_id, text="📈 *Starting Daily Market Scan...*\nStay sharp. Stay hungry.", parse_mode="Markdown")

        symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
        if not symbols:
            logger.error("[Daily Analysis] No symbols configured.")
            await bot.send_message(chat_id=chat_id, text="⚠️ *No symbols configured for analysis.*", parse_mode="Markdown")
            return

        hits = []

        for symbol in symbols:
            try:
                result = await analyze_symbol(symbol)

                if not result:
                    logger.info(f"[Daily Analysis] No data for {symbol}. Skipped.")
                    continue

                if result.get("combined_action") == "Neutral ⚪":
                    logger.info(f"[Daily Analysis] {symbol} → Neutral. Skipped.")
                    continue

                hits.append(
                    f"➔ `{symbol}`: {result.get('combined_action')} – {result.get('avg_confidence', 0):.1f}% Confidence"
                )

                await asyncio.sleep(1.2)

            except Exception as symbol_error:
                logger.error(f"[Daily Analysis] Error for {symbol}: {symbol_error}")
                await report_error(bot, chat_id, symbol_error, context_info=f"Daily Analysis {symbol}")

        if hits:
            summary = "\n".join(hits)
            message = (
                f"🚀 *Daily Market Opportunities:*\n\n"
                f"{summary}\n\n"
                f"🧠 *Remember:* Quality setups, disciplined execution.\n"
                f"_Another step closer to mastery._"
            )
        else:
            message = (
                "🔎 *Daily Market Scan Completed.*\n\n"
                "No strong opportunities today.\n"
                "🧠 _Patience is a position too._"
            )

        await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
        logger.info("[Daily Analysis] Completed and results sent.")

    except Exception as e:
        logger.critical(f"[Daily Analysis Fatal Error] {e}")
        await report_error(bot, chat_id, e, context_info="Fatal Daily Analysis Job Error")
