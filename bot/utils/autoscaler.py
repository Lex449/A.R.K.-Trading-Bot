import os
import logging
from telegram import Bot

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Correct Finnhub-compatible symbols for indices and main assets
DEFAULT_SYMBOLS = [
    "^GSPC",  # S&P 500 Index
    "^DJI",   # Dow Jones Industrial Average
    "^IXIC",  # NASDAQ Composite
    "MDY",    # MidCap ETF
    "VTI",    # Total Market ETF
    "VOO",    # S&P 500 ETF
    "SPY",    # S&P 500 ETF
    "XLF",    # Financial Sector ETF
    "XLK",    # Technology Sector ETF
    "XLE",    # Energy Sector ETF
    "AAPL",   # Apple
    "MSFT",   # Microsoft
    "TSLA",   # Tesla
    "NVDA",   # NVIDIA
    "META",   # Meta Platforms
    "AMZN",   # Amazon
    "GOOGL",  # Alphabet
    "BRK.B",  # Berkshire Hathaway
    "UNH",    # UnitedHealth
    "JPM"     # JPMorgan Chase
]

# Fallback symbols for additional scaling
FALLBACK_SYMBOLS = [
    "AAPL", "MSFT", "TSLA", "NVDA", "META",
    "AMZN", "GOOGL", "BRK.B", "UNH", "JPM"
]

def get_scaled_symbols(current_count: int, max_count: int = 150) -> tuple:
    """
    Calculate and return a list of scaled symbols based on current active symbols
    and maximum allowed symbols. Adds fallback symbols if necessary.
    """
    ideal_count = max_count // 12
    additional_needed = max(ideal_count - current_count, 0)

    final = DEFAULT_SYMBOLS.copy()
    added = []

    for sym in FALLBACK_SYMBOLS:
        if additional_needed <= 0:
            break
        if sym not in final:
            final.append(sym)
            added.append(sym)
            additional_needed -= 1

    return final, added

async def run_autoscaler(bot: Bot, chat_id: int):
    """
    Executes the auto-scaler, ensuring enough symbols are monitored.
    Sends updates via Telegram if changes occur.
    """
    env_symbols = os.getenv("AUTO_SIGNAL_SYMBOLS", "")
    current = [s.strip() for s in env_symbols.split(",") if s.strip()]

    scaled, new_added = get_scaled_symbols(len(current))

    os.environ["AUTO_SIGNAL_SYMBOLS"] = ",".join(scaled)

    if new_added:
        added_str = ", ".join(new_added)
        msg = (
            f"🚀 *Auto-Scaler Activated*\n\n"
            f"*New Symbols Added:*\n`{added_str}`\n\n"
            f"_Your bot is now better prepared for market opportunities._"
        )
        await bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
        logger.info(f"Auto-Scaler added new symbols: {added_str}")
    else:
        await bot.send_message(
            chat_id=chat_id,
            text="✅ *Auto-Scaler Check Completed:*\nAll symbols are optimally configured.",
            parse_mode="Markdown"
        )
        logger.info("Auto-Scaler check completed, no new symbols needed.")

def get_scaled_limit(symbols: list, max_total: int = 150) -> int:
    """
    Calculates how many signals are allowed per symbol per hour,
    based on the total allowed signals.
    """
    count = len(symbols)
    return max(1, max_total // count)
