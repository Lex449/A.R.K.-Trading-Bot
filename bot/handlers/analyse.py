import requests
from telegram import Update
from telegram.ext import ContextTypes
import os

# Deinen TwelveData-API-Key hier fest eintragen oder aus ENV lesen
API_KEY = "0dd4ddf44b144ea48df01c9fdfc80921"
SYMBOLS = {
    "US100": "NDX",
    "Dow Jones": "DJI",
    "DAX": "DE30",
    "Bitcoin": "BTC/USD"
}

async def analyse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = update.effective_user.language_code
    messages = []

    for name, symbol in SYMBOLS.items():
        url = f"https://api.twelvedata.com/technical_indicator?symbol={symbol}&interval=15min&type=rsi&apikey={API_KEY}"
        ema_url = f"https://api.twelvedata.com/ema?symbol={symbol}&interval=15min&time_period=20&apikey={API_KEY}"
        price_url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={API_KEY}"

        try:
            rsi = float(requests.get(url).json()["values"][0]["rsi"])
            ema = float(requests.get(ema_url).json()["values"][0]["ema"])
            price = float(requests.get(price_url).json()["price"])
        except Exception:
            continue  # Fehlerhafter Markt wird übersprungen

        signal = "Neutral"
        stars = 3

        if rsi < 30 and price > ema:
            signal = "Long"
            stars = 4 if rsi < 25 else 3
        elif rsi > 70 and price < ema:
            signal = "Short"
            stars = 4 if rsi > 75 else 3
        elif rsi < 20:
            signal = "Strong Long"
            stars = 5
        elif rsi > 80:
            signal = "Strong Short"
            stars = 5

        emoji = "📈" if "Long" in signal else "📉" if "Short" in signal else "⚖️"
        star_str = "★" * stars + "☆" * (5 - stars)

        if lang == "de":
            messages.append(
                f"*{name} Analyse {emoji}*\n"
                f"• Signal: *{signal}*\n"
                f"• RSI: `{rsi}`\n"
                f"• EMA: `{ema}`\n"
                f"• Preis: `{price}`\n"
                f"• Stärke: {star_str}\n"
            )
        else:
            messages.append(
                f"*{name} Analysis {emoji}*\n"
                f"• Signal: *{signal}*\n"
                f"• RSI: `{rsi}`\n"
                f"• EMA: `{ema}`\n"
                f"• Price: `{price}`\n"
                f"• Strength: {star_str}\n"
            )

    if not messages:
        await update.message.reply_text("❌ No data available. Please try again later.")
    else:
        await update.message.reply_markdown("\n".join(messages), disable_web_page_preview=True)