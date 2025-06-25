# modeling.py
import pandas as pd
from prophet import Prophet
import numpy as np
from config import INITIAL_CAPITAL, TRADING_COMMISSION_RATE

@st.cache_data(ttl=10800)
def train_prophet_model(df):
    """Trains a Prophet forecasting model."""
    model_df = df[['Date', 'Close']].copy()
    model_df.rename(columns={'Date': 'ds', 'Close': 'y'}, inplace=True)
    
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False,
        seasonality_mode='multiplicative',
        changepoint_prior_scale=0.05
    )
    model.fit(model_df)
    return model

def make_future_prediction(model, future_days):
    """Makes future predictions with confidence intervals."""
    future = model.make_future_dataframe(periods=future_days)
    forecast = model.predict(future)
    return forecast

@st.cache_data(ttl=3600)
def run_backtest(_model_forecast, df_historical):
    """Runs a simple backtest and calculates key performance metrics."""
    # Align forecast with historical data
    forecast_on_history = _model_forecast[_model_forecast['ds'].isin(df_historical['Date'])]
    
    # Create signals
    signals = pd.DataFrame(index=forecast_on_history['ds'])
    signals['price'] = df_historical.set_index('Date')['Close']
    signals['forecast'] = forecast_on_history.set_index('ds')['yhat']
    # Signal: 1 if forecast is higher than previous close, -1 if lower
    signals['signal'] = np.where(signals['forecast'] > signals['price'].shift(1), 1, -1)

    # Calculate strategy returns
    signals['positions'] = signals['signal'].shift(1) # Trade on next day's open
    strategy_returns = signals['positions'] * (signals['price'].pct_change())
    # Apply commission cost on trades
    trades = signals['positions'].diff().abs()
    strategy_returns -= trades * TRADING_COMMISSION_RATE
    
    # --- Performance Metrics ---
    # 1. Cumulative Returns
    cumulative_strategy_returns = (1 + strategy_returns).cumprod()
    final_strategy_value = INITIAL_CAPITAL * cumulative_strategy_returns.iloc[-1]
    
    # 2. Buy and Hold
    buy_and_hold_returns = (1 + signals['price'].pct_change()).cumprod()
    final_buy_and_hold_value = INITIAL_CAPITAL * buy_and_hold_returns.iloc[-1]

    # 3. Sharpe Ratio
    sharpe_ratio = (strategy_returns.mean() / strategy_returns.std()) * np.sqrt(252) if strategy_returns.std() != 0 else 0

    # 4. Max Drawdown
    cumulative_wealth = INITIAL_CAPITAL * (1 + strategy_returns).cumprod()
    peak = cumulative_wealth.expanding(min_periods=1).max()
    drawdown = (cumulative_wealth - peak) / peak
    max_drawdown = drawdown.min()

    return {
        "Strategy Final Value": final_strategy_value,
        "Buy & Hold Final Value": final_buy_and_hold_value,
        "Sharpe Ratio": sharpe_ratio,
        "Max Drawdown": max_drawdown,
        "Returns DF": pd.DataFrame({
            'Strategy': cumulative_strategy_returns,
            'Buy and Hold': buy_and_hold_returns
        }).reset_index()
    }
