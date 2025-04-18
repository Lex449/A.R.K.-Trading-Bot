from aiogram import Bot
import asyncio
import sys

async def notify_and_exit(bot_token, telegram_id, missing_var):
    try:
        bot = Bot(token=bot_token)
        await bot.send_message(
            chat_id=telegram_id,
            text=f"⚠️ *A.R.K. Fehler:* Die Umgebungsvariable `{missing_var}` fehlt.\nBitte in Railway → Variables eintragen."
        )
        await bot.session.close()
    except Exception as e:
        print(f"Telegram-Warnung fehlgeschlagen: {e}")
    finally:
        print(f"❌ Bot wird beendet – fehlende Variable: {missing_var}")
        sys.exit(1)