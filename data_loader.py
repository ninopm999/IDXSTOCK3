# data_loader.py
import yfinance as yf
import pandas as pd
from datetime import datetime
import streamlit as st
import requests
from config import (
    DEFAULT_START_DATE, 
    DEFAULT_END_DATE, 
    MARKETAUX_API_URL, 
    MARKETAUX_API_KEY
)

@st.cache_data(ttl=3600)
def load_stock_data(symbol):
    """Loads historical stock data for a given symbol."""
    try:
        df = yf.download(symbol, start=DEFAULT_START_DATE, end=DEFAULT_END_DATE, auto_adjust=False)
        if df.empty:
            st.error(f"No data found for symbol {symbol}. It may be an invalid ticker.")
            return None
        df.reset_index(inplace=True)
        return df
    except Exception as e:
        st.error(f"Error loading stock data for {symbol}: {e}")
        return None

@st.cache_data(ttl=86400)
def load_fundamental_data(symbol):
    """Loads fundamental data (P/E, P/B, etc.) for a given symbol."""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        fundamentals = {
            "P/E Ratio": info.get('trailingPE'),
            "P/B Ratio": info.get('priceToBook'),
            "Dividend Yield": info.get('dividendYield', 0) * 100,
            "Market Cap": info.get('marketCap')
        }
        return fundamentals
    except Exception as e:
        st.warning(f"Could not load fundamental data: {e}")
        return {}

@st.cache_data(ttl=10800)
def fetch_stock_news(symbol):
    """Fetches stock news from Marketaux API."""
    if MARKETAUX_API_KEY == "YOUR_MARKETAUX_API_KEY" or not MARKETAUX_API_KEY:
        st.warning("Marketaux API key not found. Please add it to your config.py file. News feature is disabled.")
        return []
    
    params = {
        "api_token": MARKETAUX_API_KEY,
        "symbols": symbol,
        "language": "en",
        "limit": 5  # Fetch the 5 most recent articles
    }
    try:
        response = requests.get(MARKETAUX_API_URL, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        return data.get('data', [])
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching news from Marketaux API: {e}")
        return []
