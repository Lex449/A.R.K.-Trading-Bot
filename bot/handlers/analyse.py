from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.utils.analysis import analyze_symbol
from bot.config.settings import get_settings

analyse_handler = CommandHandler("analyse", lambda update, context: analyse(update, context))

async def analyse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    settings = get_settings()
    symbols = list(settings["SYMBOLS"].keys())

    top_list = []
    response = []

    for symbol in symbols:
        result = analyze_symbol(symbol)
        if not result:
            continue

        signal = result.get("signal", "—")
        trend = result.get("trend", "—")
        rsi = float(result.get("rsi", 0))
        pattern = result.get("pattern", "—")
        price = float(result.get("price", 0))
        confidence = 0
        comment = ""
        emoji = "⏳"

        if signal == "LONG":
            emoji = "🚀"
            if rsi < 40:
                confidence = 5
                comment = "Stark überverkauft – präziser Einstieg möglich."
            elif rsi < 50:
                confidence = 4
                comment = "Momentum dreht – Long denkbar."
            else:
                confidence = 3
                comment = "Leichter Vorteil – aber nicht blind reinspringen."
        elif signal == "SHORT":
            emoji = "📉"
            if rsi > 70:
                confidence = 5
                comment = "Überkauft – Short-Signal glasklar."
            elif rsi > 60:
                confidence = 4
                comment = "Momentum bricht – Short denkbar."
            else:
                confidence = 3
                comment = "Vorsicht – aber Short möglich."
        else:
            confidence = 1
            comment = "Neutral – keine klare Richtung."

        stars = "⭐️" * confidence + "✩" * (5 - confidence)

        top_list.append({
            "symbol": symbol,
            "stars": confidence,
            "signal": signal,
            "emoji": emoji,
            "price": price,
            "trend": trend,
            "rsi": rsi,
            "pattern": pattern,
            "comment": comment
        })

    # Sortiere nach Sternen absteigend
    top_list = sorted(top_list, key=lambda x: x["stars"], reverse=True)

    header = "🧠 *A.R.K. Marktanalyse (Live)*\n_Nur klare Chancen, kein Lärm._\n\n"
    ranking = [f"`TOP {i+1}`: *{entry['symbol']}* {entry['emoji']} {entry['stars']}⭐️" for i, entry in enumerate(top_list[:3])]
    body = []

    for entry in top_list:
        if entry["stars"] < 3:
            continue

        block = (
            f"*{entry['symbol']}* {entry['emoji']}\n"
            f"> *Signal:* `{entry['signal']}`\n"
            f"> *Preis:* `{entry['price']}` | *Trend:* {entry['trend']}\n"
            f"> *RSI:* {entry['rsi']:.2f} | *Muster:* {entry['pattern']}\n"
            f"> *Qualität:* {entry['stars']}⭐️\n"
            f"_→ {entry['comment']}_\n"
        )
        body.append(block)

    if not body:
        body.append("_Aktuell keine starken Setups – Markt neutral._")

    await update.message.reply_text(
        header + "\n".join(ranking) + "\n\n" + "\n".join(body),
        parse_mode="Markdown"
    )