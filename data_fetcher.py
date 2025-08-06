import yfinance as yf

def fetch_data(ticker, period="90d", interval="1d"):
    data = yf.download(ticker, period=period, interval=interval, progress=False, auto_adjust=False)
    return data
