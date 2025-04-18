import os

def get_settings():
    return {
        "telegram": {
            "token": os.getenv("BOT_TOKEN") or "7655719634:AAE01VP0gQGXgiL_hHOgBD3pG5yzId4",
            "admin_id": 7699862580,
        },
        "twelvedata": {
            "api_key": os.getenv("TWELVEDATA_API_KEY") or "0dd4ddf44b144ea48df01c9fdfc80921"
        },
        "markets": ["NDX", "DJI", "DAX"],
        "language": "auto"
    }}