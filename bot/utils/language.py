# bot/utils/language.py

"""
A.R.K. Language Manager – Dynamic Language Setting Handler.
Provides multilingual support fallback.
"""

# Placeholder for real user-language management
user_languages = {}

def get_language(chat_id: int) -> str:
    """
    Gets the preferred language for a user.
    
    Args:
        chat_id (int): Telegram chat ID.

    Returns:
        str: Language code ("en" or "de").
    """
    return user_languages.get(chat_id, "en")

def set_language(chat_id: int, lang: str):
    """
    Sets the preferred language for a user.
    
    Args:
        chat_id (int): Telegram chat ID.
        lang (str): Language code.
    """
    user_languages[chat_id] = lang
