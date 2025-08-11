def allocate_funds(total_amount, predictions):
    # Ensure all predictions are positive-based for allocation weights
    adjusted_preds = {k: max(v, 0) for k, v in predictions.items()}

    total_pred = sum(adjusted_preds.values())

    allocations = {}
    if total_pred > 0:
        for stock, pred in adjusted_preds.items():
            alloc = (pred / total_pred) * total_amount if total_pred > 0 else 0
            allocations[stock] = round(alloc, 2)
    else:
        # No positive predictions -> equal allocation
        equal_share = total_amount / len(predictions)
        allocations = {stock: round(equal_share, 2) for stock in predictions}

    return allocations
