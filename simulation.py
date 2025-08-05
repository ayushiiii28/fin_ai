from data_fetcher import get_stock_data
from predictor import predict_next_close
from allocator import allocate_funds

def simulate_investment(total_investment, assets):
    prediction_scores = {}
    details = {}

    for asset in assets:
        df = get_stock_data(asset)
        if df.empty:
            continue
        predicted_close = predict_next_close(df['Close'].values)
        last_close = df['Close'].values[-1]

        expected_return = (predicted_close - last_close) / last_close

        prediction_scores[asset] = expected_return   # only the score goes to allocator
        details[asset] = {
            "predicted_close": round(predicted_close, 2),
            "last_close": round(last_close, 2),
            "expected_return": round(expected_return * 100, 2)
        }

    allocations = allocate_funds(prediction_scores, total_investment)
    return allocations, details
