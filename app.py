import streamlit as st
import os
from dotenv import load_dotenv
from bot.client import BinanceClient
from bot.orders import OrderManager

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Binance Futures Testnet Bot", layout="wide")

# Initialize session state for Binance Client & Balance
if "api_connected" not in st.session_state:
    st.session_state.api_connected = False
if "usdt_balance" not in st.session_state:
    st.session_state.usdt_balance = 0.0

def check_connection():
    """Validates the connection by fetching the account balance."""
    try:
        client = BinanceClient()
        balance = client.get_account_balance()
        if balance is not None:
            st.session_state.usdt_balance = balance
            st.session_state.api_connected = True
            st.success("API Keys are valid. Connected to Binance Testnet!")
        else:
            st.session_state.api_connected = False
            st.error("Failed to retrieve balance. Check API keys.")
    except Exception as e:
        st.session_state.api_connected = False
        st.error(f"Connection error: {e}")

# --- SIDEBAR ---
with st.sidebar:
    st.title("API Status")
    
    st.button("Check Connection", on_click=check_connection, use_container_width=True)
    
    if st.session_state.api_connected:
        st.success("Connected")
        st.metric("USDT Balance", f"${st.session_state.usdt_balance:.2f}")
    else:
        st.warning("Not connected")
        st.markdown("Ensure `.env` contains valid `API_KEY` and `SECRET_KEY`.")

# --- MAIN AREA ---
st.title("Trading Bot Dashboard")
st.markdown("Place orders on the Binance Futures Testnet directly from this interface.")

st.subheader("Order Entry")

symbol = st.selectbox("Symbol", options=["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT"])

current_price = None
if st.session_state.api_connected:
    try:
        client = BinanceClient()
        current_price = client.fetch_symbol_price(symbol)
        if current_price:
            st.metric(f"Real-time {symbol} Mark Price", f"${current_price:.2f}")
    except Exception:
        pass

col1, col2 = st.columns(2)
with col1:
    order_type = st.selectbox("Order Type", options=["MARKET", "LIMIT", "STOP_LIMIT"])
    quantity = st.number_input("Quantity", min_value=0.001, step=0.001, format="%.3f")

with col2:
    side = st.selectbox("Side", options=["BUY", "SELL"])
    
    price = 0.0
    stop_price = 0.0
    
    if order_type in ["LIMIT", "STOP_LIMIT"]:
        price = st.number_input("Limit Price", min_value=0.0, step=1.0, format="%.2f")
        
    if order_type == "STOP_LIMIT":
        stop_price = st.number_input("Stop Price", min_value=0.0, step=1.0, format="%.2f")
        
        from bot.validators import would_trigger_immediately
        if current_price and stop_price > 0:
            if would_trigger_immediately(stop_price, current_price, side):
                st.warning(f"⚠️ Warning: A {side} stop order at {stop_price} would trigger immediately since the current price is {current_price}.")
    
st.markdown("---")
    
if st.button("Submit Order", use_container_width=True):
    if not st.session_state.api_connected:
        st.error("Please connect to the API first using the sidebar.")
    else:
        try:
            client = BinanceClient()
            manager = OrderManager(client)
            
            with st.spinner(f"Placing {order_type} order..."):
                if order_type == "MARKET":
                    response = manager.place_market_order(symbol, side, quantity)
                elif order_type == "LIMIT":
                    response = manager.place_limit_order(symbol, side, quantity, price)
                elif order_type == "STOP_LIMIT":
                    response = manager.place_stop_limit_order(symbol, side, quantity, stop_price, price)
            
            st.success(f"Order Placed Successfully! Order ID: {response.get('orderId')}")
            st.json(response)
            
        except Exception as e:
            st.error(f"Failed to place order: {e}")
