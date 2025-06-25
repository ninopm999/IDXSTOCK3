# data_loader.py
import yfinance as yf
import pandas as pd
from datetime import datetime
import streamlit as st
import requests
from config import DEFAULT_START_DATE, DEFAULT_END_DATE, NEWS_API_KEY_PLACEHOLDER

@st.cache_data(ttl=3600) # Cache for 1 hour
def load_stock_data(symbol):
    """Loads historical stock data for a given symbol."""
    try:
        # Explicitly set auto_adjust to False to silence the warning and maintain required columns
        df = yf.download(symbol, start=DEFAULT_START_DATE, end=DEFAULT_END_DATE, auto_adjust=False)
        if df.empty:
            st.error(f"No data found for symbol {symbol}. It may be an invalid ticker.")
            return None
        df.reset_index(inplace=True)
        return df
    except Exception as e:
        st.error(f"Error loading stock data for {symbol}: {e}")
        return None

@st.cache_data(ttl=86400) # Cache for 1 day
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

@st.cache_data(ttl=10800) # Cache for 3 hours
def fetch_stock_news(query):
    """Fetches stock news from a news API. Placeholder function."""
    st.warning("News feature is a placeholder. A real News API key is required.")
    # This is a placeholder. In a real app, you would use a real News API.
    # Example using NewsAPI:
    # url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY_PLACEHOLDER}"
    # response = requests.get(url)
    # if response.status_code == 200:
    #     return response.json().get('articles', [])
    return [
        {'title': f'Positive outlook for {query}', 'description': 'Analysts are bullish.'},
        {'title': f'Market volatility impacts {query}', 'description': 'Investors are cautious.'}
    ]
