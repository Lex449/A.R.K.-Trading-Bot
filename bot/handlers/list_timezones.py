import pytz
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.error_reporter import report_error
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

async def list_timezones(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the /listtimezones command.
    Sends a clean, categorized list of available timezones.
    """
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"

    try:
        # === Fetch all timezones ===
        timezones = pytz.all_timezones

        # === Group timezones into continents ===
        continents = {
            "🌍 Europe": [],
            "🌎 America": [],
            "🌏 Asia": [],
            "🌐 Africa": [],
            "🌋 Pacific": [],
            "❄️ Antarctica": [],
            "🏝 Other": []
        }

        for tz in timezones:
            if tz.startswith("Europe/"):
                continents["🌍 Europe"].append(tz)
            elif tz.startswith("America/"):
                continents["🌎 America"].append(tz)
            elif tz.startswith("Asia/"):
                continents["🌏 Asia"].append(tz)
            elif tz.startswith("Africa/"):
                continents["🌐 Africa"].append(tz)
            elif tz.startswith("Pacific/"):
                continents["🌋 Pacific"].append(tz)
            elif tz.startswith("Antarctica/"):
                continents["❄️ Antarctica"].append(tz)
            else:
                continents["🏝 Other"].append(tz)

        # === Format the output ===
        message = "*🌐 Available Timezones:*\n\n"
        for continent, tz_list in continents.items():
            message += f"*{continent}*\n"
            for tz in sorted(tz_list):
                message += f"• `{tz}`\n"
            message += "\n"

        # === Telegram limit handling ===
        if len(message) > 4000:
            # Too long for one message → split into parts
            chunks = [message[i:i+4000] for i in range(0, len(message), 4000)]
            for chunk in chunks:
                await update.message.reply_text(chunk, parse_mode="Markdown")
        else:
            await update.message.reply_text(message, parse_mode="Markdown")

        logger.info(f"/listtimezones used by {user}")

    except Exception as e:
        await report_error(context.bot, chat_id, e, context_info="/listtimezones command failure")
        logger.error(f"Error in /listtimezones: {e}")
