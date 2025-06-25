# feature_engineering.py
import pandas as pd
from ta.momentum import RSIIndicator, AwesomeOscillatorIndicator
from ta.trend import MACD, ADXIndicator
from ta.volatility import BollingerBands, AverageTrueRange
from ta.volume import OnBalanceVolumeIndicator
from textblob import TextBlob

def add_technical_indicators(df):
    """Adds a comprehensive set of technical indicators to the dataframe."""
    # Ensure data is 1-Dimensional for the TA library
    close_series = pd.Series(df['Close'])
    high_series = pd.Series(df['High'])
    low_series = pd.Series(df['Low'])
    volume_series = pd.Series(df['Volume'])

    df['RSI'] = RSIIndicator(close=close_series).rsi()
    df['MACD'] = MACD(close=close_series).macd()
    df['BB_High'] = BollingerBands(close=close_series).bollinger_hband()
    df['BB_Low'] = BollingerBands(close=close_series).bollinger_lband()
    df['ATR'] = AverageTrueRange(high=high_series, low=low_series, close=close_series).average_true_range()
    df['OBV'] = OnBalanceVolumeIndicator(close=close_series, volume=volume_series).on_balance_volume()
    df['ADX'] = ADXIndicator(high=high_series, low=low_series, close=close_series).adx()
    df['Awesome_Osc'] = AwesomeOscillatorIndicator(high=high_series, low=low_series).awesome_oscillator()
    
    df.dropna(inplace=True)
    return df

def analyze_sentiment_from_api(news_articles):
    """
    Analyzes sentiment from news articles fetched from the Marketaux API.
    It extracts the pre-calculated sentiment score provided by the API.
    """
    if not news_articles:
        return 0.0, []

    sentiment_scores = []
    analyzed_articles = []

    for article in news_articles:
        # Marketaux provides sentiment for each entity in an article
        if 'entities' in article and article['entities']:
            # We'll average the sentiment scores of all entities found in the article
            entity_sentiments = [entity.get('sentiment_score', 0.0) for entity in article['entities']]
            avg_sentiment = sum(entity_sentiments) / len(entity_sentiments) if entity_sentiments else 0.0
            
            sentiment_scores.append(avg_sentiment)
            analyzed_articles.append({
                'title': article.get('title', 'No Title'),
                'sentiment': avg_sentiment,
                'url': article.get('url')
            })

    # Return the average sentiment across all articles
    return sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0.0, analyzed_articles
