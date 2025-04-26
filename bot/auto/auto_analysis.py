import asyncio
from telegram import Bot
from telegram.ext import ContextTypes
from bot.engine.analysis_engine import analyze_symbol
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.autoscaler import run_autoscaler
from bot.config.settings import get_settings

# Load configuration
config = get_settings()

async def daily_analysis_job(context: ContextTypes.DEFAULT_TYPE):
    """
    Executes a compact daily analysis of all monitored symbols
    and sends the results automatically to the Telegram chat.
    """
    bot: Bot = context.bot
    chat_id = int(config["TELEGRAM_CHAT_ID"])
    lang = get_language(chat_id) or "en"

    await bot.send_message(chat_id=chat_id, text="📊 *Starting daily market analysis...*", parse_mode="Markdown")

    try:
        await run_autoscaler(bot, chat_id)
    except Exception as e:
        await bot.send_message(chat_id=chat_id, text=f"⚠️ Autoscaler error: {str(e)}", parse_mode="Markdown")

    symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
    if not symbols:
        await bot.send_message(chat_id=chat_id, text="❌ No symbols defined for auto-analysis.", parse_mode="Markdown")
        return

    for symbol in symbols:
        try:
            result = await analyze_symbol(symbol)

            if not result:
                await bot.send_message(chat_id=chat_id, text=f"⚠️ No data available for {symbol}.", parse_mode="Markdown")
                continue

            message = (
                f"*Symbol:* {symbol}\n"
                f"*Signal:* {result['signal']}\n"
                f"*RSI:* {result['rsi']}\n"
                f"*Short-Term Trend:* {result['short_term_trend']}\n"
                f"*Mid-Term Trend:* {result['mid_term_trend']}\n"
                f"*Pattern:* {result['pattern']}\n"
                f"*Candlestick:* {result['candlestick']}\n"
                f"*Stars:* {result['stars']} ⭐\n"
                f"*Suggested Holding:* {result['suggested_holding']}"
            )

            await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
            await asyncio.sleep(1.5)

        except Exception as e:
            await bot.send_message(chat_id=chat_id, text=f"⚠️ Error analyzing {symbol}: {str(e)}", parse_mode="Markdown")

    await bot.send_message(chat_id=chat_id, text="✅ *Daily analysis completed successfully!*", parse_mode="Markdown")
