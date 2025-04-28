"""
A.R.K. Ultra Daily Analysis Job
– Motivierende tägliche Marktanalyse auf CEO-Niveau.
– Präzisions-Upgrade 2025: Fokus auf Top-Signale & Deep Confidence Learning.
"""

import asyncio
import logging
from telegram import Bot
from telegram.ext import ContextTypes
from bot.engine.analysis_engine import analyze_symbol
from bot.engine.deep_confidence_engine import adjust_confidence  # << NEU eingebaut
from bot.utils.error_reporter import report_error
from bot.utils.session_tracker import update_session_tracker
from bot.utils.logger import setup_logger
from bot.config.settings import get_settings

# Setup Logger
logger = setup_logger(__name__)

# Load Config
config = get_settings()

async def daily_analysis_job(context: ContextTypes.DEFAULT_TYPE):
    """
    Ultra-Scan aller Symbole mit Fokus auf echte Top-Chancen
    und motivierendem, präzisem Abschlussbericht.
    """
    bot: Bot = context.bot
    chat_id = int(config["TELEGRAM_CHAT_ID"])

    try:
        logger.info("[Daily Analysis] Starting Ultra Daily Analysis...")
        await bot.send_message(
            chat_id=chat_id,
            text="📈 *Starting Daily Precision Scan...*\nBe water. Be relentless.",
            parse_mode="Markdown"
        )

        symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
        if not symbols:
            logger.error("[Daily Analysis] No symbols configured.")
            await bot.send_message(
                chat_id=chat_id,
                text="⚠️ *No symbols configured for Daily Analysis.*",
                parse_mode="Markdown"
            )
            return

        hits = []
        misses = []
        total_scanned = 0

        for symbol in symbols:
            try:
                result = await analyze_symbol(symbol)
                total_scanned += 1

                if not result:
                    logger.info(f"[Daily Analysis] {symbol} → No data. Skipped.")
                    misses.append(symbol)
                    continue

                combined_action = result.get("combined_action", "Neutral ⚪")

                # === Deep Confidence Adjustment ===
                raw_confidence = result.get("avg_confidence", 0)
                confidence = adjust_confidence(raw_confidence)

                # Nur starke Chancen aufnehmen
                if combined_action not in ["Neutral ⚪", "Hold"] and confidence >= 58:
                    hits.append(
                        f"➔ `{symbol}`: {combined_action} – {confidence:.1f}% Confidence"
                    )

                    # Update Session Tracker
                    stars = 5 if confidence >= 70 else 4 if confidence >= 65 else 3
                    update_session_tracker(stars=stars, confidence=confidence)

                else:
                    misses.append(symbol)

                await asyncio.sleep(1.2)  # Respect Telegram Rate Limit

            except Exception as symbol_error:
                logger.error(f"[Daily Analysis] Error for {symbol}: {symbol_error}")
                await report_error(bot, chat_id, symbol_error, context_info=f"Daily Analysis {symbol}")

        # Zusammenfassung
        if hits:
            summary = "\n".join(hits)
            message = (
                f"🚀 *Daily Opportunities Spotted!*\n\n"
                f"{summary}\n\n"
                f"🔎 *Scanned:* `{total_scanned}` symbols\n"
                f"⚡ *Opportunities:* `{len(hits)}` strong signals\n"
                f"🧠 *Remember:* Discipline + Consistency = Freedom.\n"
                f"_Level up every day._"
            )
        else:
            message = (
                "🔍 *Daily Scan Completed.*\n\n"
                "No high-confidence setups found today.\n"
                "🧠 _Patience is a weapon too._\n"
                f"Scanned `{total_scanned}` symbols."
            )

        await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
        logger.info("[Daily Analysis] Completed and report sent.")

    except Exception as e:
        logger.critical(f"[Daily Analysis Fatal Error] {e}")
        await report_error(bot, chat_id, e, context_info="Fatal Error Daily Analysis Job")
