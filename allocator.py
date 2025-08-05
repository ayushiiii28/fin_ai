def allocate_funds(predictions, total_amount):
    total_score = sum(predictions.values())
    allocations = {}
    for asset, score in predictions.items():
        score_value = float(score)  # Convert from np.ndarray to float
        allocations[asset] = round((score_value / total_score) * total_amount, 2)
    return allocations
