from sklearn.linear_model import LinearRegression
import numpy as np

def predict_next_close(prices):
    if len(prices) < 7:
        return prices[-1]
    prices = prices[-7:]
    X = np.arange(len(prices)).reshape(-1, 1)
    y = prices
    model = LinearRegression()
    model.fit(X, y)
    prediction = model.predict([[len(prices)]])
    return prediction[0]