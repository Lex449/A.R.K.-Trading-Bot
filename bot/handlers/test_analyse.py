# bot/handlers/test_analyse.py

"""
Full Ultra Premium Analyse-Command für A.R.K. Bot.
Dynamisch, motivierend, branding-ready, 100 % stabil.
"""

from telegram import Update
from telegram.ext import ContextTypes
from bot.engine.analysis_engine import analyze_symbol
from bot.engine.risk_manager import assess_signal_risk
import re

async def test_analyse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if user provided a symbol
    if not context.args:
        await update.message.reply_text(
            "❗ Bitte gib ein Symbol an. Beispiel: `/testanalyse AAPL`",
            parse_mode="MarkdownV2"
        )
        return

    symbol = context.args[0].upper()

    # Validate symbol: only A-Z and max 5 chars (typisch für Stocks)
    if not re.match(r"^[A-Z]{1,5}$", symbol):
        await update.message.reply_text(
            "❗ Ungültiges Symbol. Bitte nur Buchstaben A-Z eingeben (maximal 5 Zeichen).",
            parse_mode="MarkdownV2"
        )
        return

    result = await analyze_symbol(symbol)

    if not result:
        await update.message.reply_text(
            f"❌ Keine Analyse-Daten für `{symbol}` verfügbar.",
            parse_mode="MarkdownV2"
        )
        return

    # Risk-Analyse
    risk_message, _ = await assess_signal_risk(result)

    # Dynamische Emojis
    action = result.get('combined_action', 'Neutral ⚪')
    action_emoji = "📈" if "Long" in action else "📉" if "Short" in action else "⚪"

    avg_conf = result.get('avg_confidence', 0)
    if avg_conf >= 75:
        confidence_emoji = "🔥"
    elif avg_conf >= 60:
        confidence_emoji = "⚡"
    else:
        confidence_emoji = "⚠️"

    # Abschluss-Motivation
    if avg_conf >= 75:
        final_remark = "🚀 _Starke Tradingchance entdeckt!_" 
    elif avg_conf >= 60:
        final_remark = "⚡ _Gute Setuplage gefunden._"
    else:
        final_remark = "⚠️ _Nur schwache Basis. Risk Management empfohlen._"

    # Muster-Details schön auflisten
    pattern_list = ""
    for pattern_text in result.get("patterns", []):
        pattern_list += f"• {pattern_text}\\n"

    if not pattern_list:
        pattern_list = "_Keine hochwertigen Muster erkannt._\\n"

    # Premium Analyse-Message bauen
    analysis_message = (
        f"🚀 *A.R.K. Premium Analyse*\n\n"
        f"*Symbol:* `{symbol}`\n"
        f"*Aktion:* {action} {action_emoji}\n"
        f"*Durchschnittliche Confidence:* `{avg_conf:.1f}\\%` {confidence_emoji}\n"
        f"*Erkannte Muster:* `{result.get('pattern_count', 0)}`\n\n"
        f"{pattern_list}\n"
        f"{risk_message}\n\n"
        f"{final_remark}\n\n"
        f"🔔 _A.R.K. – Qualität vor Quantität._"
    )

    await update.message.reply_text(analysis_message, parse_mode="MarkdownV2")
