"""
A.R.K. Performance Metrics – Ultra Stable Wall Street Edition.
Delivers real-time session performance and win/loss breakdown with flawless resilience.
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
    Handles the /performance command.
    Provides a real-time session performance overview.
    """
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"
    lang = get_language(chat_id) or "en"

    try:
        # Fetch performance summary
        summary = get_performance_summary(lang)

        await update.message.reply_text(
            summary,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

        logger.info(f"[Performance] Sent performance report to {user} (Chat ID: {chat_id}).")

    except Exception as e:
        await report_error(context.bot, chat_id, e, context_info="Performance Command Error")
        logger.error(f"[Performance] Critical error: {e}")

async def winloss(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the /winloss command.
    Delivers win/loss ratio overview and motivational feedback.
    """
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"
    lang = get_language(chat_id) or "en"

    try:
        # Fetch win/loss report
        report = generate_win_loss_report(lang)

        await update.message.reply_text(
            report,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

        logger.info(f"[WinLoss] Sent win/loss report to {user} (Chat ID: {chat_id}).")

    except Exception as e:
        await report_error(context.bot, chat_id, e, context_info="WinLoss Command Error")
        logger.error(f"[WinLoss] Critical error: {e}")
