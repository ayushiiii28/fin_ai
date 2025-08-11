import streamlit as st
from simulation import simulate_investment

st.title("📈 SmartInvestor.AI - Real-Time Stock Allocator")

amount = st.number_input("Enter your investment amount (USD):", min_value=100, step=100)
tickers = ["AAPL", "GOOGL", "TSLA", "MSFT"]

if st.button("Run Simulation"):
    allocations, predictions = simulate_investment(amount, tickers)

    # Display Allocations
    st.subheader("💰 Allocations")
    alloc_df = []
    for stock in tickers:
        pct = (allocations[stock] / amount) * 100 if amount > 0 else 0
        alloc_df.append({
            "Stock": stock,
            "Allocation ($)": allocations[stock],
            "Portfolio %": f"{pct:.2f}%"
        })
    st.table(alloc_df)

    # Display Predictions with Colors
    st.subheader("📊 Predicted Gains")
    for stock in tickers:
        pct = predictions[stock]
        if pct >= 0:
            st.markdown(f"🟢 **{stock}**: +{pct:.2f}%")
        else:
            st.markdown(f"🔴 **{stock}**: {pct:.2f}%")
