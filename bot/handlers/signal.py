import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from bot.engine.analysis_engine import analyze_symbol
from bot.config.settings import get_settings

config = get_settings()

async def signal_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler for /signal command.
    Analyzes configured symbols and sends trading signals to Telegram.
    """
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text="🚀 *Scanning for trading opportunities...*", parse_mode="Markdown")

    symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
    if not symbols:
        await context.bot.send_message(chat_id=chat_id, text="❌ No symbols configured for signal analysis.", parse_mode="Markdown")
        return

    for symbol in symbols:
        try:
            result = await analyze_symbol(symbol)

            if not result:
                await context.bot.send_message(chat_id=chat_id, text=f"⚠️ No data available for {symbol}.", parse_mode="Markdown")
                continue

            message = (
                f"📈 *Trading Signal*\n\n"
                f"*Symbol:* {symbol}\n"
                f"*Action:* {result['signal']}\n"
                f"*Short-Term Trend:* {result['short_term_trend']}\n"
                f"*Mid-Term Trend:* {result['mid_term_trend']}\n"
                f"*RSI:* {result['rsi']}\n"
                f"*Pattern Detected:* {result['pattern']}\n"
                f"*Candlestick Formation:* {result['candlestick']}\n"
                f"*Quality Rating:* {result['stars']} ⭐\n"
                f"*Suggested Holding:* {result['suggested_holding']}\n\n"
                f"🔎 Always manage your risk. No financial advice."
            )

            await context.bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
            await asyncio.sleep(1.5)

        except Exception as e:
            await context.bot.send_message(chat_id=chat_id, text=f"⚠️ Error analyzing {symbol}: {str(e)}", parse_mode="Markdown")

    await context.bot.send_message(chat_id=chat_id, text="✅ *Signal scan completed.*", parse_mode="Markdown")
