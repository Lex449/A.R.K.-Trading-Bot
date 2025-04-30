import asyncio
from telegram import Bot

# === Dein echter Bot Token – NICHT ändern
BOT_TOKEN = "7859748584:AAGMbG2dLKD5da1xOqBkwh5VxmfYpdzeWXE"

async def fix_webhook():
    bot = Bot(token=BOT_TOKEN)
    await bot.delete_webhook(drop_pending_updates=True)
    print("✅ Webhook erfolgreich entfernt.")

if __name__ == "__main__":
    asyncio.run(fix_webhook())
