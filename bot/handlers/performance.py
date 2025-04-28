"""
A.R.K. Performance Metrics – Ultra Stable Handlers.
Delivers real-time session statistics and win/loss breakdown.
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.analytics.performance_tracker import get_performance_summary
from bot.analytics.win_loss_report import generate_win_loss_report
from bot.utils.error_reporter import report_error
from bot.utils.logger import setup_logger
from bot.utils.language import get_language
from bot.utils.i18n import get_text

# Setup structured logger
logger = setup_logger(__name__)

async def performance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler for /performance command.
    Provides clean, real-time session stats in the user's language.
    """
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"
    lang = get_language(chat_id) or "en"

    try:
        # Retrieve the performance summary and send the response
        summary = get_performance_summary(lang)
        await update.message.reply_text(summary, parse_mode="Markdown")
        logger.info(f"[Performance] Report sent to {user} (Chat ID: {chat_id})")

    except Exception as e:
        # Handle any errors during the performance command
        await report_error(context.bot, chat_id, e, context_info="Performance Command Error")
        logger.error(f"[Performance Error] {e}")

async def winloss(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler for /winloss command.
    Sends a win/loss overview with motivation message.
    """
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"
    lang = get_language(chat_id) or "en"

    try:
        # Generate the win/loss report and send it
        report = generate_win_loss_report(lang)
        await update.message.reply_text(report, parse_mode="Markdown")
        logger.info(f"[WinLoss] Report sent to {user} (Chat ID: {chat_id})")

    except Exception as e:
        # Handle any errors during the win/loss command
        await report_error(context.bot, chat_id, e, context_info="WinLoss Command Error")
        logger.error(f"[WinLoss Error] {e}")
