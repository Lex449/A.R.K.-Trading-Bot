# bot/auto/auto_analysis.py

import asyncio
import logging
from telegram import Bot
from telegram.ext import ContextTypes
from bot.engine.analysis_engine import analyze_symbol
from bot.engine.risk_manager import assess_signal_risk
from bot.utils.session_tracker import update_session_tracker
from bot.utils.error_reporter import report_error
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.autoscaler import run_autoscaler
from bot.config.settings import get_settings
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# Load config once
config = get_settings()

async def daily_analysis_job(context: ContextTypes.DEFAULT_TYPE):
    """
    Executes a full daily market analysis on all configured symbols.
    Filters only actionable signals (buy/sell) and skips "Hold" results.
    """
    bot: Bot = context.bot
    chat_id = int(config["TELEGRAM_CHAT_ID"])
    lang = get_language(chat_id) or "en"

    try:
        logger.info("[Auto Analysis] Starting daily analysis.")
        await bot.send_message(chat_id=chat_id, text="📊 *Starting full daily analysis...*", parse_mode="Markdown")

        # Optional autoscaler execution
        try:
            await run_autoscaler(bot, chat_id)
        except Exception as e:
            logger.warning(f"[Autoscaler Error] {str(e)}")
            await report_error(bot, chat_id, e, context_info="Autoscaler during daily analysis")

        symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
        if not symbols:
            logger.error("[Auto Analysis] No symbols configured.")
            await bot.send_message(chat_id=chat_id, text="❌ No symbols defined for analysis.", parse_mode="Markdown")
            return

        for symbol in symbols:
            try:
                result = await analyze_symbol(symbol)

                if not result:
                    logger.warning(f"[Auto Analysis] No data for {symbol}.")
                    continue

                if result['signal'] == "Hold" or result['pattern'] == "No Pattern":
                    logger.info(f"[Auto Analysis] {symbol} → Hold/No pattern. Skipped.")
                    continue

                # Risk management and session tracking
                risk_message, is_warning = await assess_signal_risk(result)
                update_session_tracker(result["stars"])

                # Construct message
                message = (
                    f"📈 *Daily Analysis Signal*\n\n"
                    f"*Symbol:* `{symbol}`\n"
                    f"*Action:* {result['signal']}\n"
                    f"*Short-Term Trend:* {result['short_term_trend']}\n"
                    f"*Mid-Term Trend:* {result['mid_term_trend']}\n"
                    f"*RSI:* {result['rsi']}\n"
                    f"*Pattern:* {result['pattern']}\n"
                    f"*Candlestick:* {result['candlestick']}\n"
                    f"*Rating:* {result['stars']} ⭐\n"
                    f"*Suggested Holding:* {result['suggested_holding']}\n\n"
                    f"{risk_message}\n"
                    f"⚡ _Always manage your risk carefully._"
                )

                await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
                logger.info(f"[Auto Analysis] Signal sent for {symbol}.")

                await asyncio.sleep(1.5)  # Kleine Pause, um API-Spam zu vermeiden

            except Exception as e:
                logger.error(f"[Auto Analysis Error] Symbol: {symbol} – {str(e)}")
                await report_error(bot, chat_id, e, context_info=f"Auto Analysis error for {symbol}")

        await bot.send_message(chat_id=chat_id, text="✅ *Daily analysis completed successfully!*", parse_mode="Markdown")
        logger.info("[Auto Analysis] Completed successfully.")

    except Exception as e:
        logger.critical(f"[Auto Analysis Fatal Error] {str(e)}")
        await report_error(bot, chat_id, e, context_info="Fatal daily analysis error")
