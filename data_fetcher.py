import yfinance as yf
import pandas as pd

def fetch_data(ticker, period="30d", interval="1d"):
    """Fetch recent historical stock data."""
    data = yf.download(ticker, period=period, interval=interval, progress=False)
    data.dropna(inplace=True)
    return data
