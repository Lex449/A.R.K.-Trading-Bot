# bot/handlers/set_my_commands.py

from telegram import BotCommand

async def set_bot_commands(application):
    """
    Sets the available commands for the bot dynamically.
    """
    commands = [
        BotCommand("start", "Start the A.R.K. Bot"),
        BotCommand("help", "Show available commands"),
        BotCommand("analyse", "Analyze a market symbol (e.g., /analyse AAPL)"),
        BotCommand("setlanguage", "Change language (en/de)"),
        BotCommand("signal", "Manual signal trigger info"),
        BotCommand("status", "Session performance stats"),
        BotCommand("uptime", "Show bot uptime"),
        BotCommand("health", "System health check"),
        BotCommand("shutdown", "Stop the bot safely"),
    ]
    await application.bot.set_my_commands(commands)
