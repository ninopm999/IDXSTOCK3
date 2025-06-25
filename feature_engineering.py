# feature_engineering.py
import pandas as pd
from ta.momentum import RSIIndicator, AwesomeOscillatorIndicator
from ta.trend import MACD, ADXIndicator
from ta.volatility import BollingerBands, AverageTrueRange
from ta.volume import OnBalanceVolumeIndicator
from textblob import TextBlob

def add_technical_indicators(df):
    """Adds a comprehensive set of technical indicators to the dataframe."""
    df['RSI'] = RSIIndicator(close=df['Close']).rsi()
    df['MACD'] = MACD(close=df['Close']).macd()
    df['BB_High'] = BollingerBands(close=df['Close']).bollinger_hband()
    df['BB_Low'] = BollingerBands(close=df['Close']).bollinger_lband()
    df['ATR'] = AverageTrueRange(high=df['High'], low=df['Low'], close=df['Close']).average_true_range()
    df['OBV'] = OnBalanceVolumeIndicator(close=df['Close'], volume=df['Volume']).on_balance_volume()
    df['ADX'] = ADXIndicator(high=df['High'], low=df['Low'], close=df['Close']).adx()
    df['Awesome_Osc'] = AwesomeOscillatorIndicator(high=df['High'], low=df['Low']).awesome_oscillator()
    df.dropna(inplace=True)
    return df

def analyze_sentiment(news_articles):
    """Analyzes sentiment of news headlines and returns an aggregate score."""
    if not news_articles:
        return 0.0, []
    
    sentiment_scores = []
    analyzed_articles = []
    for article in news_articles:
        text = article.get('title', '')
        blob = TextBlob(text)
        score = blob.sentiment.polarity
        sentiment_scores.append(score)
        analyzed_articles.append({'title': text, 'sentiment': score})
        
    return sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0.0, analyzed_articles
