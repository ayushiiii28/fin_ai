📈** SmartInvestor.AI – Real-Time Stock Allocator**

SmartInvestor.AI is an AI-powered investment decision-support system that intelligently allocates a user’s investment amount across multiple stocks based on predicted short-term market trends.
The system integrates real-time market data, machine learning prediction (XGBoost), and a dynamic allocation engine, deployed through an interactive Streamlit web application.

🚀 **Live Demo**

🔗 Deployed App: https://fin-ai-8zen.onrender.com/

<img width="1919" height="959" alt="Screenshot 2026-01-22 235921" src="https://github.com/user-attachments/assets/6054732c-003f-4394-88dc-440c7fa88063" />

🎯 **Project Objective**

The main goal of SmartInvestor.AI is to:

Predict short-term stock performance

Allocate funds intelligently across selected stocks

Maximize expected returns while minimizing risk

Simulate real-world AI-driven investment strategies

This project demonstrates how Artificial Intelligence can be applied in fintech for automated decision-making and portfolio allocation.

🧠** How It Works**
User Input → Fetch Stock Data → Feature Engineering → XGBoost Prediction 
→ Normalization → Fund Allocation → Streamlit Dashboard Output


**Core Workflow:**

Fetches 30–60 days of stock data using Yahoo Finance API

Extracts technical features (volatility, momentum, sector strength, returns)

Predicts expected price movement using XGBoost

Normalizes and shifts predictions

Allocates funds proportionally

Displays results in real time on a Streamlit dashboard

**🛠️ Technologies Used**

Programming Language: Python 3.x

Machine Learning: XGBoost, Scikit-learn

Data Handling: Pandas, NumPy

API: Yahoo Finance (yfinance)

Visualization: Matplotlib, Seaborn

Deployment: Streamlit

Tools: VS Code, Jupyter Notebook, Git, GitHub

⚙️ **Features**

✔ Real-time stock data fetching
✔ Financial feature engineering
✔ ML-based price movement prediction
✔ Intelligent fund allocation engine
✔ Prediction normalization and fallback safety logic
✔ Investment simulation
✔ Interactive Streamlit web interface
