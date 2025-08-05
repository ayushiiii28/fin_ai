import streamlit as st
from simulation import simulate_investment

st.title("📈 SmartInvestAI")

amount = st.number_input("Enter Investment Amount (₹)", min_value=100.0, value=1000.0)
assets = st.multiselect("Select Assets (e.g., AAPL, GOOGL)", ["AAPL", "GOOGL", "MSFT", "TSLA"], default=["AAPL", "GOOGL"])

if st.button("Run Simulation"):
    allocations, predictions = simulate_investment(amount, assets)
    st.subheader("💰 Allocations")
    st.write(allocations)
    st.subheader("📊 Predictions")
    st.write(predictions)