import numpy as np
import xgboost as xgb
import os

# Load the model from JSON
model = xgb.Booster()
model.load_model(os.path.join(os.path.dirname(__file__), "xgboost_model.json"))

def predict_next_close(prices):
    if prices is None or len(prices) < 6:
        return float(prices[-1]) if len(prices) > 0 else 0.0

    prices = np.array(prices)
    recent = prices[-6:]  # last 6 closes to make 5 diffs
    return_1d = (recent[1:] - recent[:-1]) / recent[:-1]

    volatility = np.std(return_1d)
    momentum = prices[-1] / prices[-6]
    sector_strength = np.mean(prices[-10:]) / prices[-1] if len(prices) >= 10 else 1.0

    features = np.array([[volatility, momentum, sector_strength, return_1d[-1]]])

    # XGBoost Booster expects DMatrix input
    dmatrix = xgb.DMatrix(features)
    predicted = model.predict(dmatrix)[0]
    return float(predicted)
