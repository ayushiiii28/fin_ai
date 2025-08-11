# allocator.py
def allocate_funds(predictions, total_amount):
    """
    Allocate investment funds based on predicted percentage gains.
    - predictions: dict of {ticker: predicted_percentage_gain}
    - total_amount: total USD amount to allocate
    """
    # Keep only positive predictions
    positive_preds = {k: v for k, v in predictions.items() if v > 0}

    if not positive_preds:
        # If all predictions are negative, split equally
        num_assets = len(predictions)
        return {k: round(total_amount / num_assets) for k in predictions}

    # Normalize so sum = 1
    total_gain = sum(positive_preds.values())
    allocation_ratios = {k: v / total_gain for k, v in positive_preds.items()}

    # Allocate funds
    allocations = {k: round(total_amount * allocation_ratios.get(k, 0)) for k in predictions}

    return allocations
