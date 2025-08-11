import yfinance as yf
from predictor import predict_next_close

def simulate_investment(amount, tickers):
    predictions = {}
    allocations = {}

    # Get predictions for each stock
    for ticker in tickers:
        df = yf.download(ticker, period="60d", interval="1d", progress=False)
        pct_pred = predict_next_close(df['Close'].values)
        predictions[ticker] = pct_pred if pct_pred is not None else 0.0

    # Ensure no zero allocation for good stocks — shift values up
    min_pred = min(predictions.values())
    if min_pred <= 0:
        shift = abs(min_pred) + 1  # ensure all are positive
        shifted_preds = {t: p + shift for t, p in predictions.items()}
    else:
        shifted_preds = predictions.copy()

    # Normalize and allocate funds
    total_score = sum(shifted_preds.values())
    if total_score > 0:
        allocations = {
            t: round((score / total_score) * amount, 2)
            for t, score in shifted_preds.items()
        }
    else:
        allocations = {t: amount / len(tickers) for t in tickers}  # equal allocation fallback

    return allocations, predictions
