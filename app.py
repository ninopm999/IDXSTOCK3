# app.py
import streamlit as st
from config import *
import data_loader
import feature_engineering
import modeling
import ui_components

# --- Page Configuration ---
st.set_page_config(page_title=APP_TITLE, page_icon=PAGE_ICON, layout="wide")
st.title(f"{PAGE_ICON} {APP_TITLE}")

# --- Sidebar Controls ---
st.sidebar.title(SIDEBAR_TITLE)
selected_symbol = st.sidebar.text_input("Enter IDX stock symbol", DEFAULT_TICKER).strip().upper()
future_days = st.sidebar.slider("Days to Forecast", MIN_FUTURE_DAYS, MAX_FUTURE_DAYS, DEFAULT_FUTURE_DAYS)
run_button = st.sidebar.button("Run Analysis", type="primary")

# --- Main Application Flow ---
if run_button:
    if not selected_symbol:
        st.warning("Please enter a stock symbol.")
    else:
        with st.spinner(f"Running analysis for {selected_symbol}... This may take a moment."):
            try:
                # 1. Load Data
                df = data_loader.load_stock_data(selected_symbol)
                
                if df is not None:
                    df.attrs['symbol'] = selected_symbol
                    last_close = df['Close'].iloc[-1]
                    
                    fundamentals = data_loader.load_fundamental_data(selected_symbol)
                    news = data_loader.fetch_stock_news(selected_symbol)

                    # 2. Feature Engineering
                    df = feature_engineering.add_technical_indicators(df)
                    sentiment_score, analyzed_news = feature_engineering.analyze_sentiment(news)
                    
                    # 3. Modeling & Forecasting
                    model = modeling.train_prophet_model(df)
                    forecast = modeling.make_future_prediction(model, future_days)

                    # Run backtest on historical forecast portion
                    model_historical_forecast = model.predict(model.history)
                    backtest_results = modeling.run_backtest(model_historical_forecast, df)

                    # 4. UI Display
                    ui_components.display_prediction_summary(forecast.tail(1), last_close, selected_symbol)
                    st.divider()
                    ui_components.display_dashboard(selected_symbol, fundamentals, sentiment_score, analyzed_news, backtest_results)
                    st.divider()
                    ui_components.plot_interactive_charts(df, forecast, backtest_results['Returns DF'])
                    ui_components.display_news_and_sentiment(analyzed_news)

            except Exception as e:
                st.error("An unexpected error occurred during the analysis.")
                st.error(f"Details: {e}")
else:
    st.info("Enter a stock symbol and click 'Run Analysis' to begin.")
