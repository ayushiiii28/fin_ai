import numpy as np
import joblib
from typing import List
from xgboost import XGBRegressor

# Load the pre-trained XGBoost model
model = joblib.load("xgboost_model.pkl")

def predict_next_close(prices: List[float]) -> float:
    """
    Predicts the next closing price using a pre-trained XGBoost model.

    Parameters:
    prices (List[float]): List of past closing prices.

    Returns:
    float: Predicted next closing price.
    """
    if not prices:
        raise ValueError("Price list is empty.")

    if len(prices) < 7:
        return float(prices[-1])  # Fallback to the last price if insufficient data

    # Use the last 7 prices as features
    recent_prices = np.array(prices[-7:]).reshape(1, -1)

    # Predict using the pre-trained model
    prediction = model.predict(recent_prices)

    return round(float(prediction[0]), 2)

