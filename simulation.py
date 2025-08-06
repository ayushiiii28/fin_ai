import yfinance as yf
from predictor import predict_next_close

def simulate_investment(amount, tickers):
    allocations = {}
    predictions = {}

    for ticker in tickers:
        df = yf.download(ticker, period="20d", interval="1d", progress=False)

        if df.empty or len(df) < 10:
            predictions[ticker] = "Insufficient data"
            allocations[ticker] = 0
            continue

        try:
            prediction = predict_next_close(df["Close"])
            predictions[ticker] = float(prediction)

            # Allocate proportionally to positive predictions
            allocations[ticker] = max(prediction, 0)
        except Exception as e:
            predictions[ticker] = f"Error: {str(e)}"
            allocations[ticker] = 0

    # Normalize allocations
    total_score = sum(allocations.values())
    if total_score > 0:
        for ticker in allocations:
            allocations[ticker] = round((allocations[ticker] / total_score) * amount, 2)
    else:
        # No good investment, zero allocation
        allocations = {ticker: 0 for ticker in tickers}

    return allocations, predictions
