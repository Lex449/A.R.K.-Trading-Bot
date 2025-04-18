from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime
import pytz

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bali_time = datetime.now(pytz.timezone("Asia/Makassar")).strftime('%H:%M:%S')
    message = (
        "📊 *A.R.K. Status Check*\n"
        "------------------------------\n"
        "🧠 *Modus:* Live | Mentor aktiviert\n"
        f"⏰ *Bali-Zeit:* {bali_time}\n"
        "⚙️ *Version:* 1.0.0\n"
        "⭐ *Stabilität:* Hoch\n"
        "📩 *Ping:* ✅\n"
        "------------------------------\n"
        "_Ich bin bereit, Daniel._"
    )
    await update.message.reply_markdown(message)