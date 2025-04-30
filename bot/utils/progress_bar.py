def create_progress_bar(percent: float, length: int = 20) -> str:
    """
    Generates a visual progress bar using █ and ░ for Telegram messages.

    Args:
        percent (float): Value between 0–100.
        length (int): Total number of segments (default: 20)

    Returns:
        str: Progress bar string like [████████░░░░░░░░░░]
    """
    filled = int((percent / 100) * length)
    empty = length - filled
    bar = "█" * filled + "░" * empty
    return f"[{bar}]"
