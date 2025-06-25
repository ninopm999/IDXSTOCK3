# ui_components.py
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def display_prediction_summary(forecast, last_close, symbol):
    """Displays the main prediction card."""
    predicted_price = forecast['yhat'].iloc[-1]
    confidence_lower = forecast['yhat_lower'].iloc[-1]
    confidence_upper = forecast['yhat_upper'].iloc[-1]
    
    st.header(f"Forecast for {symbol}")
    trend_arrow = "🔼" if predicted_price > last_close else "🔽"
    st.metric(
        label=f"Predicted Close Price on {forecast['ds'].iloc[-1].date()}",
        value=f"Rp {predicted_price:,.2f} {trend_arrow}",
        help=f"The model predicts the price will be between Rp {confidence_lower:,.2f} and Rp {confidence_upper:,.2f}."
    )

def plot_forecast(fig, forecast):
    """Adds forecast data to the main plot."""
    # Plot predicted line
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Prediction', line=dict(color='orange', dash='dot')))
    # Plot confidence interval
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], fill=None, mode='lines', line=dict(color='rgba(255,165,0,0.2)'), name='Upper Confidence'))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'], fill='tonexty', mode='lines', line=dict(color='rgba(255,165,0,0.2)'), name='Lower Confidence'))
    return fig

def display_dashboard(symbol, fundamentals, sentiment_score, analyzed_news, backtest_results):
    """Displays a dashboard of fundamentals, sentiment, and backtest results."""
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Fundamentals")
        for key, val in fundamentals.items():
            st.metric(label=key, value=f"{val:,.2f}" if val else "N/A")
    with col2:
        st.subheader("Sentiment")
        sentiment_emoji = "😊" if sentiment_score > 0.05 else "😟" if sentiment_score < -0.05 else "😐"
        st.metric(label="Agg. News Sentiment", value=f"{sentiment_score:.3f} {sentiment_emoji}")
    with col3:
        st.subheader("Backtest Highlights")
        st.metric("Strategy Return", f"{((backtest_results['Strategy Final Value']/INITIAL_CAPITAL)-1)*100:.2f}%")
        st.metric("Buy & Hold Return", f"{((backtest_results['Buy & Hold Final Value']/INITIAL_CAPITAL)-1)*100:.2f}%")
        st.metric("Sharpe Ratio", f"{backtest_results['Sharpe Ratio']:.2f}")


def plot_interactive_charts(df, forecast, backtest_returns_df):
    """Creates and displays all interactive charts."""
    # Main forecast chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Historical Close', line=dict(color='blue')))
    fig = plot_forecast(fig, forecast)
    fig.update_layout(title=f"{df.attrs['symbol']} Price Forecast", xaxis_title="Date", yaxis_title="Price (Rp)")
    st.plotly_chart(fig, use_container_width=True)

    # Indicator and Backtest Charts
    with st.expander("Show Detailed Charts & Backtest Performance"):
        # Backtest Performance Chart
        back_fig = go.Figure()
        back_fig.add_trace(go.Scatter(x=backtest_returns_df['ds'], y=backtest_returns_df['Strategy'], name='Model Strategy'))
        back_fig.add_trace(go.Scatter(x=backtest_returns_df['ds'], y=backtest_returns_df['Buy and Hold'], name='Buy & Hold'))
        back_fig.update_layout(title="Backtest: Strategy vs. Buy & Hold", xaxis_title="Date", yaxis_title="Cumulative Returns")
        st.plotly_chart(back_fig, use_container_width=True)

        # Technical Indicator Subplots
        tech_fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.05, subplot_titles=('RSI', 'MACD', 'On-Balance Volume (OBV)'))
        tech_fig.add_trace(go.Scatter(x=df['Date'], y=df['RSI'], name='RSI'), row=1, col=1)
        tech_fig.add_hline(y=70, row=1, col=1, line_dash="dot", line_color="red")
        tech_fig.add_hline(y=30, row=1, col=1, line_dash="dot", line_color="green")
        tech_fig.add_trace(go.Scatter(x=df['Date'], y=df['MACD'], name='MACD'), row=2, col=1)
        tech_fig.add_trace(go.Scatter(x=df['Date'], y=df['OBV'], name='OBV'), row=3, col=1)
        tech_fig.update_layout(height=600, title_text="Technical Indicators")
        st.plotly_chart(tech_fig, use_container_width=True)

def display_news_and_sentiment(analyzed_news):
    """Displays fetched news headlines and their individual sentiment."""
    with st.expander("View News Headlines & Sentiment Analysis"):
        for article in analyzed_news:
            sentiment_emoji = "😊" if article['sentiment'] > 0.05 else "😟" if article['sentiment'] < -0.05 else "😐"
            st.markdown(f"* {article['title']} **[{article['sentiment']:.2f} {sentiment_emoji}]**")
