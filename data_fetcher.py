import yfinance as yf

def get_stock_data(ticker, period="1mo", interval="1d"):
    data = yf.download(ticker, period=period, interval=interval, progress=False)
    return data[['Close']]