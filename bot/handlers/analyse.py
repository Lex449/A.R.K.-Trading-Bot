from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.utils.analysis import analyze_symbol
from bot.config.settings import get_settings

analyse_handler = CommandHandler("analyse", lambda update, context: analyse(update, context))

async def analyse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    settings = get_settings()
    symbols = list(settings["SYMBOLS"].keys())

    header = "🧠 *A.R.K. LIVE-MARKTÜBERSICHT*\n_Einschätzung aller beobachteten ETFs_\n\n"
    response = [header]

    for symbol in symbols:
        result = analyze_symbol(symbol)
        if not result:
            response.append(f"❌ *{symbol}*: _Keine Daten oder Analyse derzeit nicht möglich._\n")
            continue

        signal = result.get("signal", "—")
        trend = result.get("trend", "—")
        rsi = float(result.get("rsi", 0))
        pattern = result.get("pattern", "—")

        # === Sternebewertung ===
        confidence = 0
        reason = ""

        if signal == "LONG":
            if rsi < 30:
                confidence = 5
                reason = "Überverkauft & bullisch – klare Long-Chance."
            elif rsi < 40:
                confidence = 4
                reason = "Solider Aufwärtstrend – Long möglich."
            else:
                confidence = 3
                reason = "Leichter Vorteil für Long – abwarten möglich."
        elif signal == "SHORT":
            if rsi > 70:
                confidence = 5
                reason = "Überkauft & bärisch – Short-Setup ideal."
            elif rsi > 60:
                confidence = 4
                reason = "Korrektur wahrscheinlich – Short denkbar."
            else:
                confidence = 2
                reason = "Vorsichtiger Abwärtstrend – aber unsicher."
        else:
            confidence = 1
            reason = "Kein Signal – Markt derzeit neutral oder unklar."

        stars = "⭐️" * confidence + "✩" * (5 - confidence)
        arrow = "📈" if signal == "LONG" else "📉" if signal == "SHORT" else "➖"

        response.append(
            f"*{symbol}* {arrow}\n"
            f"> *Signal:* `{signal}`\n"
            f"> *Trend:* {trend}\n"
            f"> *RSI:* {rsi:.2f}\n"
            f"> *Muster:* {pattern}\n"
            f"> *Qualität:* {stars}\n"
            f"> _{reason}_\n"
        )

    await update.message.reply_text(
        "\n".join(response),
        parse_mode="Markdown"
    )