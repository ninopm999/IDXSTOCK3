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
# For market-wide context, we use the Jakarta Composite Index
MARKET_INDEX_TICKER = "^JKSE"

# --- Backtesting Settings ---
INITIAL_CAPITAL = 100000.00
# A simple representation of trading costs
TRADING_COMMISSION_RATE = 0.001 

# --- News & Sentiment ---
# In a real app, use a real API key stored securely (e.g., Streamlit Secrets)
NEWS_API_KEY_PLACEHOLDER = "YOUR_NEWS_API_KEY" 
NEWS_SEARCH_QUERY = "{stock_name} stock news"
