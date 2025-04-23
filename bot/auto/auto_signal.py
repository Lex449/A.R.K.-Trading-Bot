import asyncio
from telegram import Bot
from bot.utils.analysis import analyse_market
from bot.config.settings import get_settings

async def auto_signal_loop():
    settings = get_settings()
    bot = Bot(token=settings["BOT_TOKEN"])
    chat_id = settings["DANIEL_TELEGRAM_ID"]

    symbols = ["US100/USDT", "US30/USDT", "US500/USDT"]

    while True:
        for symbol in symbols:
            try:
                result = analyse_market(symbol)

                if result:
                    trend = result["trend"]
                    confidence = result["confidence"]
                    pattern = result["pattern"]

                    if confidence >= 3:
                        stars = "⭐️" * confidence + "✩" * (5 - confidence)
                        message = (
                            f"📡 *Auto-Signal: {symbol}*\n"
                            f"Trend: *{trend}*\n"
                            f"Muster: *{pattern}*\n"
                            f"Qualität: {stars}\n\n"
                            f"_A.R.K. analysiert rund um die Uhr – nur bei klarem Vorteil._"
                        )
                        await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
                    else:
                        print(f"[Info] Signal für {symbol} erkannt, aber zu schwach ({confidence}/5)")
                else:
                    print(f"[Warnung] Keine Analyse-Daten für {symbol}")

            except Exception as e:
                print(f"[Fehler] Fehler bei der Analyse von {symbol}: {e}")

        await asyncio.sleep(300)
