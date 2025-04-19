from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.utils.analysis import analyse_market
from bot.utils.language import get_language

async def analyse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_language(update)

    # Lade-Text während der Analyse
    loading_text = {
        "de": "⏳ Ich analysiere den Markt in Echtzeit... bitte einen Moment Geduld.",
        "en": "⏳ Analyzing the market in real time... please wait a moment."
    }

    await update.message.reply_text(loading_text[lang])

    # Durchführung der Marktanalyse
    result = analyse_market()

    if result is None:
        fallback = {
            "de": "⚠️ Kein klares Setup gefunden. Geduld ist auch eine Position.",
            "en": "⚠️ No clear setup found. Patience is a position too."
        }
        await update.message.reply_text(fallback[lang])
        return

    # Signal-Details aus dem Analyse-Ergebnis
    direction = result["trend"]
    confidence = result["confidence"]
    pattern = result.get("pattern", "Unbekannt")
    stars = "⭐️" * confidence + "✩" * (5 - confidence)

    # Zusätzliche Details der Analyse, z.B. RSI, MACD oder andere Indikatoren
    extra_info = result.get("extra_info", "Keine zusätzlichen Informationen verfügbar.")
    
    # Detaillierte Nachrichten für den Nutzer (Deutsch/Englisch)
    messages = {
        "de": (
            f"📊 *Analyse abgeschlossen!*\n"
            f"------------------------------\n"
            f"📈 *Trendrichtung:* `{direction.upper()}`\n"
            f"🕵️ *Erkanntes Muster:* `{pattern}`\n"
            f"⭐ *Signalqualität:* {stars}\n"
            f"📉 *Zusätzliche Analyse:* {extra_info}\n"
            f"------------------------------\n"
            f"_Bleib fokussiert, Daniel. Timing schlägt alles._"
        ),
        "en": (
            f"📊 *Analysis complete!*\n"
            f"------------------------------\n"
            f"📈 *Trend direction:* `{direction.upper()}`\n"
            f"🕵️ *Recognized pattern:* `{pattern}`\n"
            f"⭐ *Signal quality:* {stars}\n"
            f"📉 *Additional Analysis:* {extra_info}\n"
            f"------------------------------\n"
            f"_Stay sharp, Daniel. Timing beats everything._"
        )
    }

    # Sende die Antwort zurück an den Nutzer
    await update.message.reply_markdown(messages[lang])

# Erstelle den Handler für den /analyse-Befehl
analyse_handler = CommandHandler("analyse", analyse)