from data_fetcher import fetch_data
from predictor import predict_next_close

def simulate_investment(amount, tickers):
    allocations = {}
    predictions = {}

    for ticker in tickers:
        df = fetch_data(ticker)
        if df.empty:
            predictions[ticker] = None
            allocations[ticker] = 0
            continue

        prediction = predict_next_close(df['Close'].values)

        if prediction is None:
            predictions[ticker] = None
            allocations[ticker] = 0
            continue

        predictions[ticker] = round(prediction, 4)

        # Allocate equally to predictions > 0.5
        if prediction > 0.5:
            allocations[ticker] = 1  # Will normalize later
        else:
            allocations[ticker] = 0

    # Normalize allocations
    total_alloc = sum(allocations.values())
    if total_alloc > 0:
        for k in allocations:
            allocations[k] = round((allocations[k] / total_alloc) * amount, 2)
    else:
        for k in allocations:
            allocations[k] = 0

    return allocations, predictions
