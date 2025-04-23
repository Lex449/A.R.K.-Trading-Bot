import asyncio
from telegram import Bot
from bot.utils.analysis import analyze_symbol
from bot.config.settings import get_settings

async def auto_signal_loop():
    """Automatisierter Live-Signal-Loop: 5 ETFs alle 5 Minuten."""
    settings = get_settings()
    bot = Bot(token=settings["BOT_TOKEN"])
    symbols = ["QQQ", "SPY", "DIA", "IWM", "MDY"]

    while True:
        for symbol in symbols:
            try:
                result = analyze_symbol(symbol)
                if result and result.get("signal"):
                    trend = result.get("trend", "—")
                    rsi = float(result.get("rsi", 0))
                    pattern = result.get("pattern", "—")
                    stars = "⭐️" * (5 if result.get("signal") == "LONG" else 4) + "✩"

                    message = (
                        f"🧠 *A.R.K. LIVE-Signal* für {symbol}\n"
                        f"*Signal:* `{result['signal']}`\n"
                        f"*Trend:* {trend}\n"
                        f"*RSI:* {rsi:.2f}\n"
                        f"*Muster:* {pattern}\n"
                        f"*Qualität:* {stars}\n\n"
                        f"_Jede Chance nutzen – alle 5 Minuten!_"
                    )

                    await bot.send_message(
                        chat_id=settings["TELEGRAM_CHAT_ID"],
                        text=message,
                        parse_mode="Markdown"
                    )
                else:
                    print(f"[Info] Kein Signal für {symbol} oder zu schwach.")
            except Exception as e:
                print(f"[Fehler] Fehler bei {symbol}: {e}")

        await asyncio.sleep(settings["SIGNAL_CHECK_INTERVAL_SEC"])  # exakt 5 Minuten