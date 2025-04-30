"""
A.R.K. Command Handler – NASA Signature Build 2025
Handles bilingual user commands with ultra-stability and strategic real-time responses.
"""

from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.language import get_language, set_language
from bot.utils.i18n import get_text
from bot.utils.logger import setup_logger
from bot.utils.error_reporter import report_error
from bot.utils.uptime_tracker import get_uptime
from bot.engine.analysis_engine import analyze_symbol
from bot.utils.api_bridge import monitor as usage_monitor  # ✅ Einheitlicher Zugriff

logger = setup_logger(__name__)

# === /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user = update.effective_user.first_name or "Trader"
        lang = get_language(update.effective_chat.id) or "en"
        text = get_text("start", lang).format(user=user)

        menu_text = {
            "en": "\n\n🧭 *Main Menu*\n"
                  "`/analyse [SYMBOL]` – Full signal analysis\n"
                  "`/signal` – Current signal\n"
                  "`/status` – System status\n"
                  "`/monitor` – API usage\n"
                  "`/uptime` – Uptime info\n"
                  "`/setlanguage en|de` – Set language\n"
                  "`/help` – All commands",
            "de": "\n\n🧭 *Hauptmenü*\n"
                  "`/analyse [SYMBOL]` – Signal-Analyse starten\n"
                  "`/signal` – Aktuelles Signal\n"
                  "`/status` – Systemstatus\n"
                  "`/monitor` – API-Verbrauch\n"
                  "`/uptime` – Laufzeit anzeigen\n"
                  "`/setlanguage de|en` – Sprache setzen\n"
                  "`/help` – Alle Befehle"
        }.get(lang, "")

        await update.message.reply_text(text + menu_text, parse_mode="Markdown")
        logger.info(f"✅ [Command] /start executed by {user}")
    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/start Handler Error")

# === /help ===
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        lang = get_language(update.effective_chat.id) or "en"
        text = get_text("help", lang)
        await update.message.reply_text(text, parse_mode="Markdown")
        logger.info(f"✅ [Command] /help executed")
    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/help Handler Error")

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

        if result:
            confidence = result.get("avg_confidence", 0.0)
            move = result.get("combined_action", "Unknown")
            category = result.get("signal_category", "⭐")
            price = result.get("last_price", "n/a")
            patterns = result.get("patterns", [])
            rrr = result.get("risk_reward_info", {})
            stars = "⭐" * int(round(confidence / 20))

            pattern_names = [f"`{p.get('pattern', 'N/A')}`" for p in patterns]
            pattern_text = ", ".join(pattern_names) if pattern_names else get_text("no_patterns_found", lang)

            message = (
                f"📊 *{symbol} – {get_text('analysis_completed', lang)}*\n\n"
                f"*Current Price:* `${price}`\n"
                f"*Move:* `{move}`\n"
                f"*Confidence:* `{confidence:.1f}%` {stars}\n"
                f"*Signal Rating:* {category}\n"
                f"*Patterns:* {pattern_text}"
            )

            if rrr:
                message += (
                    f"\n\n🎯 *Risk/Reward*\n"
                    f"• *Target:* `${rrr.get('target')}`\n"
                    f"• *Stop:* `${rrr.get('stop_loss')}`\n"
                    f"• *RRR:* `{rrr.get('risk_reward_ratio')}`"
                )

            message += "\n\n_This is not financial advice. Use discretion._"

            await update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)
            logger.info(f"✅ [Command] /analyse → {symbol}")
        else:
            await update.message.reply_text(get_text("no_analysis_data", lang).format(symbol=symbol), parse_mode="Markdown")
            logger.warning(f"⚠️ [Command] /analyse no data for {symbol}")
    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/analyse Handler Error")

# === /signal ===
async def signal_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        lang = get_language(update.effective_chat.id) or "en"
        await update.message.reply_text(get_text("live_signal_info", lang), parse_mode="Markdown")
        logger.info(f"✅ [Command] /signal executed")
    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/signal Handler Error")

# === /status ===
async def status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_text("📊 *System Status:* Operational.\n*More details coming soon.*", parse_mode="Markdown")
        logger.info(f"✅ [Command] /status executed")
    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/status Handler Error")

# === /uptime ===
async def uptime_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        uptime = get_uptime()
        await update.message.reply_text(f"⏱️ *Uptime:* `{uptime}`", parse_mode="Markdown")
        logger.info(f"✅ [Command] /uptime executed")
    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/uptime Handler Error")

# === /setlanguage ===
async def set_language_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        if not context.args:
            await update.message.reply_text("❗ Please specify a language: `en` or `de`", parse_mode="Markdown")
            return

        lang = context.args[0].lower()
        if lang not in ["en", "de"]:
            await update.message.reply_text("❗ Supported: `en`, `de`", parse_mode="Markdown")
            return

        set_language(update.effective_chat.id, lang)
        await update.message.reply_text(get_text("set_language", lang), parse_mode="Markdown")
        logger.info(f"✅ [Command] /setlanguage changed to {lang}")
    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/setlanguage Handler Error")

# === /shutdown ===
async def shutdown_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        lang = get_language(update.effective_chat.id) or "en"
        await update.message.reply_text(get_text("shutdown", lang), parse_mode="Markdown")
        await context.application.stop()
        logger.info(f"🛑 [Command] /shutdown triggered")
    except Exception as e:
        await report_error(context.bot, update.effective_chat.id, e, context_info="/shutdown Handler Error")

# === /monitor ===
async def monitor_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        lang = get_language(update.effective_chat.id) or "en"
        call_count = usage_monitor.get_call_count()
        rate = usage_monitor.get_rate_per_minute()
        duration = usage_monitor.get_elapsed_minutes()

        if rate < 75:
            emoji = "🟢"
            comment = "Stable"
        elif rate < 140:
            emoji = "🟡"
            comment = "Caution"
        else:
            emoji = "🔴"
            comment = "CRITICAL"

        message = (
            f"{emoji} *API Usage Monitor*\n\n"
            f"*Total Calls:* `{call_count}`\n"
            f"*Uptime:* `{duration:.1f} min`\n"
            f"*Calls/min:* `{rate:.2f}`\n"
            f"*Status:* `{comment}`\n\n"
            "_Auto-monitoring is active._"
        )

        await update.message.reply_text(message, parse_mode="Markdown")
        logger.info(f"✅ [Command] /monitor executed")
    except Exception as e:
        logger.error(f"[Command] /monitor failed: {e}")
        await update.message.reply_text("⚠️ Error while loading monitor status.")
