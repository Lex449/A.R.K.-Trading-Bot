from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.utils.analysis import analyze_symbol

async def analyse(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Führt eine Marktanalyse für ein bestimmtes Symbol durch (z. B. US100)."""
    symbol = "US100"  # Du kannst hier später dynamisch via Argumente erweitern

    result = analyze_symbol(symbol)

    if result is None:
        await update.message.reply_text("⚠️ Analyse fehlgeschlagen. Bitte später erneut versuchen.")
        return

    response = (
        f"**Analyse für {result['symbol']}**\n"
        f"Preis: {result['price']}\n"
        f"RSI: {result['rsi']:.2f}\n"
        f"EMA (Short): {result['ema_short']:.2f}\n"
        f"EMA (Long): {result['ema_long']:.2f}\n"
        f"Muster: {result['pattern']}\n"
        f"Trend: {result['trend'] or 'Unklar'}\n"
        f"Signal: {result['signal'] or 'Kein Signal'}"
    )

    await update.message.reply_text(response, parse_mode="Markdown")

analyse_handler = CommandHandler("analyse", analyse)
