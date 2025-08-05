from data_fetcher import get_stock_data
from predictor import predict_next_close
from allocator import allocate_funds

def simulate_investment(total_investment, assets):
    predictions = {}
    for asset in assets:
        df = get_stock_data(asset)
        if df.empty or len(df) < 10:
            continue
        predicted_close = predict_next_close(df['Close'].values.flatten())
        last_close = df['Close'].values[-1]
        expected_return = (predicted_close - last_close) / last_close
        predictions[asset] = expected_return
    allocations = allocate_funds(predictions, total_investment)
    return allocations, predictions
