from sklearn.linear_model import LinearRegression
import numpy as np
from typing import List

def predict_next_close(prices: List[float]) -> float:
    """
    Predicts the next closing price based on the past 7 prices using linear regression.

    Parameters:
    prices (List[float]): List of past closing prices.

    Returns:
    float: Predicted next closing price.
    """
    if not prices:
        raise ValueError("Price list is empty.")

    if len(prices) < 7:
        return float(prices[-1])  # Fallback to the last price if insufficient data

    recent_prices = prices[-7:]
    X = np.arange(len(recent_prices)).reshape(-1, 1)
    y = np.array(recent_prices)

    model = LinearRegression()
    model.fit(X, y)

    prediction = model.predict([[len(recent_prices)]])
    return round(prediction[0], 2)
