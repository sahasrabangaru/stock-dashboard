import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Advanced Stock Dashboard", layout="wide")
st.title("📈 Advanced Stock Investment Dashboard")

# Sidebar input
st.sidebar.header("➕ Add Stock to Portfolio")
ticker = st.sidebar.text_input("Stock Ticker (e.g., AAPL, TSLA)")
quantity = st.sidebar.number_input("Quantity", min_value=0, step=1)
purchase_price = st.sidebar.number_input("Purchase Price per Share", min_value=0.0, step=0.01)
add_button = st.sidebar.button("Add to Portfolio")

# Session state portfolio
if "portfolio" not in st.session_state:
    st.session_state.portfolio = pd.DataFrame(columns=["Ticker", "Quantity", "Purchase Price", "Current Price", "Gain/Loss"])

# Add stock to portfolio
if add_button and ticker and quantity > 0 and purchase_price > 0:
    try:
        data = yf.Ticker(ticker).history(period="1d")
        current_price = data["Close"][-1]
        gain_loss = (current_price - purchase_price) * quantity
        new_row = pd.DataFrame([[ticker.upper(), quantity, purchase_price, current_price, gain_loss]],
                               columns=st.session_state.portfolio.columns)
        st.session_state.portfolio = pd.concat([st.session_state.portfolio, new_row], ignore_index=True)
    except:
        st.error("❌ Invalid ticker or unable to fetch data.")

# Update current prices
for i, row in st.session_state.portfolio.iterrows():
    try:
        current_price = yf.Ticker(row["Ticker"]).history(period="1d")["Close"][-1]
        st.session_state.portfolio.at[i, "Current Price"] = current_price
        st.session_state.portfolio.at[i, "Gain/Loss"] = (current_price - row["Purchase Price"]) * row["Quantity"]
    except:
        continue

# Display portfolio
st.subheader("📊 Your Portfolio")
st.dataframe(st.session_state.portfolio.style.format({
    "Purchase Price": "${:.2f}",
    "Current Price": "${:.2f}",
    "Gain/Loss": "${:.2f}"
}))

# Trend visualization
st.subheader("📉 Live Stock Trends")

if not st.session_state.portfolio.empty:
    selected_tickers = st.multiselect(
        "Select stocks to view trends:",
        st.session_state.portfolio["Ticker"].unique(),
        default=st.session_state.portfolio["Ticker"].unique().tolist()
    )

    fig, ax = plt.subplots(figsize=(10, 4))

    for ticker in selected_tickers:
        data = yf.Ticker(ticker).history(period="7d", interval="1h")
        ax.plot(data.index, data["Close"], label=ticker)

    ax.set_title("7-Day Hourly Price Trend")
    ax.set_ylabel("Price ($)")
    ax.legend()
    st.pyplot(fig)
else:
    st.info("Add stocks to see live trends.")
