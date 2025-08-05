import numpy as np
import xgboost as xgb
import os

# Load the model from JSON
model = xgb.Booster()
model.load_model(os.path.join(os.path.dirname(__file__), "xgboost_model.json"))

def predict_next_close(prices):
    """
    Predicts next closing performance (1 = invest, 0 = not) using recent prices and XGBoost model.

    Parameters:
        prices (list or np.array): Past closing prices.

    Returns:
        float: Model prediction (probability).
    """
    if prices is None or len(prices) < 10:
        return float(prices[-1]) if len(prices) > 0 else 0.0

    prices = np.array(prices).flatten()
    recent = prices[-6:]   # last 6 prices
    return_1d = (recent[1:] - recent[:-1]) / recent[:-1]

    # Compute features safely
    volatility = float(np.std(return_1d))
    momentum = float(prices[-1] / prices[-6])
    sector_strength = float(np.mean(prices[-10:]) / prices[-1])  # uses all 10
    last_return = float(return_1d[-1])  # ✅ force scalar, not array

    features = np.array([[volatility, momentum, sector_strength, last_return]], dtype=np.float32)
    dmatrix = xgb.DMatrix(features)
    predicted = model.predict(dmatrix)[0]

    return float(predicted)
