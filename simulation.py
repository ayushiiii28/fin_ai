import pandas as pd
from predictor import predict_next_close
from allocator import allocate_funds

def simulate_investment(amount, tickers):
    allocations = {}
    predictions = {}

    for ticker in tickers:
        df = pd.read_csv(f"data/{ticker}.csv")  # Replace with real-time fetch
        predicted_pct = predict_next_close(df['Close'].values)

        # Store predictions as percentages
        predictions[ticker] = predicted_pct

    # Allocate funds based on predicted % returns
    allocations = allocate_funds(amount, predictions)

    return allocations, predictions

