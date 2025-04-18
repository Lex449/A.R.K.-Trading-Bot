import os
from dotenv import load_dotenv
load_dotenv()

def get_settings():
    return {
        "BOT_TOKEN": os.getenv("BOT_TOKEN"),
        "OWNER_ID": os.getenv("OWNER_ID"),
        "API_KEY": os.getenv("API_KEY")
    }