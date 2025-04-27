"""
Sets a clean custom command list for Telegram.
Premium Build – No more external bot suggestions.
"""

from telegram import BotCommand

async def set_bot_commands(application):
    """
    Defines and sets the command list for the bot.
    """

    commands = [
        BotCommand("start", "Start the bot"),
        BotCommand("help", "Show help and command list"),
        BotCommand("analyse", "Analyse a symbol (e.g. /analyse AAPL)"),
        BotCommand("signal", "Get current trading signals"),
        BotCommand("status", "Show session statistics"),
        BotCommand("shutdown", "Stop the bot"),
        BotCommand("testsignal", "Send a test trading signal"),
        BotCommand("testanalyse", "Send a test symbol analysis"),
    ]

    await application.bot.set_my_commands(commands)
