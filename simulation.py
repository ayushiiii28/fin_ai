# simulation.py
from predictor import predict_pct_from_prices

def simulate_investment(amount, tickers):
    allocations = {}
    predictions = {}

    for ticker in tickers:
        import yfinance as yf
        df = yf.download(ticker, period="90d", interval="1d", progress=False)
        prices = df["Close"].values
        pct = predict_pct_from_prices(prices)

        predictions[ticker] = pct
        if pct is not None:
            allocations[ticker] = round(amount * max(pct, 0) / 100, 2)  # allocate only for positive pct
        else:
            allocations[ticker] = 0

    return allocations, predictions
