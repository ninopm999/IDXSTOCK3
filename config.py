# config.py
from datetime import datetime, timedelta

# --- General App Settings ---
APP_TITLE = "📈 World-Class Stock Forecaster"
PAGE_ICON = "📈"

# --- Sidebar Settings ---
SIDEBAR_TITLE = "🛠️ Controls"
DEFAULT_TICKER = "BBRI.JK"
DEFAULT_FUTURE_DAYS = 30
MIN_FUTURE_DAYS = 7
MAX_FUTURE_DAYS = 90

# --- Data Loading Settings ---
DEFAULT_START_DATE = "2020-01-01"
DEFAULT_END_DATE = datetime.today().strftime('%Y-%m-%d')
MARKET_INDEX_TICKER = "^JKSE"

# --- Backtesting Settings ---
INITIAL_CAPITAL = 100000.00
TRADING_COMMISSION_RATE = 0.001

# --- News & Sentiment ---
# Get your free API key from https://www.marketaux.com/
MARKETAUX_API_URL = "https://api.marketaux.com/v1/news/all"
MARKETAUX_API_KEY = "YOUR_MARKETAUX_API_KEY" # IMPORTANT: Replace with your actual key
