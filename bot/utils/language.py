# bot/utils/language.py

def get_language(update_or_context) -> str:
    """
    Determines the preferred language of the user.
    Tries user_data['lang'] first, defaults to English.
    """

    # Case 1: It's an update object from a Telegram command
    if hasattr(update_or_context, "user_data"):
        return update_or_context.user_data.get("lang", "en")

    # Case 2: It's just a chat_id or unknown input
    return "en"
