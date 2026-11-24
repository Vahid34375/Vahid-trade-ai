
import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "Vahid Trade AI"

MARKET_API_KEY = os.getenv("MARKET_API_KEY", "")

ANALYSIS_INTERVAL = 3600

LOG_LEVEL = "INFO"

def check_configuration():
    print(f"{APP_NAME} configuration loaded")
    print("Analysis interval: 1 hour")
    print("Market API:", "Connected key" if MARKET_API_KEY else "Not configured")
