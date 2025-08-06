import streamlit as st
from simulation import simulate_investment

st.title("📈 Smart Investment Simulator")

amount = st.number_input("💰 Enter investment amount", value=10000)
tickers = st.multiselect("📊 Select stocks", ["AAPL", "GOOGL", "TSLA", "MSFT"], default=["AAPL", "GOOGL"])

if st.button("Simulate"):
    allocations, predictions = simulate_investment(amount, tickers)

    st.subheader("💰 Allocations")
    st.json(allocations)

    st.subheader("📊 Predictions (Probabilities)")
    st.json(predictions)

