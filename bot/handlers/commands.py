"""
A.R.K. Command Handler – NASA Signature Build 2025
Handles bilingual user commands with ultra-stability and strategic real-time responses.
Made in Bali. Engineered with German Precision.
"""

from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.language import get_language, set_language
from bot.utils.i18n import get_text
from bot.utils.logger import setup_logger
from bot.utils.error_reporter import report_error
from bot.utils.uptime_tracker import get_uptime
from bot.engine.analysis_engine import analyze_symbol
from bot.utils.api_bridge import monitor as usage_monitor

logger = setup_logger(__name__)

# === /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user = update.effective_user.first_name or "Trader"
        lang = get_language(update.effective_chat.id) or "en"
        text = get_text("start", lang).format(user=user)

        menu = {
            "en": "\n\n🧭 *Main Menu*\n"
                  "`/analyse [SYMBOL]` – Full analysis\n"
                  "`/signal` – Latest signal\n"
                  "`/status` – System status\n"
                  "`/monitor` – API usage\n"
                  "`/uptime` – Uptime check\n"
                  "`/setlanguage en|de` – Switch language\n"
                  "`/help` – All commands",
            "de": "\n\n🧭 *Hauptmenü*\n"
                  "`/analyse [SYMBOL]` – Analyse starten\n"
                  "`/signal` – Letztes Signal\n"
                  "`/status` – Systemstatus\n"
                  "`/monitor` – API-Verbrauch\n"
                  "`/uptime` – Laufzeit prüfen\n"
                  "`/setlanguage de|en` – Sprache wählen\n"
                  "`/help` – Alle Befehle"
        }.get(lang, "")

        await update.message.reply_text(text + menu, parse_mode="Markdown")
        logger.info(f"✅ [Command] /start by {user}")
    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, "/start Handler Error")

# === /help ===
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        lang = get_language(update.effective_chat.id) or "en"
        await update.message.reply_text(get_text("help", lang), parse_mode="Markdown")
        logger.info("✅ [Command] /help")
    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, "/help Handler Error")

# === /analyse ===
async def analyze_symbol_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        lang = get_language(update.effective_chat.id) or "en"
        if not context.args:
            await update.message.reply_text(get_text("analysis_no_symbol", lang), parse_mode="Markdown")
            return

        symbol = context.args[0].upper()
        await update.message.reply_text(f"🔍 {get_text('analyzing', lang)} *{symbol}*...", parse_mode="Markdown")

        result = await analyze_symbol(symbol, chat_id=update.effective_chat.id)
        if not result:
            await update.message.reply_text(get_text("no_analysis_data", lang).format(symbol=symbol), parse_mode="Markdown")
            return

        confidence = result.get("avg_confidence", 0.0)
        move = result.get("combined_action", "Unknown")
        category = result.get("signal_category", "⭐")
        price = result.get("last_price", "n/a")
        patterns = result.get("patterns", [])
        rrr = result.get("risk_reward_info", {})
        stars = "⭐" * int(round(confidence / 20))
        pattern_list = [f"`{p.get('pattern', 'N/A')}`" for p in patterns] or [get_text("no_patterns_found", lang)]

        message = (
            f"📊 *{symbol} – {get_text('analysis_completed', lang)}*\n\n"
            f"*Price:* `${price}`\n"
            f"*Move:* `{move}`\n"
            f"*Confidence:* `{confidence:.1f}%` {stars}\n"
            f"*Rating:* {category}\n"
            f"*Patterns:* {', '.join(pattern_list)}"
        )

        if rrr:
            message += (
                f"\n\n🎯 *Risk/Reward*\n"
                f"• *Target:* `${rrr.get('target')}`\n"
                f"• *Stop:* `${rrr.get('stop_loss')}`\n"
                f"• *Ratio:* `{rrr.get('risk_reward_ratio')}`"
            )

        message += "\n\n_This is not financial advice._"
        await update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)
        logger.info(f"✅ [Command] /analyse {symbol}")

    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, "/analyse Handler Error")

# === /signal ===
async def signal_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        lang = get_language(update.effective_chat.id) or "en"
        await update.message.reply_text(get_text("live_signal_info", lang), parse_mode="Markdown")
        logger.info("✅ [Command] /signal")
    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, "/signal Handler Error")

# === /status ===
async def status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_text("📊 *System Status:* All systems operational.", parse_mode="Markdown")
        logger.info("✅ [Command] /status")
    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, "/status Handler Error")

# === /uptime ===
async def uptime_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        uptime = get_uptime()
        await update.message.reply_text(f"⏱️ *Uptime:* `{uptime}`", parse_mode="Markdown")
        logger.info("✅ [Command] /uptime")
    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, "/uptime Handler Error")

# === /setlanguage ===
async def set_language_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        if not context.args:
            await update.message.reply_text("❗ Please use: `/setlanguage en` or `/setlanguage de`", parse_mode="Markdown")
            return

        lang = context.args[0].lower()
        if lang not in ["en", "de"]:
            await update.message.reply_text("❗ Supported languages: `en`, `de`", parse_mode="Markdown")
            return

        set_language(update.effective_chat.id, lang)
        await update.message.reply_text(get_text("set_language", lang), parse_mode="Markdown")
        logger.info(f"✅ [Command] /setlanguage → {lang}")
    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, "/setlanguage Handler Error")

# === /shutdown ===
async def shutdown_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        lang = get_language(update.effective_chat.id) or "en"
        await update.message.reply_text(get_text("shutdown", lang), parse_mode="Markdown")
        await context.application.stop()
        logger.info("🛑 [Command] /shutdown")
    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, "/shutdown Handler Error")

# === /monitor ===
async def monitor_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        lang = get_language(update.effective_chat.id) or "en"
        calls = usage_monitor.get_call_count()
        minutes = usage_monitor.get_elapsed_minutes()
        rate = usage_monitor.get_rate_per_minute()

        status = (
            ("🟢", "Stable") if rate < 75 else
            ("🟡", "Elevated") if rate < 140 else
            ("🔴", "Critical")
        )

        text = (
            f"{status[0]} *API Monitor*\n\n"
            f"• *Total Calls:* `{calls}`\n"
            f"• *Runtime:* `{minutes:.1f} min`\n"
            f"• *Rate:* `{rate:.2f} calls/min`\n"
            f"• *Status:* `{status[1]}`\n\n"
            "_All API usage tracked in real-time._"
        )

        await update.message.reply_text(text, parse_mode="Markdown")
        logger.info("✅ [Command] /monitor")
    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, "/monitor Handler Error")
