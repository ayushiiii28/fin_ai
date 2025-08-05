def allocate_funds(predictions, total_amount):
    total_score = sum([p["return"] / p["risk"] for p in predictions.values()])
    allocations = {}
    for asset, pred in predictions.items():
        score = pred["return"] / pred["risk"]
        allocations[asset] = round((score / total_score) * total_amount, 2)
    return allocations