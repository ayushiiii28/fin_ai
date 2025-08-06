import streamlit as st
from simulation import simulate_investment

st.title("📈 SmartInvestor.AI - Real-Time Stock Allocator")

amount = st.number_input("Enter your investment amount (USD):", min_value=100, step=100)
tickers = ["AAPL", "GOOGL", "TSLA", "MSFT"]

if st.button("Run Simulation"):
    with st.spinner("Predicting and allocating..."):
        allocations, predictions = simulate_investment(amount, tickers)

    st.subheader("💰 Allocations")
    st.json(allocations)

    st.subheader("📊 Predictions")
    st.json(predictions)
