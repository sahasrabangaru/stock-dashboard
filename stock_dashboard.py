import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Stock Investment Dashboard", layout="wide")

st.title("📈 Stock Investment Dashboard")

st.sidebar.header("➕ Add Stock to Portfolio")
ticker = st.sidebar.text_input("Stock Ticker (e.g., AAPL, TSLA)")
quantity = st.sidebar.number_input("Quantity", min_value=0, step=1)
purchase_price = st.sidebar.number_input("Purchase Price per Share", min_value=0.0, step=0.01)
add_button = st.sidebar.button("Add to Portfolio")

if "portfolio" not in st.session_state:
    st.session_state.portfolio = pd.DataFrame(columns=["Ticker", "Quantity", "Purchase Price", "Current Price", "Gain/Loss"])

if add_button and ticker and quantity > 0 and purchase_price > 0:
    try:
        current_price = yf.Ticker(ticker).history(period="1d")["Close"][-1]
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

st.subheader("📊 Your Portfolio")
st.dataframe(st.session_state.portfolio.style.format({
    "Purchase Price": "${:.2f}",
    "Current Price": "${:.2f}",
    "Gain/Loss": "${:.2f}"
}))

st.subheader("💹 Portfolio Performance")
if not st.session_state.portfolio.empty:
    fig, ax = plt.subplots()
    ax.bar(st.session_state.portfolio["Ticker"], st.session_state.portfolio["Gain/Loss"], color='green')
    ax.set_ylabel("Gain / Loss ($)")
    ax.set_title("Your Stocks Performance")
    st.pyplot(fig)
